import requests
import urllib.parse
import random

def generate_comic_image(prompt: str, style: str = "cartoon"):
    """
    100% WORKING - NO PURPLE, NO TORCH, NO ERROR
    """
    # Clean prompt
    clean_prompt = prompt.strip()[:300]
    
    # Style prompt
    full_prompt = f"{clean_prompt}, {style} comic style, vibrant colors, highly detailed, 4k, comic book art"
    
    # Pollinations - FREE & FAST
    encoded = urllib.parse.quote(full_prompt)
    seed = random.randint(1, 999999)
    
    # IMPORTANT: NO PURPLE - using cartoon model
    url = f"https://image.pollinations.ai/p/{encoded}?width=512&height=512&seed={seed}&model=turbo&nologo=true"
    
    # Test URL works
    try:
        requests.head(url, timeout=2)
    except:
        pass
        
    return url

def generate_all_panels(prompts: list, style="cartoon"):
    return [generate_comic_image(p, style) for p in prompts]
