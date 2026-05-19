import argparse
import time
import sys
import utils_data
import utils_sql
import utils_ai_structurer
import config

def main():
    parser = argparse.ArgumentParser(description="Automatisation du transfert de données des réunions vers SQL Server.")
    parser.add_argument("--limit", type=int, default=None, help="Nombre maximum de réunions à traiter")
    parser.add_argument("--model", type=str, default="models/gemini-2.0-flash-lite", help="Nom du modèle Gemini à utiliser")
    args = parser.parse_args()

    print(f"Demarrage du script d'importation SQL Server")
    print(f"Modèle sélectionné : {args.model}")
    if args.limit:
        print(f"Limite d'exécution fixée à {args.limit} réunion(s).")
    
    # 1. Test SQL
    print("\n[1/4] Test de la connexion SQL Server...")
    sql_check = utils_sql.check_connection()
    if not sql_check["ok"]:
        print(f"FAILED : Erreur critique: Impossible de joindre SQL Server.")
        print(f"   Détails: {sql_check['message']}")
        sys.exit(1)
    print(f"SUCCESS : Connecté avec succès : {sql_check['database']} ({sql_check['driver']})")

    # 2. Config Gemini
    print("\n[2/4] Configuration du modèle IA...")
    try:
        model = config.configure(model_name=args.model)
        print(f"SUCCESS : Modèle configuré : {model.model_name}")
    except Exception as e:
        print(f"FAILED : Erreur lors de la configuration du modèle: {e}")
        sys.exit(1)

    # 3. Charger meetings
    print("\n[3/4] Chargement des données locales...")
    meetings = utils_data.load_meetings()
    if not meetings:
        print("INFO : Aucune réunion trouvée dans meetings.json.")
        sys.exit(0)
    print(f"SUCCESS : {len(meetings)} réunion(s) chargée(s).")

    # 4. Traitement
    print("\n[4/4] Traitement itératif des réunions...")
    processed_count = 0
    success_count = 0
    fail_count = 0
    skipped_count = 0

    for idx, meeting in enumerate(meetings):
        # Limite
        if args.limit and processed_count >= args.limit:
            print(f"\nWARNING : Limite de {args.limit} réunion(s) atteinte. Arrêt.")
            break
            
        m_id = meeting.get("meeting_id", f"idx_{idx}")
        title = meeting.get("title", f"Sans_titre_{idx}")
        
        print(f"\n--- Réunion {idx+1}/{len(meetings)} : {title} ---")
        
        # Vérification doublons
        t0 = time.time()
        if utils_sql.meeting_already_inserted(source_meeting_id=m_id):
            print(f"SKIP : Déjà en base SQL. Ignore.")
            skipped_count += 1
            continue
            
        # Structuration IA
        print(f"AI : Structuration IA en cours...")
        try:
            transcript = meeting.get("transcript_clean", meeting.get("transcript", ""))
            if not transcript.strip():
                print(f"FAILED : Erreur : Transcription vide.")
                fail_count += 1
                continue
                
            structured_data = utils_ai_structurer.structure_transcript_for_sql(
                transcript=transcript,
                report_text=transcript,
                kpis=meeting.get("kpis", None),
                model=model,
                meeting_title=title
            )
            
            is_valid, errors = utils_ai_structurer.validate_structured_data(structured_data)
            if not is_valid:
                print(f"WARNING : Validation partielle - erreurs trouvées: {errors}")
            
            # Insertion
            print(f"SQL : Insertion SQL...")
            raw_segments = meeting.get("segments_clean", meeting.get("segments", []))
            
            stats = utils_sql.insert_meeting_full(
                structured=structured_data,
                source_meeting_id=m_id,
                raw_segments=raw_segments
            )
            
            # Stats success
            t1 = time.time()
            total_rows = sum(v for k, v in stats.items() if k not in ["meeting_id_sql", "success"])
            print(f"SUCCESS : Succès ! {total_rows} lignes insérées (ID: {stats['meeting_id_sql']}) en {t1-t0:.1f}s.")
            success_count += 1
            processed_count += 1
            
        except Exception as e:
            print(f"FAILED : Échec lors du traitement : {e}")
            fail_count += 1
            processed_count += 1
            
        # Petit délai de respiration entre chaque pour l'API Free si besoin (géré en partie par config fallback, mais une pause douce évite de saturer d'un coup)
        time.sleep(2)

    # 5. Rapport Final
    print(f"\n<<< Bilan de l'importation >>>")
    print(f"Total évalué     : {skipped_count + processed_count}")
    print(f"Ignorés (exist)  : {skipped_count}")
    print(f"Nouvelles insérées: {success_count}")
    print(f"Échecs           : {fail_count}")

if __name__ == "__main__":
    main()
