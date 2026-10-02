from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
import os

router = APIRouter()

# Gemini setup - optional
try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
except:
    gemini_model = None

from app.ai.image_generator import generate_comic_image

@router.post("/generate")
async def generate_comic(prompt: str = Form(...), style: str = Form("cartoon comic")):
    try:
        # 1. Generate story panels
        if gemini_model:
            try:
                story_q = f"Break this into 4 comic panels, each 1 short sentence: {prompt}. Return like: 1) ... 2) ... 3) ... 4) ..."
                resp = gemini_model.generate_content(story_q)
                text = resp.text
                # Simple split
                panels_text = [line.strip() for line in text.split('\n') if len(line.strip()) > 10][:4]
                if len(panels_text) < 4:
                    panels_text = [f"{prompt} - panel {i+1}" for i in range(4)]
            except:
                panels_text = [f"{prompt} - panel {i+1}" for i in range(4)]
        else:
            panels_text = [f"{prompt} - panel {i+1}" for i in range(4)]

        # 2. Generate images - ALL REAL IMAGES
        result = []
        for p_text in panels_text[:4]:
            img_url = generate_comic_image(p_text, style)
            result.append({"text": p_text, "image": img_url})

        return JSONResponse({"status": "success", "panels": result, "prompt": prompt})
    
    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)

@router.get("/generate-test")
def generate_test(prompt: str = "superhero cat"):
    img = generate_comic_image(prompt)
    return {"prompt": prompt, "image": img, "status": "success"}
