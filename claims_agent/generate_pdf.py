from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_dummy_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "FNOL - First Notice of Loss")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, "Policy Information")
    c.drawString(50, height - 100, "Policy Number: POL-PDF-99")
    c.drawString(50, height - 115, "Policyholder: Alice Walker")
    c.drawString(50, height - 130, "Effective Dates: 2024-01-01 to 2025-01-01")
    
    c.drawString(50, height - 160, "Incident Details")
    c.drawString(50, height - 180, "Date: 2024-11-20")
    c.drawString(50, height - 195, "Time: 08:15")
    c.drawString(50, height - 210, "Location: Highway 101, CA")
    c.drawString(50, height - 225, "Description: Collision with a deer. Front bumper and hood damaged.")
    
    c.drawString(50, height - 255, "Financials")
    c.drawString(50, height - 275, "Estimated Damage: $4500.00")
    c.drawString(50, height - 290, "Initial Estimate: $4800.00")
    
    c.save()

if __name__ == "__main__":
    output_path = os.path.join("data", "fnol_05_mock.pdf")
    create_dummy_pdf(output_path)
    print(f"Created {output_path}")
