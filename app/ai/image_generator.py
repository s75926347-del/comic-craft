import os
import requests
import urllib.parse
import random
from PIL import Image, ImageDraw

def generate_image(desc="", style="comic", path="static/panels/panel.png", *args, **kwargs):
    # Handle if desc is dict or other type
    if isinstance(desc, dict):
        desc = desc.get('description', desc.get('prompt', str(desc)))
    if not isinstance(desc, str):
        desc = str(desc)
    if isinstance(path, dict):
        path = "static/panels/panel.png"
    
    # Also handle kwargs
    if 'description' in kwargs:
        desc = kwargs['description']
    if 'save_path' in kwargs:
        path = kwargs['save_path']

    # Fix path creation
    try:
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
    except:
        path = f"/tmp/panel_{random.randint(1,99999)}.png"

    if not desc or len(desc) < 3:
        desc = "epic comic book hero"

    # --- REAL AI GENERATION ---
    try:
        # Make super detailed prompt
        full_prompt = f"{style} art, {desc}, comic book illustration, highly detailed, vibrant colors, cinematic lighting, 4k, masterpiece"
        safe_prompt = urllib.parse.quote(full_prompt[:700])
        seed = random.randint(1, 9999999)
        
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=768&height=768&nologo=true&seed={seed}&model=turbo&enhance=true"
        
        print(f"Generating: {desc[:50]}")
        response = requests.get(url, timeout=90)
        
        if response.status_code == 200 and len(response.content) > 8000:
            with open(path, 'wb') as f:
                f.write(response.content)
            print(f"Saved AI image to {path}")
            return path
    except Exception as e:
        print(f"AI error: {e}")

    # Fallback so site never crashes
    try:
        img = Image.new('RGB', (768, 768), color=(108, 92, 231))
        draw = ImageDraw.Draw(img)
        draw.text((40, 350), f"{style}\n{desc[:100]}", fill="white")
        img.save(path)
    except:
        pass
    return path

# Compatibility for all old function names
def generate_comic_image(*a, **k):
    return generate_image(*a, **k)

def create_image(*a, **k):
    return generate_image(*a, **k)

def generate_panel(*a, **k):
    return generate_image(*a, **k)
