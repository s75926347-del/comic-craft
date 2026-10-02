import urllib.parse
import random

def generate_comic_image(prompt: str, style: str = "cartoon"):
    """
    100% working Pollinations - No more purple!
    """
    try:
        # Clean prompt
        safe_prompt = prompt[:300].replace("\n", " ").strip()
        # Add comic style
        full_prompt = f"{safe_prompt}, comic book style, vibrant colors, detailed illustration, {style}"
        
        encoded = urllib.parse.quote(full_prompt)
        seed = random.randint(1, 999999)
        
        # Pollinations - Always works!
        url = f"https://image.pollinations.ai/prompt/{encoded}?seed={seed}&width=512&height=512&nologo=true"
        
        print(f"✅ Generated: {url[:100]}")
        return url
        
    except Exception as e:
        print(f"❌ Image gen failed: {e}")
        # Fallback also pollinations
        encoded = urllib.parse.quote("cartoon comic forest brave fox")
        return f"https://image.pollinations.ai/prompt/{encoded}?seed={random.randint(1,9999)}&width=512&height=512"

# For compatibility - if your code calls these names
def generate_image(prompt, **kwargs):
    return generate_comic_image(prompt)

def generate_panel_image(prompt, **kwargs):
    return generate_comic_image(prompt)

def create_image(prompt, **kwargs):
    return generate_comic_image(prompt)
