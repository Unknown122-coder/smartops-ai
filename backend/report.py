import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# 🔹 Get project root directory (smartops_ai)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 🔹 Reports folder at project root
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
REPORT_PATH = os.path.join(REPORTS_DIR, "business_report.pdf")

def generate_pdf(result):
    # ✅ Ensure reports folder exists
    os.makedirs(REPORTS_DIR, exist_ok=True)

    c = canvas.Canvas(REPORT_PATH, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "SmartOps AI – Business Analysis Report")

    c.setFont("Helvetica", 12)
    y = height - 100

    for key, value in result.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20

        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 50

    c.save()
    return REPORT_PATH
