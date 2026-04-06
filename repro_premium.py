
import os
import json
import time
import config
from app import generate_improvement_report, generate_pro_minutes
import utils_pdf

def test_premium_report():
    print("--- Testing Premium Report & Design ---")
    
    # 1. Configure Model
    try:
        model = config.configure()
        print(f"Model configured: {model.model_name}")
    except Exception as e:
        print(f"FAILED to configure model: {e}")
        return

    # 2. Complex Transcript Scenario
    transcript = """
Montacer (Client) : Bonjour, je cherche à automatiser mon agence immobilière. On reçoit 50 leads par jour via WhatsApp et Facebook, mais on en perd la moitié car mon équipe n'arrive pas à répondre assez vite.
Vendeur Inspirigence : C'est un problème classique de "Leads Leakage". Quel est votre taux de conversion actuel ?
Montacer : Environ 10%. On veut monter à 25%. On a déjà un CRM mais personne ne l'utilise, c'est trop complexe.
Vendeur Inspirigence : On a une solution "RealtyMatch" avec un Agent IA qui qualifie les leads en temps réel 24/7. Ça s'intègre avec votre CRM actuel ou on peut vous en proposer un plus simple.
Montacer : Et le prix ?
Vendeur Inspirigence : C'est un investissement sur le ROI. Si on double votre conversion, le système est payé en 15 jours. Le coût est de 500€/mois + frais de setup.
Montacer : D'accord, je dois voir avec mon associé Abdelkrim, mais ça m'intéresse beaucoup. On peut faire un test sur 3 jours ?
Vendeur Inspirigence : Absolument. Je vous envoie le devis et on démarre le pilote lundi.
"""

    # 3. Generate Improvement Report (The depth test)
    print("Generating Premium Improvement Report...")
    try:
        report_text, kpis, pdf_header = generate_improvement_report([transcript], model)
        print("--- Improvement Report Summary ---")
        print(report_text[:500] + "...")
        
        # Save as PDF
        pdf_bytes = utils_pdf.create_pdf(report_text, title=pdf_header)
        with open("test_premium_improvement.pdf", "wb") as f:
            f.write(pdf_bytes)
        print("SUCCESS: test_premium_improvement.pdf created.")
            
    except Exception as e:
        print(f"FAILED to generate improvement report: {e}")
        return

    # 4. Generate Pro Minutes (The design test)
    print("Generating Pro Minutes...")
    try:
        pro_minutes = generate_pro_minutes(report_text, model, titles=["Appel Découverte ImmobiLeads"])
        pdf_pro_bytes = utils_pdf.create_pdf(pro_minutes, title="COMPTE RENDU DE RÉUNION")
        with open("test_premium_minutes.pdf", "wb") as f:
            f.write(pdf_pro_bytes)
        print("SUCCESS: test_premium_minutes.pdf created.")
    except Exception as e:
        print(f"FAILED to generate pro minutes: {e}")

if __name__ == "__main__":
    test_premium_report()
