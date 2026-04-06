
import os
import json
import time
import config
from app import generate_global_report
import utils_pdf

def test_global_report():
    print("--- Testing Global Activity Report ---")
    
    # 1. Configure Model
    try:
        model = config.configure()
        print(f"Model configured: {model.model_name}")
    except Exception as e:
        print(f"FAILED to configure model: {e}")
        return

    # 2. Mock Data
    transcripts_dict = {
        "Meeting 1: Immobilier Lead": "Client Montacer s'intéresse à l'automatisation. Pain: perte de leads WhatsApp.",
        "Meeting 2: Suivi CRM": "Abdelkrim veut un CRM simple. Objection: coût de setup.",
        "Meeting 3: Clôture Deal": "Montacer est convaincu. Accord pour un pilote lundi."
    }

    # 3. Generate Global Audit
    print("Generating Global Strategic Audit...")
    try:
        global_audit = generate_global_report(transcripts_dict, model)
        print("--- Global Audit Output ---")
        print(global_audit[:500] + "...")
        
        # Save as PDF
        pdf_bytes = utils_pdf.create_pdf(global_audit, title="AUDIT STRATÉGIQUE GLOBAL")
        with open("repro_global_audit.pdf", "wb") as f:
            f.write(pdf_bytes)
        print("SUCCESS: repro_global_audit.pdf created.")
            
    except Exception as e:
        print(f"FAILED to generate global report: {e}")

if __name__ == "__main__":
    test_global_report()
