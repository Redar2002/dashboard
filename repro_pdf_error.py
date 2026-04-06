from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=10)
pdf.cell(0, 10, "Test", 0, 1)

try:
    output = pdf.output()
    print(f"Output type: {type(output)}")
    print("PDF generated successfully")
except Exception as e:
    print(f"Error: {e}")
