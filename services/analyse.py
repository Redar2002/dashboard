"""
services/analyse.py — Génération IA (rapports, comptes rendus, recherche, guides)
Toutes les fonctions reçoivent le modèle Gemini en paramètre.
"""
import json
import re
import time

import streamlit as st
from google.api_core.exceptions import ResourceExhausted

import config
import utils_data


def generate_improvement_report(transcripts, model):
    joined = "\n\n".join(transcripts)
    is_plural = len(transcripts) > 1
    
    prompt = f"""
Tu es un Senior Consultant en Cabinet de Conseil Stratégique (McKinsey / BCG).
Rédige un **RAPPORT D'ANALYSE PROFESSIONNEL** sur {"ces réunions" if is_plural else "cette réunion"}.

RÈGLES DE RÉDACTION :
- Longueur cible : 500 mots MAXIMUM (hors JSON)
- Chaque section doit être complète mais concise : pas de remplissage, que de la valeur
- Mélange équilibré : 1-2 phrases de contexte + bullet points pour les détails
- Ton professionnel, analytique, direct
- **ANONYMISATION OBLIGATOIRE** : Ne cite JAMAIS les prénoms ou noms des personnes (ex: pas de "Montacer", "Mathias", etc.). Remplace-les systématiquement par "Le Commercial" (ou "Le Vendeur") et "Le Client" (ou "Le Prospect").
- **AUCUN TABLEAU MARKDOWN** : N'utilise jamais de tableaux (ex: |---|---|). Utilise EXCLUSIVEMENT des listes à puces.

---

# 📊 RAPPORT D'ANALYSE — {"RÉUNIONS" if is_plural else "RÉUNION"}

---

## 🧭 Synthèse Exécutive
> *(2-3 phrases max : résumé du contexte, de l'enjeu principal, et du niveau de maturité du deal)*

---

## 🔎 Analyse MEDDIC

- 💢 **Pain identifié** [🔴/🟡/🟢] : [Description précise de la douleur business]
- 👤 **Economic Buyer** [🔴/🟡/🟢] : [Qui décide réellement + niveau d'accès]
- 📋 **Critères de décision** [🔴/🟡/🟢] : [Ce sur quoi le client va évaluer la solution]
- 🔀 **Processus de décision** [🔴/🟡/🟢] : [Étapes + délai estimé avant signature]
- 🏆 **Champion interne** [🔴/🟡/🟢] : [Allié identifié + niveau d'engagement]

*(🟢 = Favorable · 🟡 = À travailler · 🔴 = Point critique)*

---

## 🧠 Dynamique du Client

**Niveau d'engagement :** [Faible / Moyen / Élevé] — [1 phrase d'explication]

- **Signal positif :** [Ce qui a bien fonctionné dans l'échange]
- **Signal d'alerte :** [Hésitation, réticence ou zone floue détectée]
- **Niveau de conviction estimé :** [Froid / Tiède / Chaud] — justification courte

---

## ⚠️ Objections & Freins

- **[Objection principale]**
  - *Réponse recommandée :* [Script de réponse en 1 ligne]
- **[Objection secondaire]**
  - *Réponse recommandée :* [Script de réponse en 1 ligne]

---

## 🎯 Recommandations Stratégiques

1. **[Recommandation prioritaire]**
   - *Pourquoi :* [Justification en 1 ligne]
   - *Comment :* [Action concrète à mener]

2. **[Recommandation secondaire]**
   - *Pourquoi :* [Justification en 1 ligne]
   - *Comment :* [Action concrète à mener]

3. **[Recommandation tertiaire]**
   - *Pourquoi :* [Justification en 1 ligne]
   - *Comment :* [Action concrète à mener]

---

## 📧 Email de Suivi Recommandé

- **Objet :** [Objet court, percutant, personnalisé]
- **Angle d'approche :** [Angle stratégique de l'email en 1-2 phrases]

---

B. GENERE UN BLOC JSON STRICT À LA FIN pour les KPIs.
Le format du JSON doit être **exactement** celui-ci :
{{
  "global_score": 0-100,
  "listen_ratio_client": 0-100,
  "pain_intensity": "Faible" | "Moyenne" | "Forte",
  "phases_alignment": {{
    "Preparation": 1-5,
    "Introduction": 1-5,
    "Decouverte": 1-5,
    "Presentation": 1-5,
    "Conclusion": 1-5
  }}
}}

Sépare le rapport textuel du JSON par une ligne contenant uniquement : "---JSON-STATS---"

TRANSCRIPTION :
{joined}
"""

    try:
        response, used_model = config.generate_with_retry(
            model_name=model.model_name,
            content=prompt,
            generation_config={"temperature": 0.3},
            request_options={"timeout": 600}
        )
    except Exception as e:
        st.error(f"❌ Échec de génération du rapport : {e}")
        raise
    
    text_content = response.text
    kpi_data = None
    
    if is_plural:
        intro = "ANALYSE DES RÉUNIONS\n\nCe rapport identifie les forces et faiblesses de ces échanges et propose des actions concrètes d'amélioration.\n\n"
        pdf_header = "RAPPORT D'AMÉLIORATION (MULTIPLES)"
    else:
        intro = "ANALYSE DE LA RÉUNION\n\nCe rapport identifie les forces et faiblesses de cet échange et propose des actions concrètes d'amélioration.\n\n"
        pdf_header = "RAPPORT D'AMÉLIORATION"
    
    text_content = intro + text_content

    if "---JSON-STATS---" in text_content:
        parts = text_content.split("---JSON-STATS---")
        text_content = parts[0].strip()
        try:
            json_str = parts[1].strip()
            json_str = json_str.replace("```json", "").replace("```", "")
            kpi_data = json.loads(json_str)
        except Exception as e:
            print(f"Error parsing JSON KPIs: {e}")
            
    text_content = config.clean_text_glossary(text_content)
    
    return text_content, kpi_data, pdf_header

def generate_global_report(transcripts_dict, model):
    MAX_CHARS_PER_MEETING = 1200
    MAX_TOTAL_MEETINGS = 20
    
    history_blocks = []
    items = list(transcripts_dict.items())[:MAX_TOTAL_MEETINGS]
    for idx, (title, text) in enumerate(items):
        excerpt = text[:MAX_CHARS_PER_MEETING].strip()
        block = (
            f"--- RÉUNION #{idx+1} ---\n"
            f"Titre : {title}\n"
            f"Extrait :\n{excerpt}\n[...]"
        )
        history_blocks.append(block)
    history = "\n\n".join(history_blocks)

    prompt = f"""
Tu es un Senior Partner en Cabinet de Conseil Stratégique (McKinsey / BCG / Oliver Wyman), spécialisé en Excellence Commerciale et Performance des Équipes de Vente.
Ta mission est de produire un **AUDIT STRATÉGIQUE GLOBAL** à destination de la direction générale, basé sur l'historique complet des échanges commerciaux ci-dessous.

CONSIGNES RÉDACTIONNELLES :
- **Ne résume pas** chaque réunion individuellement. Identifie les schémas, tendances et dynamiques TRANSVERSES.
- **Ton** : Visionnaire, critique, factuel et constructif. Niveau Senior Partner — pas de formules creuses.
- **Profondeur** : Analyse les causes racines, pas seulement les symptômes.
- **Structure** : Respecte scrupuleusement les titres de sections ci-dessous.

# AUDIT STRATÉGIQUE GLOBAL D'ACTIVITÉ

## I. Dynamique Commerciale Globale
- Analyse de l'évolution de la qualité des leads, de la posture commerciale et de la fluidité des échanges au fil du temps.
- Y a-t-il une progression ou une régression observable entre les premières et les dernières interactions ?

## II. Cartographie des Objections Récurrentes
- Identifie les 3 à 5 freins clients qui reviennent systématiquement.
- Pour chacun, propose une réponse systémique à ancrer dans le discours commercial.

## III. Performance & Benchmark Interne
- Comparaison anonymisée des performances : engagement client, intensité du pain identifié, ratio écoute/parole.
- Qui (quel profil de réunion) performe le mieux et pourquoi ?

## IV. Opportunités de Croissance & Upsell
- Sur la base des besoins explicites et implicites exprimés, quels produits ou services devraient être davantage mis en avant ?
- Existe-t-il des signaux de cross-sell ou d'upsell non exploités ?

## V. Recommandations de Gouvernance
- Liste exactement **3 décisions majeures** que la direction doit prendre pour accélérer la croissance commerciale.
- Chaque recommandation doit être actionnnable à horizon 30/60/90 jours.

## VI. Analyse SWOT Globale
Synthèse stratégique en 4 quadrants basée sur l'ensemble des échanges :

### Forces (Internes — ce que l'équipe fait bien)
- Listez 3 à 5 points forts observés dans les échanges.

### Faiblesses (Internes — axes d'amélioration)
- Listez 3 à 5 lacunes récurrentes dans l'approche commerciale.

### Opportunités (Externes — facteurs favorables)
- Listez 3 à 5 opportunités marché ou client identifiées.

### Menaces (Externes — risques)
- Listez 3 à 5 risques ou signaux d'alerte à surveiller.

---

B. À la toute fin de ta réponse, génère un bloc JSON STRICT (sans markdown) séparé par la ligne : ---JSON-STATS---
Le JSON doit avoir EXACTEMENT ce format :
{{
  "global_sentiment_score": 75,
  "avg_pain_intensity": "Moyenne",
  "conversion_probability_trend": "En hausse",
  "common_topics": ["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"]
}}

Les valeurs autorisées :
- global_sentiment_score : entier de 0 à 100
- avg_pain_intensity : "Faible" | "Moyenne" | "Forte"
- conversion_probability_trend : "En hausse" | "Stable" | "En baisse"
- common_topics : liste de 5 sujets (strings courts)

HISTORIQUE DES ÉCHANGES ({len(transcripts_dict)} réunions analysées) :
{history}
"""

    try:
        response, used_model = config.generate_with_retry(
            model_name=model.model_name,
            content=prompt,
            generation_config={"temperature": 0.2}
        )
        raw = response.text
    except Exception as e:
        return (f"Erreur lors de la génération de l'audit global : {e}", None)

    kpi_data = None
    text_content = raw

    if "---JSON-STATS---" in raw:
        parts = raw.split("---JSON-STATS---")
        text_content = parts[0].strip()
        try:
            json_str = parts[1].strip()
            json_str = json_str.replace("```json", "").replace("```", "").strip()
            kpi_data = json.loads(json_str)
        except Exception as e:
            print(f"[global_report] Erreur parsing JSON KPIs: {e}")

    text_content = config.clean_text_glossary(text_content)
    return text_content, kpi_data

def generate_pro_minutes(report_text, model, titles=None):
    titles_str = ", ".join(titles) if titles else "Réunion commerciale"
    prompt = f"""
Tu es un expert en secrétariat de direction. Ta mission est de produire un **COMPTE RENDU FLASH**.
Objectif : Tout doit tenir sur une seule page PDF, très aéré.

STRUCTURE STRICTE :

# COMPTE RENDU DE RÉUNION
TITRE: [Titre court]
DATE: {time.strftime("%d/%m/%Y")}
LIEU: RABAT
ORGANISATEUR: Inspirigence Groupe
TYPE: Stratégique

## PARTICIPANTS
- Équipe Inspirigence : Consultant Senior
- Clients / Prospect : [Extraire les noms des clients du rapport source et des titres : {titles_str}]

## SYNTHÈSE DES DÉCISIONS
- **Décision 1** : [Détail majeur]
- **Décision 2** : [Détail majeur]

## ACTIONS À MENER
- Responsable | Détail de l'action | Échéance

---
CONSIGNES :
- **Équipe Inspirigence** : Écris TOUJOURS "Consultant Senior" uniquement dans cette section.
- **Clients / Prospect** : Liste les noms des clients/prospects trouvés dans le rapport ou les titres ({titles_str}).
- **Remplacer les exemples** : Remplace les lignes ci-dessus par les vraies données.
- **Dinstinction des rôles** : Monsef (Montacer) est TOUJOURS un client. Ne confonds pas les rôles et les noms. Ne liste que les NOMS dans les participants.
- **Pas de section 'Absents'** : Inutile dans ce format flash.
- **Ultra-Bref** : Limite-toi à 2 points MAX par section pour garantir une seule page.
- **Zéro blabla** : Pas d'introduction, pas de conclusion, pas de répétition des consignes.
- **Format** : Utilise uniquement le format pipe (|) pour les actions.

RAPPORT SOURCE :
{report_text}
"""

    try:
        response, _ = config.generate_with_retry(
            model_name=model.model_name,
            content=prompt,
            generation_config={"temperature": 0.1}
        )
        return config.clean_text_glossary(response.text)
    except Exception as e:
        return f"Erreur lors de la génération du compte rendu : {str(e)}"

def generate_followup_email(report_text, kpis, model):
    global_score = kpis.get("global_score", 0) if kpis else 0
    pain = kpis.get("pain_intensity", "Non spécifié") if kpis else "Non spécifié"
    
    prompt = f"""
    Tu es un expert en Copywriting B2B et Sales (emailing à froid et suivi).
    
    TA MISSION :
    Rédige un email de suivi de réunion ultra-performant pour ce prospect.
    L'objectif est d'obtenir une réponse ou de valider le Next Step.
    
    BASÉ SUR CE RAPPORT DE RÉUNION :
    {report_text}
    
    CONSIGNES DE STYLE (TRES IMPORTANT) :
    - Ton : Professionnel, direct, empathique mais pas "commercial lourd"
    - Structure :
        1. **Objet** : Kourt, percutant, intrigue (Ex: "Suite à notre échange", "Idée pour [Entreprise]", "Question sur [Pain]")
        2. **Accroche** : Rappel du contexte + validation du problème (Pain)
        3. **Value Prop** : Rappel rapide de la solution proposée (sans feature dumping)
        4. **Call to Action (CTA)** : Une question claire pour le Next Step (pas de "n'hésitez pas à revenir vers moi")
    
    - Ne mets PAS de placeholders [Nom] si tu peux le déduire du contexte, sinon laisse [Nom].
    - Sois bref : 150 mots maximum.
    """
    
    try:
        response, _ = config.generate_with_retry(
            model_name=model.model_name,
            content=prompt,
            generation_config={"temperature": 0.5}
        )
        return config.clean_text_glossary(response.text)
    except Exception as e:
        return f"Erreur lors de la génération de l'email : {str(e)}"

def extract_objections(transcript, model):
    prompt = f"""
    Tu es un expert en négociation commerciale et gestion des objections.
    
    TA MISSION :
    Analyse le transcript ci-dessous et identifie les 3 principales objections ou blocages (explicites ou implicites) soulevés par le prospect.
    Pour chaque objection, propose une réponse "Scriptée" idéale.
    
    TRANSCRIPT :
    {transcript[:25000]}
    
    FORMAT DE SORTIE (JSON STRICT) :
    [
      {{
        "objection": "Citation courte de l'objection ou du blocage",
        "type": "Prix" | "Concurrent" | "Timing" | "Autorité" | "Confiance" | "Besoin",
        "technique": "Nom de la technique (ex: Feel-Felt-Found, Isolation, Boomerang)",
        "reponse": "Script de réponse suggéré (1-2 phrases percutantes)"
      }}
    ]
    
    Si aucune objection n'est trouvée, renvoie une liste vide [].
    Ne mets PAS de markdown (```json). Renvoie juste le JSON brut.
    """
    
    try:
        response, _ = config.generate_with_retry(
            model_name=model.model_name,
            content=prompt,
            generation_config={"temperature": 0.0}
        )
        text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(text)
    except Exception as e:
        print(f"Erreur extraction objections: {e}")
        return []


def semantic_search(query, selected_indices, model):
    """Search for information across selected meetings using AI"""
    meetings = utils_data.load_meetings()
    
    # Build context from selected meetings
    search_context = []
    for idx in selected_indices:
        meeting = meetings[idx]
        title = meeting.get("title", meeting.get("filename", "Sans titre"))
        segments = meeting.get("segments", [])
        
        for segment in segments:
            search_context.append({
                "meeting_title": title,
                "meeting_index": idx,
                "start_time": segment.get("start", 0),
                "end_time": segment.get("end", 0),
                "text": segment.get("text", "")
            })
    
    if not search_context:
        return None
    
    # Create prompt for AI search
    context_text = "\n\n".join([
        f"[{item['meeting_title']} - {int(item['start_time']//60)}:{int(item['start_time']%60):02d}] {item['text']}"
        for item in search_context
    ])
    
    prompt = f"""Tu es un assistant de recherche intelligent. L'utilisateur cherche des informations dans des transcriptions de réunions.

QUESTION DE L'UTILISATEUR :
{query}

TRANSCRIPTIONS DISPONIBLES :
{context_text}

INSTRUCTIONS CRITIQUES :
1. Trouve les segments les PLUS PERTINENTS qui répondent à la question
2. Retourne UNIQUEMENT un JSON valide, sans texte avant ou après
3. Format JSON EXACT (respecte les guillemets doubles) :

{{
  "results": [
    {{
      "meeting_title": "titre du meeting",
      "timestamp": "MM:SS",
      "text": "extrait pertinent",
      "relevance": 95
    }}
  ],
  "summary": "Réponse courte en 2-3 phrases"
}}

4. Maximum 5 résultats, triés par pertinence décroissante
5. Si aucune info pertinente : results vide avec summary expliquant pourquoi
6. N'ajoute AUCUN texte en dehors du JSON
"""
    
    try:
        max_retries = 3
        retry_delay = 15
        last_response = None

        for attempt in range(max_retries):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.0, 
                        "max_output_tokens": 4096,
                        "response_mime_type": "application/json"
                    }
                )
                last_response = response
                break
            except ResourceExhausted:
                if attempt < max_retries - 1:
                    wait = retry_delay * (2 ** attempt)
                    print(f"[semantic_search] Quota 429 — attente {wait}s (tentative {attempt+1}/{max_retries})")
                    time.sleep(wait)
                    continue
                else:
                    return {
                        "results": [],
                        "summary": "Quota API dépassé (429). Veuillez patienter une minute avant de réessayer."
                    }

        if last_response is None:
            return {"results": [], "summary": "Aucune réponse obtenue après plusieurs tentatives."}

        result_text = last_response.text.strip()

        # Clean markdown code blocks if present
        if "```" in result_text:
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            else:
                result_text = result_text.replace("```json", "").replace("```", "").strip()

        search_results = json.loads(result_text)
        return search_results
    except json.JSONDecodeError:
        return {
            "results": [],
            "summary": "Erreur de format dans la réponse de l'IA. Veuillez réessayer."
        }
    except Exception as e:
        return {
            "results": [],
            "summary": f"Erreur lors de la recherche: {str(e)}"
        }


def generate_topic_explanation(topic, selected_indices, model):
    """Generate an explanatory report about a specific topic from meeting transcripts"""
    meetings = utils_data.load_meetings()
    
    # Gather all relevant content from selected meetings
    all_content = []
    for idx in selected_indices:
        meeting = meetings[idx]
        title = meeting.get("title", meeting.get("filename", "Sans titre"))
        transcript = meeting.get("transcript", "")
        if not transcript and "segments" in meeting:
            transcript = "\n".join([s.get("text", "") for s in meeting["segments"]])
        all_content.append(f"### Meeting: {title}\n{transcript}")
    
    combined_content = "\n\n".join(all_content)
    
    prompt = f"""Tu es un expert en documentation technique et pédagogique.

Ta mission est de créer un **rapport explicatif complet** sur le sujet suivant :
**SUJET : {topic}**

En te basant UNIQUEMENT sur les informations contenues dans les transcriptions de réunions ci-dessous.

TRANSCRIPTIONS DES RÉUNIONS :
{combined_content}

INSTRUCTIONS :
1. Crée un rapport structuré et professionnel expliquant **comment fonctionne {topic}**
2. Utilise UNIQUEMENT les informations présentes dans les transcriptions
3. Structure ton rapport avec les sections suivantes :

# 📘 Guide Complet : {topic}

## 🎯 Vue d'ensemble
(Résumé en 2-3 phrases de ce qu'est {topic})

## ⚙️ Fonctionnement
(Explication détaillée du fonctionnement basée sur les discussions)

## ✨ Fonctionnalités Principales
(Liste des fonctionnalités mentionnées avec descriptions)

## 💡 Cas d'Usage
(Exemples concrets d'utilisation mentionnés dans les meetings)

## 🔧 Configuration/Mise en Place
(Si des informations de configuration ont été discutées)

## ⚠️ Points d'Attention
(Limitations, difficultés ou points importants mentionnés)

## 📊 Avantages
(Bénéfices et points forts discutés)

4. Utilise le **gras** pour les termes importants
5. Sois précis et factuel
6. Si une section n'a pas d'information dans les transcriptions, écris "*Informations non disponibles dans les meetings analysés*"
7. Cite des extraits pertinents entre guillemets quand c'est utile
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erreur lors de la génération du rapport : {str(e)}"
