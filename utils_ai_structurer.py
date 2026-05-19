"""
utils_ai_structurer.py — Transformation IA : transcription → JSON conforme au schéma SQL Server
Utilise Gemini pour extraire des données structurées à partir du texte brut.
"""
import json
import re
import config
from datetime import date


# ─── Prompt principal ─────────────────────────────────────────────────────────

def structure_transcript_for_sql(
    transcript: str,
    report_text: str,
    kpis: dict,
    model,
    meeting_title: str = "Réunion commerciale"
) -> dict:
    """
    Envoie la transcription + le rapport à Gemini et reçoit un JSON
    structuré conforme au schéma SQL Server MeetingIntelligence.

    Retourne un dict Python prêt à être inséré via utils_sql.insert_meeting_full()
    """

    today = date.today().isoformat()
    global_score = kpis.get("global_score", 0) if kpis else 0
    pain = kpis.get("pain_intensity", "Moyenne") if kpis else "Moyenne"

    prompt = f"""Tu es un assistant de structuration de données.
Ta mission est d'analyser une transcription de réunion commerciale et de produire un JSON STRICT, sans aucun texte avant ou après.

CONTEXTE :
- Titre de la réunion : {meeting_title}
- Date du jour : {today}
- Score global (0-100) : {global_score}
- Intensité du besoin : {pain}

TRANSCRIPTION :
\"\"\"
{transcript[:15000]}
\"\"\"

RAPPORT D'ANALYSE :
\"\"\"
{report_text[:5000]}
\"\"\"

INSTRUCTIONS CRITIQUES :
1. Identifie les informations demandées en te basant UNIQUEMENT sur la transcription et le rapport.
2. Pour "sentiment_score", convertis le global_score (0-100) en valeur décimale (0.0 à 1.0).
3. Pour "duration", estime la durée en minutes (compte les segments si possible, sinon 30 par défaut).
4. Pour le "client", utilise les informations du prospect/client mentionné. Si plusieurs clients, prends le principal.
5. client_email peut rester vide "" si non mentionné.
6. "topics" : liste de 3 à 6 thèmes clés discutés (strings courts).
7. "decisions" : liste des décisions prises ou engagements formulés (verbes d'action).
8. "actions" : liste avec pour chaque action : action_text, assigned_to (Commercial/Client/Les deux), status ("À faire").
9. "report.summary" : résumé en 3 phrases max.
10. "report.pain_points" : les 2-3 douleurs/problèmes principaux du client identifiés.
11. "report.recommendations" : les 2-3 recommandations prioritaires issues du rapport.

FORMAT JSON EXACT ATTENDU (ne rien ajouter d'autre) :
{{
  "client": {{
    "client_name": "Nom du client ou de l'entreprise",
    "client_email": ""
  }},
  "meeting": {{
    "title": "{meeting_title}",
    "date": "{today}",
    "duration": 30,
    "sentiment_score": 0.75
  }},
  "topics": [
    "Sujet 1",
    "Sujet 2",
    "Sujet 3"
  ],
  "decisions": [
    "Décision ou engagement 1",
    "Décision ou engagement 2"
  ],
  "actions": [
    {{
      "action_text": "Description de l'action",
      "assigned_to": "Commercial",
      "status": "À faire"
    }}
  ],
  "report": {{
    "summary": "Résumé de la réunion en 2-3 phrases.",
    "pain_points": "Douleur 1. Douleur 2.",
    "recommendations": "Recommandation 1. Recommandation 2."
  }}
}}

RAPPEL : Renvoie UNIQUEMENT le JSON. Pas de ```json, pas d'explication, pas de commentaire."""

    response, _ = config.generate_with_retry(
        model_name=model.model_name,
        content=prompt,
        generation_config={"temperature": 0.0},
        request_options={"timeout": 120}
    )

    raw = response.text.strip()
    # Nettoyage défensif des balises markdown si Gemini les ajoute quand même
    raw = re.sub(r"^```(?:json)?", "", raw, flags=re.MULTILINE).strip()
    raw = re.sub(r"```$", "", raw, flags=re.MULTILINE).strip()

    return json.loads(raw)


# ─── Validation ───────────────────────────────────────────────────────────────

def validate_structured_data(data: dict) -> tuple[bool, list]:
    """
    Vérifie la cohérence du JSON structuré avant insertion.
    Retourne (is_valid, liste_d_erreurs).
    """
    errors = []
    required_keys = ["client", "meeting", "topics", "decisions", "actions", "report"]

    for key in required_keys:
        if key not in data:
            errors.append(f"Clé manquante : '{key}'")

    if "meeting" in data:
        m = data["meeting"]
        if not m.get("title"):
            errors.append("meeting.title est vide")
        score = m.get("sentiment_score", -1)
        if not (0.0 <= float(score) <= 1.0):
            errors.append(f"sentiment_score invalide : {score} (doit être entre 0.0 et 1.0)")
        try:
            int(m.get("duration", 0))
        except (ValueError, TypeError):
            errors.append("meeting.duration doit être un entier")

    if "client" in data:
        if not data["client"].get("client_name"):
            errors.append("client.client_name est vide")

    if "report" in data:
        if not data["report"].get("summary"):
            errors.append("report.summary est vide")

    return len(errors) == 0, errors
