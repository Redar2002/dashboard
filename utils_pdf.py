from fpdf import FPDF
import io
import time

class PDF(FPDF):
    def __init__(self, title="RAPPORT D'AMÉLIORATION DE RÉUNION"):
        super().__init__()
        self.report_title = title
        self.primary_color = (103, 78, 167)  # Inspirigence Purple
        self.dark_gray = (40, 40, 40)
        self.light_gray = (245, 245, 245)

    def header(self):
        # Premium Header Bar
        self.set_fill_color(*self.primary_color)
        self.rect(0, 0, 210, 35, 'F')
        
        # Logo placeholder or Text
        try:
            self.image('logo_inspirigence.jpg', x=10, y=8, h=15)
        except Exception:
            self.set_font('Helvetica', 'B', 16)
            self.set_text_color(255, 255, 255)
            self.set_xy(10, 10)
            self.cell(0, 10, "INSPIRIGENCE")

        # Title on the right side of the banner
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(255, 255, 255)
        self.set_xy(100, 12)
        self.cell(100, 10, self.report_title.upper(), 0, 0, 'R')
        
        self.ln(30)

    def footer(self):
        # Subtle Footer
        self.set_y(-20)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        
        # Line above footer
        self.set_draw_color(220, 220, 220)
        self.line(10, self.get_y(), 200, self.get_y())
        
        # Content
        self.cell(0, 10, f'Inspirigence Groupe - Document Confidentiel', 0, 0, 'L')
        self.cell(0, 10, f'Page {self.page_no()} sur {{nb}}', 0, 0, 'R')

def create_pdf(text, title=None):
    # Detect if this is a professional minutes report to use the Hubspot design
    if "COMPTE RENDU DE RÉUNION" in text.upper() and ("APPEL" in text.upper() or "PARTICIPANTS" in text.upper()):
        return create_hubspot_pdf(text, title)
        
    if title:
        pdf = PDF(title=title)
    else:
        pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=40)
    pdf.set_font("Helvetica", size=10)
    
    # Final aggressive cleaning for Latin-1 compatibility
    def clean_for_latin1(s):
        # Map some common unicode characters to latin-1 equivalents
        s = s.replace('’', "'").replace('–', "-").replace('—', "-").replace('…', "...")
        s = s.replace('“', '"').replace('”', '"').replace('‘', "'").replace('€', "EUR")
        s = s.replace('œ', 'oe').replace('Œ', 'OE')
        # Strip any other non-latin-1 characters (emojis, etc.) to avoid "?"
        return "".join(c if ord(c) < 256 else "" for c in s)

    lines = text.split('\n')
    primary_color = (103, 78, 167)  # Purple
    secondary_color = (60, 60, 60) # Dark Gray
    accent_color = (30, 136, 229)   # Blue
    
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(4)
            continue
            
        try:
            line = clean_for_latin1(line)
            
            # Heading Level 1 (#) - Major Section
            if line.startswith('# '):
                pdf.ln(8)
                section_title = line[2:].upper()
                
                # Background block for H1
                pdf.set_fill_color(240, 235, 255) # Light Purple tint
                pdf.set_draw_color(*primary_color)
                pdf.set_line_width(0.5)
                
                curr_y = pdf.get_y()
                pdf.rect(10, curr_y, 190, 12, 'FD') # Fill and Draw
                
                pdf.set_xy(15, curr_y + 1)
                pdf.set_font("Helvetica", 'B', 16)
                pdf.set_text_color(*primary_color)
                pdf.cell(0, 10, section_title, new_x="LMARGIN", new_y="NEXT", align='L')
                
                pdf.ln(5)
                pdf.set_font("Helvetica", size=11)
                pdf.set_text_color(40, 40, 40)
                
            # Heading Level 2 (##) - Sub Section
            elif line.startswith('## '):
                pdf.ln(6)
                pdf.set_font("Helvetica", 'B', 14)
                pdf.set_text_color(*accent_color)
                
                # Double line accent for H2
                curr_y = pdf.get_y()
                pdf.cell(0, 8, line[3:].strip(), new_x="LMARGIN", new_y="NEXT", align='L')
                
                pdf.set_draw_color(*accent_color)
                pdf.set_line_width(0.3)
                pdf.line(10, pdf.get_y(), 50, pdf.get_y())
                
                pdf.ln(3)
                pdf.set_font("Helvetica", size=11)
                pdf.set_text_color(40, 40, 40)

            # Bullet points
            elif line.startswith('- ') or line.startswith('* '):
                pdf.set_x(15)
                # Modern caret bullet
                pdf.set_font("Helvetica", 'B', 11)
                pdf.set_text_color(*primary_color)
                pdf.write(7, "  > ") 
                
                pdf.set_font("Helvetica", '', 11)
                pdf.set_text_color(40, 40, 40)
                process_bold_text_inline(pdf, line[2:])
                pdf.ln(7)
                
            # Standard Text
            else:
                pdf.set_font("Helvetica", '', 11)
                pdf.set_text_color(40, 40, 40)
                process_bold_text_inline(pdf, line)
                pdf.ln(7)

        except Exception as e:
            pdf.set_font("Helvetica", size=8)
            pdf.cell(0, 5, f"[Erreur ligne: {str(e)}]", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())

def create_hubspot_pdf(text, title=None):
    """Specialized PDF generator with Inspirigence Branding (HubSpot-style layout)"""
    pdf = FPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=30)
    
    # New Branding Colors (Purple & Slate)
    primary_color = (103, 78, 167) # Inspirigence Purple
    dark_gray = (40, 40, 40)
    label_color = (200, 80, 0) # Accent for labels
    
    def clean(s):
        s = s.replace('’', "'").replace('–', "-").replace('—', "-").replace('…', "...")
        s = s.replace('œ', 'oe').replace('Œ', 'OE')
        s = s.replace('**', '').replace('__', '').replace('*', '').replace('_', '')
        return "".join(c if ord(c) < 256 else "" for c in s)

    # Parsing the text
    data = {}
    current_section = None
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith('# '): data['main_title'] = line[2:].strip()
        elif line.startswith('## '): 
            current_section = line[3:].strip().upper()
            if "DÉCISIONS" in current_section: current_section = "DÉCISIONS"
            if "ACTIONS" in current_section: current_section = "ACTIONS"
            if "PARTICIPANTS" in current_section: current_section = "PARTICIPANTS"
        elif current_section == "PARTICIPANTS":
            clean_line = line.lstrip("- *").strip()
            if clean_line.lower().startswith("absent"):
                continue
            if "équipe inspirigence" in clean_line.lower():
                current_sub = "TEAM"
                val = clean_line.split(":", 1)[-1].strip()
                if val: data.setdefault("TEAM", []).append(val)
            elif "clients / prospect" in clean_line.lower() or "client" in clean_line.lower():
                current_sub = "CLIENTS"
                val = clean_line.split(":", 1)[-1].strip()
                if val: data.setdefault("CLIENTS", []).append(val)
            elif clean_line:
                 # Default to whichever sub-section we are in
                 if 'current_sub' in locals():
                     data.setdefault(current_sub, []).append(clean_line)
                 else:
                     data.setdefault("TEAM", []).append(clean_line)
        elif ':' in line and not line.startswith('- ') and current_section is None:
            parts = line.split(':', 1)
            key = parts[0].strip().upper()
            val = parts[1].strip()
            data[key] = val
        elif current_section:
            clean_line = line.lstrip('- *').strip()
            if clean_line:
                # Basic smart split for merged Participants/Excusés
                if current_section == "PARTICIPANTS":
                    if clean_line.lower().startswith("absent") or clean_line.lower().startswith("excus"):
                        data.setdefault("EXCUSÉS", []).append(clean_line.split(":", 1)[-1].strip())
                    elif clean_line.lower().startswith("présent"):
                        data.setdefault("PARTICIPANTS", []).append(clean_line.split(":", 1)[-1].strip())
                    else:
                        data.setdefault("PARTICIPANTS", []).append(clean_line)
                else:
                    data.setdefault(current_section, []).append(clean_line)

    # --- HEADER DESIGN ---
    # New Logo: Inspirigence Group
    try:
        pdf.image('logo_inspirigence.jpg', x=15, y=8, h=12) # Shrunk logo
    except Exception:
        # Fallback if image missing
        pdf.set_font("Helvetica", 'B', 18)
        pdf.set_text_color(*primary_color)
        pdf.set_xy(15, 12)
        pdf.cell(0, 10, "INSPIRIGENCE")
    
    # Right side: Minutes Info
    pdf.set_font("Helvetica", 'I', 10)
    pdf.set_text_color(*primary_color)
    pdf.set_xy(150, 12)
    pdf.cell(50, 5, "Compte-rendu", align='R', ln=1)
    pdf.set_x(150)
    pdf.cell(50, 5, f"No {time.strftime('%Y%m')}-XXX", align='R', ln=1)
    pdf.set_x(150)
    pdf.cell(50, 5, clean(data.get('DATE', '')), align='R', ln=1)

    # Big Title Box
    pdf.ln(5)
    curr_y = pdf.get_y()
    pdf.set_draw_color(*primary_color)
    pdf.set_line_width(0.6)
    pdf.line(10, curr_y, 200, curr_y)
    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 18) # Shrunk from 24
    pdf.set_text_color(*dark_gray)
    header_title = clean(data.get('main_title', 'COMPTE RENDU DE RÉUNION'))
    pdf.cell(0, 12, header_title, align='C', ln=1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    
    # Subtitle
    pdf.ln(3)
    pdf.set_font("Helvetica", 'BI', 12) # Shrunk from 14
    pdf.cell(0, 8, clean(data.get('TITRE', 'Réunion sans titre')), align='C', ln=1)

    # --- SECTIONS ---
    
    # 1. Appel à l'ordre
    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_text_color(*label_color)
    pdf.cell(0, 10, clean("Détails de la réunion"), ln=1)
    
    # Unified Info Box (2 columns for compactness)
    pdf.set_draw_color(*primary_color)
    pdf.set_line_width(0.1)
    start_y = pdf.get_y()
    
    meeting_info = [
        ("Date :", data.get('DATE', 'Non spécifiée'), "Lieu :", data.get('LIEU', 'RABAT')),
        ("Organisateur :", data.get('ORGANISATEUR', 'Inspirigence Groupe'), "Type :", data.get('TYPE', 'Stratégique')),
        ("Animateur :", data.get('ANIMATEUR', 'A définir'), "Rédacteur :", data.get('RÉDACTEUR', 'IA Gemini'))
    ]
    
    box_h = len(meeting_info) * 6 + 4 # Tighter row height
    pdf.rect(10, start_y, 190, box_h)
    
    pdf.set_xy(15, start_y + 2)
    for l1, v1, l2, v2 in meeting_info:
        # Col 1
        pdf.set_font("Helvetica", 'B', 8.5)
        pdf.set_text_color(*primary_color)
        pdf.cell(30, 6, clean(l1))
        pdf.set_font("Helvetica", '', 8.5)
        pdf.set_text_color(*dark_gray)
        pdf.cell(65, 6, clean(v1))
        
        # Col 2
        pdf.set_font("Helvetica", 'B', 8.5)
        pdf.set_text_color(*primary_color)
        pdf.cell(30, 6, clean(l2))
        pdf.set_font("Helvetica", '', 8.5)
        pdf.set_text_color(*dark_gray)
        pdf.cell(60, 6, clean(v2), ln=1)
        pdf.set_x(15)
    
    pdf.set_y(start_y + box_h + 5)

    # 2. Participants
    pdf.ln(5)
    start_y = pdf.get_y()
    
    p_text = ", ".join(data.get('TEAM', [])) if data.get('TEAM') else "Aucun"
    e_text = ", ".join(data.get('CLIENTS', [])) if data.get('CLIENTS') else "Aucun"
    
    # Calculate box height based on multi-cell wrap
    pdf.set_font("Helvetica", '', 9)
    p_h = (int(pdf.get_string_width(clean(p_text)) / 85) + 1) * 5
    e_h = (int(pdf.get_string_width(clean(e_text)) / 85) + 1) * 5
    box_h = max(15, p_h + 10, e_h + 10)
    
    pdf.rect(10, start_y, 190, box_h)
    pdf.line(10, start_y + 8, 200, start_y + 8) # Header line
    pdf.line(105, start_y, 105, start_y + box_h)      # Middle separator
    
    pdf.set_font("Helvetica", 'B', 9)
    pdf.set_text_color(*primary_color)
    pdf.set_xy(10, start_y + 1.5)
    pdf.cell(95, 5, "Equipe Inspirigence", align='C')
    pdf.cell(95, 5, clean("Clients / Prospect"), align='C')
    
    pdf.set_font("Helvetica", '', 9)
    pdf.set_text_color(*dark_gray)
    
    # Draw Multi-cells for both columns
    pdf.set_xy(12, start_y + 9)
    pdf.multi_cell(90, 5, clean(p_text), border=0, align='L')
    
    pdf.set_xy(108, start_y + 9)
    pdf.multi_cell(90, 5, clean(e_text), border=0, align='L')
    
    pdf.set_y(start_y + box_h)
    
    pdf.set_y(start_y + box_h)

    # Next sections in boxes
    def draw_section_box(title, content_key):
        pdf.ln(5)
        if pdf.get_y() > 230: pdf.add_page()
        
        pdf.set_font("Helvetica", 'B', 12)
        pdf.set_text_color(*label_color)
        pdf.cell(0, 10, clean(title), ln=1)
        
        start_y = pdf.get_y()
        content_items = data.get(content_key, [])
        content_str = "\n".join(content_items) if content_items else "Non spécifié"
        
        pdf.set_font("Helvetica", '', 11)
        pdf.set_text_color(*dark_gray)
        
        # Draw text first to see how much space it takes
        pdf.set_xy(15, start_y + 2)
        pdf.multi_cell(180, 6, clean(content_str))
        
        end_y = pdf.get_y()
        actual_h = max(20, end_y - start_y + 4)
        
        # Draw the rectangle after knowing the actual height
        pdf.set_draw_color(*primary_color)
        pdf.set_line_width(0.2)
        pdf.rect(10, start_y, 190, actual_h)
        
        # Reset Y to below the box
        pdf.set_y(start_y + actual_h + 5)

    def draw_actions_table():
        pdf.ln(5)
        if pdf.get_y() > 230: pdf.add_page()
        
        pdf.set_font("Helvetica", 'B', 12)
        pdf.set_text_color(*label_color)
        pdf.cell(0, 10, clean("Actions à mener"), ln=1)
        
        # Table Header
        pdf.set_fill_color(*primary_color)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", 'B', 10)
        
        cols = [("Responsable", 35), ("Action", 120), ("Échéance", 35)]
        for name, width in cols:
            pdf.cell(width, 8, clean(name), border=1, align='C', fill=True)
        pdf.ln(8)
        
        # Table Body
        pdf.set_text_color(*dark_gray)
        pdf.set_font("Helvetica", '', 9)
        pdf.set_draw_color(*primary_color)
        
        actions = data.get('ACTIONS', [])
        for line in actions:
            # Filter out formatting instructions or empty examples
            if any(x in line.lower() for x in ["format :", "responsable | action", "[nom] |"]):
                continue
                
            parts = [p.strip() for p in line.split('|')]
            while len(parts) < 3: parts.append("")
            
            action_text = clean(parts[1])
            
            # Predict height
            num_lines = pdf.get_string_width(action_text) / 115
            est_row_h = max(10, (int(num_lines) + 1) * 6)
            
            if pdf.get_y() + est_row_h > 270:
                pdf.add_page()
                # Redraw header
                pdf.set_fill_color(*primary_color)
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Helvetica", 'B', 10)
                for name, width in cols:
                    pdf.cell(width, 8, clean(name), border=1, align='C', fill=True)
                pdf.ln(8)
                pdf.set_text_color(*dark_gray)
                pdf.set_font("Helvetica", '', 9)

            curr_y = pdf.get_y()
            
            # Draw middle column (Action) with padding inside
            # X offset: 45 + 3mm padding = 48
            # W reduced: 120 - 6mm padding = 114
            pdf.set_xy(48, curr_y + 3) 
            pdf.multi_cell(114, 5, action_text, border=0)
            end_y = pdf.get_y()
            final_h = max(12, end_y - curr_y + 5) # Increased height for vertical padding
            
            # Draw cells and borders with consistent height
            pdf.set_line_width(0.1)
            pdf.set_xy(10, curr_y)
            pdf.cell(35, final_h, clean(parts[0]), border=1, align='C')
            pdf.set_xy(45, curr_y)
            pdf.cell(120, final_h, "", border=1) # Outer border for Multi-cell area
            pdf.set_xy(165, curr_y)
            pdf.cell(35, final_h, clean(parts[2]), border=1, align='C')
            
            pdf.set_y(curr_y + final_h)

    # Removed Objectifs box as it's often empty/N/A in flash reports
    draw_section_box("Décisions et Points Clés", "DÉCISIONS")
    draw_actions_table()

    # Footer
    pdf.set_y(-15)
    pdf.set_font("Helvetica", '', 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, f"Page {pdf.page_no()} sur {{nb}}", align='R')

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
