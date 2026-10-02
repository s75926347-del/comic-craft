from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
import random

router = APIRouter()

@router.post("/generate")
async def generate_comic(prompt: str = Form(...), style: str = Form("cartoon comic")):
    # Dummy logic - un original logic iruntha atha vechukko
    panels = []
    for i in range(3):
        panels.append({
            "text": f"{prompt} - Scene {i+1}",
            "image": f"https://via.placeholder.com/512x512/ff6b35/ffffff?text=Panel+{i+1}"
        })
    return {"prompt": prompt, "style": style, "panels": panels}

@router.get("/test-image")
async def test_image(prompt: str = "brave fox"):
    return {"image": f"https://via.placeholder.com/512x512?text={prompt}"}

@router.get("/generate-test")
async def gen_test(prompt: str = "fox"):
    return await generate_comic(prompt=prompt, style="comic")
