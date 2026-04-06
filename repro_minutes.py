
import os
import json
import time
import config
from app import generate_pro_minutes
import utils_pdf

def test_minutes_reproduction():
    print("--- Testing Minutes Reproduction ---")
    
    # 1. Configure Model
    try:
        model = config.configure()
        print(f"Model configured: {model.model_name}")
    except Exception as e:
        print(f"FAILED to configure model: {e}")
        return

    # 2. Dummy Report Text
    dummy_report = """
# SYNTHÈSE STRATÉGIQUE

## Enjeux & Maturité
- Le client cherche un CRM pour centraliser la gestion des leads (50-100/jour). Maturité forte.

## MEDDIC Flash
- **Metrics/Buyer** : Augmenter le taux de conversion de 20% à 30%. CEO est le décideur.
- **Process** : Déploiement en 72h.
- **Pain** : Perte de temps et d'énergie dans le suivi manuel (WhatsApp, FB, IG).
- **Champion** : Abdelkrim (très engagé).

## Alignement & Upsell
- **Fit** : Parfait adéquation avec l'offre IA Automation.
- **Upsell** : Potentiel de chatbot qualification.
"""

    # 3. Generate Pro Minutes
    print("Generating Pro Minutes via AI...")
    try:
        titles = ["Appel Découverte - Monsef", "Suivi Projet - Abdelkrim"]
        pro_minutes = generate_pro_minutes(dummy_report, model, titles=titles)
        print("--- Pro Minutes Output ---")
        print(pro_minutes)
        print("---------------------------")
        
        if "Erreur" in pro_minutes:
            print(f"AI Generation returned an error: {pro_minutes}")
            return
            
    except Exception as e:
        print(f"FAILED to generate pro minutes: {e}")
        return

    # 4. Generate PDF
    print("Generating PDF...")
    try:
        pdf_bytes = utils_pdf.create_pdf(pro_minutes, title="COMPTE RENDU DE R\u00C9UNION")
        output_file = "repro_compte_rendu.pdf"
        with open(output_file, "wb") as f:
            f.write(pdf_bytes)
        print(f"SUCCESS: PDF saved to {output_file}")
    except Exception as e:
        print(f"FAILED to generate PDF: {e}")

if __name__ == "__main__":
    test_minutes_reproduction()
