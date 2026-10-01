import os
from fpdf import FPDF
from datetime import datetime

def save_pdf(layout, filename=None):
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"static/exports/comic_{timestamp}.pdf"

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, panel['title'], ln=True)

        # Image
        if os.path.exists(panel['image_path']):
            pdf.image(panel['image_path'], x=10, w=190)
            pdf.ln(5)

        pdf.set_font("Arial", 'I', 12)
        pdf.multi_cell(0, 10, f"Scene: {panel['description']}")
        pdf.ln(5)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, f"Dialogue: {panel['dialogue']}")

    pdf.output(filename)
    return filename