from fpdf import FPDF

def create_topic_pdf(text, topic_name):
    """Create a professional PDF for topic explanation guide"""
    
    class TopicPDF(FPDF):
        def __init__(self, topic):
            super().__init__()
            self.topic = topic
            
        def header(self):
            # Background for header
            self.set_fill_color(124, 58, 237)  # Purple gradient
            self.rect(0, 0, 210, 30, 'F')
            
            self.set_font('Helvetica', 'B', 18)
            self.set_text_color(255, 255, 255)
            self.cell(0, 20, f'GUIDE COMPLET', 0, 1, 'C')
            self.set_font('Helvetica', '', 14)
            self.cell(0, 5, self.topic.upper(), 0, 1, 'C')
            self.ln(15)

        def footer(self):
            # Footer Image
            self.set_y(-35)
            try:
                self.image('fouter.png', x=10, y=self.get_y(), w=190)
            except Exception:
                pass
                
            # Page number
            self.set_y(-15)
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(128)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    pdf = TopicPDF(topic_name)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=40)
    pdf.set_font("Helvetica", size=10)
    
    # Text cleaning - remove emojis
    replacements = {
        ''': "'", '–': "-", '—': "-", '…': "...",
        '"': '"', '"': '"', ''': "'", '€': "EUR",
        '•': "-", '✔': "[OK]", '✅': "[OK]", '❌': "[NO]",
        '📊': "", '📥': "", '📂': "", '🔧': "",
        '🎯': "", '💡': "", '🚀': "", '⚠️': "[!]", '✨': "", 
        '🤝': "", '⚖️': "", '📄': "", '📦': "", '📘': "",
        '🔍': "", '⚙️': "", '📈': "", '🔗': "", '🛡️': ""
    }
    
    cleaned_text = text
    for char, rep in replacements.items():
        cleaned_text = cleaned_text.replace(char, rep)
        
    lines = cleaned_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(4)
            continue
            
        try:
            line = line.encode('latin-1', 'replace').decode('latin-1')
            
            # Heading Level 1 (#)
            if line.startswith('# '):
                pdf.ln(5)
                pdf.set_font("Helvetica", 'B', 16)
                pdf.set_text_color(124, 58, 237)  # Purple
                pdf.cell(0, 10, line[2:].upper(), new_x="LMARGIN", new_y="NEXT", align='L')
                pdf.ln(2)
                # Border line
                pdf.set_draw_color(124, 58, 237)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(4)
                pdf.set_font("Helvetica", size=10)
                pdf.set_text_color(0)
                
            # Heading Level 2 (##)
            elif line.startswith('## '):
                pdf.ln(6)
                pdf.set_font("Helvetica", 'B', 13)
                pdf.set_text_color(99, 102, 241)  # Blue
                pdf.cell(0, 8, line[3:], new_x="LMARGIN", new_y="NEXT", align='L')
                pdf.ln(1)
                pdf.set_font("Helvetica", size=10)
                pdf.set_text_color(0)

            # Bullet points
            elif line.startswith('- ') or line.startswith('* '):
                pdf.set_x(15)
                pdf.set_font("Helvetica", 'B', 10)
                pdf.write(6, "- ")
                pdf.set_font("Helvetica", '', 10)
                process_bold_text_inline(pdf, line[2:])
                pdf.ln(6)
                
            # Standard Text
            else:
                process_bold_text_inline(pdf, line)
                pdf.ln(6)

        except Exception as e:
            pdf.set_font("Helvetica", size=8)
            pdf.cell(0, 5, f"[Erreur ligne: {str(e)}]", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())


def process_bold_text_inline(pdf, text):
    """Handles inline bold text using mapping segments."""
    parts = text.split("**")
    for i, part in enumerate(parts):
        if i % 2 == 1:
            pdf.set_font("Helvetica", 'B', 10)
        else:
            pdf.set_font("Helvetica", '', 10)
        pdf.write(6, part)
