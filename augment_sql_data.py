"""
augment_sql_data.py -- Generation en boucle de donnees de reunion dans SQL Server.

Strategie :
  1. Charge 3 reunions sources depuis meetings.json.
  2. Les structure UNE SEULE FOIS via Gemini (templates).
  3. Boucle N fois : prend un template au hasard, randomise date/titre/score/duree,
     genere un identifiant unique, et insere directement dans SQL Server.

Usage :
  python augment_sql_data.py                 # 100 reunions par defaut
  python augment_sql_data.py --count 50      # 50 reunions
  python augment_sql_data.py --count 5       # test rapide
"""

import argparse
import copy
import random
import string
import sys
import time
import uuid
from datetime import date, timedelta

import config
import utils_ai_structurer
import utils_data
import utils_sql


# --- Noms et titres aleatoires ------------------------------------------------

CLIENTS = [
    "Montacer", "Abdelkrim", "Chakir Ghazrani", "Ahmed Benali",
    "Moncef Kettani", "Redouane El Fassi", "Serge Dupont",
    "Youssef Amrani", "Hamid Lahlou", "Nadia Chraibi",
    "Omar Benjelloun", "Fatima-Zahra Tazi", "Karim Idrissi",
    "Samir Bouazza", "Leila Haddad", "Hassan Mansouri",
    "Rachid Ouazzani", "Zineb Alaoui", "Amine Berrada",
    "Soukaina Filali",
]

TOPICS_POOL = [
    "Automatisation CRM", "Strategie digitale", "Suivi leads",
    "Pipeline commercial", "WhatsApp Business", "Integration ERP",
    "Formation equipe", "Tableau de bord KPI", "Gestion contacts",
    "Prospection B2B", "Relance clients", "Scoring leads",
    "Chatbot IA", "Marketing automation", "Reporting mensuel",
    "Budget previsionnel", "Negociation contrat", "Onboarding client",
    "Fidelisation", "Optimisation processus",
]

TITLE_PREFIXES = [
    "Reunion commerciale", "Point de suivi", "Appel decouverte",
    "Session strategique", "Presentation produit", "Negociation",
    "Revue trimestrielle", "Kick-off projet", "Demo solution",
    "Atelier de travail", "Bilan mensuel", "Call de qualification",
]


def random_date(start_months_ago: int = 6) -> str:
    """Genere une date ISO aleatoire dans les N derniers mois."""
    today = date.today()
    start = today - timedelta(days=start_months_ago * 30)
    delta = (today - start).days
    random_day = start + timedelta(days=random.randint(0, delta))
    return random_day.isoformat()


def randomize_template(template: dict, iteration: int) -> dict:
    """Cree une copie du template avec des donnees randomisees."""
    data = copy.deepcopy(template)

    # Client aleatoire
    client_name = random.choice(CLIENTS)
    data["client"]["client_name"] = client_name
    data["client"]["client_email"] = f"{client_name.lower().replace(' ', '.')}@email.com"

    # Titre aleatoire
    prefix = random.choice(TITLE_PREFIXES)
    data["meeting"]["title"] = f"{prefix} - {client_name}"

    # Date aleatoire sur 6 mois
    data["meeting"]["date"] = random_date(6)

    # Duree aleatoire (15-90 min)
    data["meeting"]["duration"] = random.randint(15, 90)

    # Score de sentiment aleatoire (0.3 - 0.95)
    data["meeting"]["sentiment_score"] = round(random.uniform(0.3, 0.95), 2)

    # Topics : 3 a 5 sujets aleatoires
    data["topics"] = random.sample(TOPICS_POOL, k=random.randint(3, 5))

    return data


# --- Main ---------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Boucle d'augmentation de donnees dans SQL Server."
    )
    parser.add_argument(
        "--count", type=int, default=100,
        help="Nombre de reunions fictives a generer (defaut: 100)"
    )
    parser.add_argument(
        "--model", type=str, default="models/gemini-2.0-flash-lite",
        help="Modele Gemini pour la structuration initiale des templates"
    )
    args = parser.parse_args()

    print("=" * 60)
    print(f"  AUGMENTATION SQL SERVER -- {args.count} reunions")
    print("=" * 60)

    # 1. Connexion SQL
    print("\n[1/4] Test de la connexion SQL Server...")
    sql_check = utils_sql.check_connection()
    if not sql_check["ok"]:
        print(f"  [FAIL] Erreur : {sql_check['message']}")
        sys.exit(1)
    print(f"  [OK] Connecte : {sql_check['database']} ({sql_check['driver']})")

    # 2. Config Gemini
    print("\n[2/4] Configuration du modele IA...")
    try:
        model = config.configure(model_name=args.model)
        print(f"  [OK] Modele : {model.model_name}")
    except Exception as e:
        print(f"  [FAIL] Erreur : {e}")
        sys.exit(1)

    # 3. Creation des templates (appel IA unique)
    print("\n[3/4] Creation des templates IA (3 reunions sources)...")
    meetings = utils_data.load_meetings()
    if len(meetings) < 3:
        print(f"  [FAIL] Pas assez de reunions sources ({len(meetings)}/3 min).")
        sys.exit(1)

    # Prendre 3 reunions avec le plus de contenu
    meetings_sorted = sorted(
        meetings,
        key=lambda m: len(m.get("transcript_clean", m.get("transcript", ""))),
        reverse=True
    )
    sources = meetings_sorted[:3]

    templates = []
    for i, src in enumerate(sources):
        title = src.get("title", f"Source_{i}")
        print(f"  -> Structuration de << {title} >>...")
        try:
            transcript = src.get("transcript_clean", src.get("transcript", ""))
            structured = utils_ai_structurer.structure_transcript_for_sql(
                transcript=transcript,
                report_text=transcript,
                kpis=src.get("kpis", None),
                model=model,
                meeting_title=title
            )
            templates.append(structured)
            print(f"    [OK] Template {i+1} pret.")
            time.sleep(2)  # Pause API
        except Exception as e:
            print(f"    [FAIL] Echec : {e}")

    if not templates:
        print("  [FAIL] Aucun template cree. Arret.")
        sys.exit(1)

    print(f"\n  [OK] {len(templates)} template(s) cree(s) avec succes.")

    # 4. Boucle d'insertion
    print(f"\n[4/4] Insertion de {args.count} reunions en boucle...")
    success = 0
    fail = 0

    for i in range(args.count):
        try:
            # Choisir un template au hasard et le randomiser
            template = random.choice(templates)
            data = randomize_template(template, i)

            # Identifiant unique
            source_id = f"augmented_{uuid.uuid4().hex[:12]}"

            # Segments fictifs legers (3-5 segments)
            num_segments = random.randint(3, 5)
            fake_segments = []
            t = 0.0
            for s in range(num_segments):
                duration = random.uniform(30, 180)
                fake_segments.append({
                    "start": round(t, 2),
                    "end": round(t + duration, 2),
                    "text": random.choice(data.get("topics", ["Discussion"]))
                })
                t += duration + random.uniform(5, 30)

            # Insertion SQL
            stats = utils_sql.insert_meeting_full(
                structured=data,
                source_meeting_id=source_id,
                raw_segments=fake_segments
            )
            success += 1

            total_rows = sum(
                v for k, v in stats.items()
                if k not in ["meeting_id_sql", "success"]
            )

            # Affichage progression
            pct = (i + 1) / args.count * 100
            print(
                f"  [{i+1:3d}/{args.count}] ({pct:5.1f}%) [OK] "
                f"{data['meeting']['title'][:40]:40s} "
                f"| {data['meeting']['date']} "
                f"| {total_rows} lignes "
                f"| ID: {stats['meeting_id_sql']}"
            )

        except Exception as e:
            fail += 1
            print(f"  [{i+1:3d}/{args.count}] [FAIL] Erreur : {e}")

    # 5. Rapport final
    print("\n" + "=" * 60)
    print("  BILAN")
    print("=" * 60)
    print(f"  Reussies   : {success}")
    print(f"  Echouees   : {fail}")
    print(f"  Total vise : {args.count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
