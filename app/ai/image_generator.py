import os
from PIL import Image, ImageDraw
def generate_image(desc, style, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = Image.new('RGB', (512,512), color=(108,92,231))
    d = ImageDraw.Draw(img)
    d.rectangle([5,5,507,507], outline="white", width=4)
    d.text((20,220), f"{style}\n{desc[:70]}", fill=(255,255,255))
    img.save(path)
    return path