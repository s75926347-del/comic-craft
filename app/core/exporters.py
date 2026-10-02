import os
from fpdf import FPDF
from datetime import datetime
from PIL import Image

def save_pdf(layout, filename=None):
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"static/exports/comic_{timestamp}.pdf"

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        img_path = panel.get('image_path')

        if img_path and os.path.exists(img_path):
            try:
                with Image.open(img_path) as im:
                    if im.mode in ("RGBA", "P", "LA"):
                        bg = Image.new("RGB", im.size, (255, 255, 255))
                        if im.mode == "P":
                            im = im.convert("RGBA")
                        bg.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
                        im = bg
                    elif im.mode != "RGB":
                        im = im.convert("RGB")
                    im.save(img_path, "PNG")
            except Exception as e:
                print(f"Image fix failed {img_path}: {e}")

            try:
                pdf.image(img_path, x=10, w=190)
            except Exception as e:
                print(f"PDF add failed: {e}")
                continue

        if panel.get('text'):
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, panel['text'])

    pdf.output(filename)
    return filename
