import os
import requests
import urllib.parse

def generate_image(desc, style, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        # Make prompt safe for URL
        full_prompt = f"{style} comic art, {desc}, highly detailed, vibrant colors, comic book style"
        safe_prompt = urllib.parse.quote(full_prompt)
        
        # Free AI image - no API key needed!
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=512&height=512&nologo=true&seed={hash(desc) % 10000}"
        
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.content)
            return path
    except Exception as e:
        print(f"Image gen failed: {e}")

    # Fallback if fails
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (512,512), color=(108,92,231))
    d = ImageDraw.Draw(img)
    d.rectangle([5,5,507,507], outline="white", width=4)
    d.text((20,220), f"{style}\n{desc[:70]}", fill=(255,255,255))
    img.save(path)
    return path
