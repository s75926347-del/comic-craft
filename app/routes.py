from fastapi import APIRouter, Form
import random
import urllib.parse

router = APIRouter()

@router.post("/generate")
async def generate_comic(prompt: str = Form(...), style: str = Form("cartoon comic")):
    scenes = [
        f"{prompt}, opening scene, cinematic establishing shot",
        f"{prompt}, adventure begins, action pose",
        f"{prompt}, facing a big challenge, dramatic lighting",
        f"{prompt}, clever solution, bright colors",
        f"{prompt}, happy ending celebration, joyful"
    ]

    panels = []
    for i, scene in enumerate(scenes):
        encoded = urllib.parse.quote(f"{scene}, {style}, highly detailed comic book art, vibrant")
        seed = random.randint(1, 999999)
        image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=768&seed={seed}&nologo=true&model=flux"

        panels.append({
            "panel": i+1,
            "text": scenes[i],
            "image": image_url
        })

    return {"prompt": prompt, "panels": panels, "count": 5}

@router.get("/test-image")
async def test_image(prompt: str = "brave fox"):
    encoded = urllib.parse.quote(prompt)
    return {"image": f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512&nologo=true"}

@router.get("/generate-test")
async def gen_test(prompt: str = "fox"):
    return await generate_comic(prompt=prompt)
