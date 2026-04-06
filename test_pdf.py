from utils_pdf import create_pdf
import os

test_text = """
# Test Report
## Summary
This is a test report to verify the footer image.

- Item 1
- Item 2

### Conclusion
The footer should be visible at the bottom.
"""

try:
    pdf_bytes = create_pdf(test_text)
    with open("test_report.pdf", "wb") as f:
        f.write(pdf_bytes)
    print("PDF generated successfully: test_report.pdf")
except Exception as e:
    print(f"Error generating PDF: {e}")
