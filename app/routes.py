from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.ai.gemini_flash import generate_outline
from app.ai.gemini_pro import generate_story
from app.ai.image_generator import generate_image
from app.core.layout_builder import build_comic_layout
from app.core.exporters import save_pdf
from app.schemas import PromptRequest

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):
    user_full_prompt = f"Story: {story_prompt}, Character: {character_name}, Setting: {setting}, Tone: {tone}"
    panels = generate_outline(user_full_prompt)
    story_text = generate_story(panels)
    images = []
    for i, p in enumerate(panels):
        desc = p.description if hasattr(p, 'description') else str(p)
        img_path = f"static/panels/panel_{i+1}.png"
        saved = generate_image(desc, art_style, img_path)
        images.append(saved)
    layout = build_comic_layout(panels, images, story_text)
    pdf_path = save_pdf(layout)
    return templates.TemplateResponse(request, "comic_preview.html", {
        "request": request, "layout": layout, "pdf_path": pdf_path, "character_name": character_name
    })

@router.post("/generate-comic/json")
async def generate_comic_json(data: PromptRequest):
    panels = generate_outline(data.story_prompt)
    story_text = generate_story(panels)
    images = [generate_image(p.description, data.art_style, f"static/panels/panel_{i+1}.png") for i, p in enumerate(panels)]
    layout = build_comic_layout(panels, images, story_text)
    pdf_path = save_pdf(layout)
    return {"layout": layout, "pdf_path": pdf_path}

@router.get("/test-image")
async def test_image(prompt: str = "a brave fox in enchanted forest"):
    path = generate_image(prompt, "comic book", "static/panels/test.png")
    return {"image_path": path}

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request):
    return templates.TemplateResponse(request, "export_success.html", {"request": request})