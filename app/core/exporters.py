from fpdf import FPDF
from PIL import Image
import os

def save_pdf(layout):
    pdf = FPDF()
    
    for panel in layout:
        pdf.add_page()
        img_path = panel['image_path']
        
        # FIX: Image ah valid PNG ah maathu
        if os.path.exists(img_path):
            try:
                with Image.open(img_path) as im:
                    # RGB ku convert pannu
                    if im.mode in ("RGBA", "P", "LA"):
                        # White background
                        background = Image.new("RGB", im.size, (255, 255, 255))
                        if im.mode == "P":
                            im = im.convert("RGBA")
                        background.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
                        im = background
                    elif im.mode != "RGB":
                        im = im.convert("RGB")
                    
                    # Force ah PNG ah save pannu
                    im.save(img_path, "PNG")
            except Exception as e:
                print(f"Error fixing image {img_path}: {e}")
        
        try:
            pdf.image(img_path, x=10, y=10, w=190)
        except Exception as e:
            print(f"PDF image add failed: {e}")
            continue
            
        # Text iruntha add pannu
        if 'text' in panel and panel['text']:
            pdf.set_xy(10, 170)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(190, 10, panel['text'])

    pdf_path = "static/comic.pdf"
    os.makedirs("static", exist_ok=True)
    pdf.output(pdf_path)
    return pdf_path
