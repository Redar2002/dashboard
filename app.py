import os
import json
import streamlit as st
import config
from fpdf import FPDF
from utils_topic_pdf import create_topic_pdf
import time
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable, InternalServerError, DeadlineExceeded
import utils_audio
import utils_theme


# MODEL initialization moved to sidebar for dynamic configuration


import utils_data


# -------------------------
# Utils
# -------------------------

# Redirection of data functions to shared utility
load_meetings = utils_data.load_meetings
save_meetings = utils_data.save_meetings


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
    
    # Simple parsing to separate Text from JSON
    text_content = response.text
    kpi_data = None
    
    # Prepend the requested introduction paragraph
    if is_plural:
        intro = f"ANALYSE DES RÉUNIONS\n\nCe rapport identifie les forces et faiblesses de ces échanges et propose des actions concrètes d’amélioration.\n\n"
        pdf_header = "RAPPORT D'AMÉLIORATION (MULTIPLES)"
    else:
        intro = f"ANALYSE DE LA RÉUNION\n\nCe rapport identifie les forces et faiblesses de cet échange et propose des actions concrètes d’amélioration.\n\n"
        pdf_header = "RAPPORT D'AMÉLIORATION"
    
    # Actually, let's just properly format it.
    text_content = intro + text_content

    if "---JSON-STATS---" in text_content:
        parts = text_content.split("---JSON-STATS---")
        text_content = parts[0].strip()
        try:
            json_str = parts[1].strip()
            # Clean potential markdown code blocks if AI puts them
            json_str = json_str.replace("```json", "").replace("```", "")
            kpi_data = json.loads(json_str)
        except Exception as e:
            print(f"Error parsing JSON KPIs: {e}")
            
    # Apply glossary cleaning
    text_content = config.clean_text_glossary(text_content)
    
    return text_content, kpi_data, pdf_header


def generate_global_report(transcripts_dict, model):
    """Generates a high-level Strategic Audit of all combined meetings.
    Returns (text_content, kpi_data) where kpi_data may be None on parsing failure.
    """
    
    # --- Build a rich, well-structured history for the prompt ---
    # Limite : max 1200 caractères par réunion pour éviter le dépassement de tokens Gemini
    MAX_CHARS_PER_MEETING = 1200
    MAX_TOTAL_MEETINGS = 20  # Ne pas dépasser 20 réunions dans un seul prompt
    
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

    # --- Parse text + JSON-STATS ---
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
    """Generates a structured formal Minutes of Meeting (Compte Rendu Pro) for the HubSpot Design"""
    
    titles_str = ", ".join(titles) if titles else "Réunion commerciale"
    prompt = f"""
Tu es un expert en secrétariat de direction. Ta mission est de produire un **COMPTE RENDU DE RÉUNION** formel.
STRUCTURE STRICTE À RESPECTER (pour parsing PDF) :

# COMPTE RENDU DE RÉUNION
TITRE: [Nom du projet ou titre de la réunion]
DATE: {time.strftime("%d/%m/%Y")}
LIEU: RABAT

ORGANISATEUR: Inspirigence Groupe
TYPE: Réunion commerciale / Stratégique
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
    """Generates a high-conversion follow-up email based on the report"""
    
    # Extract key info safely
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
    """Extracts objections and provides rebuttal scripts"""
    
    prompt = f"""
    Tu es un expert en négociation commerciale et gestion des objections.
    
    TA MISSION :
    Analyse le transcript ci-dessous et identifie les 3 principales objections ou blocages (explicites ou implicites) soulevés par le prospect.
    Pour chaque objection, propose une réponse "Scriptée" idéale.
    
    TRANSCRIPT :
    {transcript[:25000]}  # Limite de tokens
    
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




def save_kpis_to_meeting(meeting_index, kpis):
    """Save KPIs to a specific meeting in meetings.json"""
    from datetime import datetime
    
    meetings = load_meetings()
    if 0 <= meeting_index < len(meetings):
        if kpis:
            meetings[meeting_index]["kpis"] = kpis.copy()
            meetings[meeting_index]["kpis"]["analyzed_at"] = datetime.now().isoformat()
            save_meetings(meetings)
            return True
    return False



def semantic_search(query, selected_indices):
    """Search for information across selected meetings using AI"""
    meetings = load_meetings()
    
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
        for item in search_context[:100]  # Limit to first 100 segments to avoid token limits
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
        response, _ = config.generate_with_retry(
            model_name=MODEL.model_name,
            content=prompt,
            generation_config={"temperature": 0.0},
            request_options={"timeout": 600}
        )
        result_text = response.text.strip()
        
        if "```" in result_text:
            import re
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            else:
                result_text = result_text.replace("```json", "").replace("```", "").strip()
        
        search_results = json.loads(result_text)
        return search_results

    except Exception as e:
        return {"results": [], "summary": f"Erreur de recherche : {str(e)}"}
    
    return {"results": [], "summary": "La recherche a échoué après plusieurs tentatives."}


def generate_topic_explanation(topic, selected_indices):
    """Generate an explanatory report about a specific topic from meeting transcripts"""
    meetings = load_meetings()
    
    # Gather all relevant content from selected meetings
    all_content = []
    for idx in selected_indices:
        meeting = meetings[idx]
        title = meeting.get("title", meeting.get("filename", "Sans titre"))
        transcript = meeting.get("transcript", "")
        all_content.append(f"### Meeting: {title}\n{transcript}")
    
    combined_content = "\n\n".join(all_content)
    
    is_plural = len(selected_indices) > 1
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

# 📘 {"Guides Complets" if is_plural else "Guide Complet"} : {topic}

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
6. Si une section n'a pas d'information dans les transcriptions, écris "*Informations non disponibles dans les {"meetings analysés" if is_plural else "meeting analysé"}*"
7. Cite des extraits pertinents entre guillemets quand c'est utile
"""
    
    try:
        response, _ = config.generate_with_retry(
            model_name=MODEL.model_name,
            content=prompt,
            generation_config={"temperature": 0.3},
            request_options={"timeout": 600}
        )
        return response.text
    except Exception as e:
        return f"Erreur lors de la génération du rapport : {str(e)}"


# -------------------------
# UI
# -------------------------

st.set_page_config(page_title="Meeting Intelligence", page_icon="📊", layout="wide")

# ── Logo & Title Styling ───────────────────────────────────────────────
st.markdown("""
<style>
h1 {
    background: linear-gradient(90deg, #8B5CF6, #D946EF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 10px;
}
h2 {
    color: #A78BFA !important;
}
h3 {
    color: #C084FC !important;
}
/* Align sidebar "Home" icon correctly */
[data-testid="stSidebarNavItems"] li:first-child a {
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    flex-direction: row !important;
}
[data-testid="stSidebarNavItems"] li:first-child a span:last-child {
    display: inline-flex !important;
    align-items: center !important;
}
[data-testid="stSidebarNavItems"] li:first-child a span:last-child::before {
    content: "🏠";
    margin-right: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

import base64
try:
    with open("logo_inspirigence.jpg", "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(f"""
        <style>
        [data-testid="stSidebarNav"]::before {{
            content: "";
            display: block;
            margin: 20px auto;
            width: 80%;
            height: 120px;
            background-image: url("data:image/jpeg;base64,{data}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
    """, unsafe_allow_html=True)
except Exception:
    pass

# ── Hero Header ───────────────────────────────────────────────
st.title("Meeting Intelligence")
st.caption("Analyse stratégique propulsée par Gemini AI — Insights actionables en temps réel")

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.markdown('<div style="color: #94A3B8; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 15px; border-bottom: 1px solid #334155; padding-bottom: 8px;">CONFIGURATION</div>', unsafe_allow_html=True)
    
    utils_theme.render_theme_toggle()
    
    # Model Selection
    QUOTA_LABELS = {
        "models/gemini-2.0-flash":      "gemini-2.0-flash      ✅ RECOMMANDÉ (Stable)",
        "models/gemini-flash-latest":   "gemini-flash-latest   ⚡ Switch ici si 429",
        "models/gemini-pro-latest":     "gemini-pro-latest     🔬 Switch ici si 429",
        "models/gemini-2.5-flash":      "gemini-2.5-flash      ⚠️ QUOTA LIMITÉ (20/j)",
    }
    try:
        available_models = config.list_available_models()
        if not available_models:
            available_models = ["models/gemini-flash-latest"]

        # Default to gemini-2.0-flash-lite for free tier safety 
        default_idx = 0
        for i, m in enumerate(available_models):
            if "flash-lite" in m.lower():
                default_idx = i
                break

        labels = [QUOTA_LABELS.get(m, m) for m in available_models]
        selected_label = st.selectbox("🤖 Choisir le modèle", labels, index=default_idx)
        # Map label back to model id
        selected_model = available_models[labels.index(selected_label)]

    except Exception as e:
        st.error(f"Erreur chargement modèles: {e}")
        selected_model = "models/gemini-2.0-flash-lite"

    # Initialize Model with selection
    try:
        MODEL = config.configure(model_name=selected_model)
        
        # FINAL VERIFICATION BADGE
        clean_model_name = MODEL.model_name.replace('models/', '')
        st.markdown(f'<div style="border: 1px solid #8B5CF6; border-radius: 6px; padding: 8px 12px; font-size: 0.85rem; margin-top: 10px; display: flex; align-items: center; gap: 8px;"><div style="width: 8px; height: 8px; border-radius: 50%; background-color: #10B981;"></div><span>Actif: <strong>{clean_model_name}</strong></span></div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erreur config model: {e}")
        MODEL = None

    st.markdown("---")

    # ── Bouton Test API ──────────────────────────────────────────
    if MODEL and st.button("🔌 Tester l'API", use_container_width=True, type="primary"):
        with st.spinner("Test en cours..."):
            try:
                test_response = MODEL.generate_content(
                    "Réponds uniquement par: OK",
                    generation_config={"max_output_tokens": 5}
                )
                st.markdown("""
                    <div style="background:#064e3b; border-left:4px solid #10b981;
                                padding:10px; border-radius:8px; margin-top:8px;">
                        <p style="margin:0; color:#6ee7b7; font-weight:bold;">✅ API opérationnelle</p>
                        <p style="margin:0; font-size:x-small; color:#a7f3d0;">
                            Quota disponible — vous pouvez générer des rapports.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                err = str(e)
                if "429" in err or "ResourceExhausted" in err:
                    st.markdown("""
                        <div style="background:#450a0a; border-left:4px solid #ef4444;
                                    padding:10px; border-radius:8px; margin-top:8px;">
                            <p style="margin:0; color:#fca5a5; font-weight:bold;">🔴 Quota épuisé (429)</p>
                            <p style="margin:0; font-size:x-small; color:#fecaca;">
                                Réessayez demain après 00h00 UTC ou activez la facturation.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                elif "404" in err or "NotFound" in err:
                    st.markdown("""
                        <div style="background:#431407; border-left:4px solid #f97316;
                                    padding:10px; border-radius:8px; margin-top:8px;">
                            <p style="margin:0; color:#fdba74; font-weight:bold;">⚠️ Modèle introuvable (404)</p>
                            <p style="margin:0; font-size:x-small; color:#fed7aa;">
                                Ce modèle n'est pas disponible. Changez de modèle.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"❌ Erreur inattendue : {err[:120]}")

    st.markdown("---")
    st.markdown("""<div style="margin-top: 30px; color: #94A3B8; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 15px; border-bottom: 1px solid #334155; padding-bottom: 8px;">CONSOLE D'ADMINISTRATION</div>""", unsafe_allow_html=True)
    st.caption("Générez un audit stratégique global consolidant l'ensemble de vos réunions.")
    
    if MODEL and st.button("📈 Générer Audit Global Strategique", use_container_width=True, type="primary"):
        all_meetings = load_meetings()
        if not all_meetings:
            st.error("Aucune donnée disponible.")
        else:
            with st.spinner(f"Analyse de {len(all_meetings)} réunions en cours..."):
                transcripts_dict = {
                    m.get('title', f"Meeting_{idx}"): m.get('transcript', '')
                    for idx, m in enumerate(all_meetings)
                }
                global_audit_text, global_kpis = generate_global_report(transcripts_dict, MODEL)
                st.session_state.global_audit = global_audit_text
                st.session_state.global_kpis = global_kpis
                import utils_pdf
                st.session_state.global_pdf_bytes = utils_pdf.create_pdf(
                    global_audit_text, title="AUDIT STRATEGIQUE GLOBAL"
                )
                st.success(f"✅ Audit Global prêt ({len(all_meetings)} réunions analysées) !")

    # --- KPI Dashboard (affiché après génération) ---
    if "global_kpis" in st.session_state and st.session_state.global_kpis:
        kpis = st.session_state.global_kpis
        st.markdown("---")
        trend = kpis.get('conversion_probability_trend', 'N/A')
        trend_icon = "📈" if trend == "En hausse" else ("📉" if trend == "En baisse" else "➡️")
        pain_colors = {"Forte": "#EF4444", "Moyenne": "#F59E0B", "Faible": "#10B981"}
        pain_color = pain_colors.get(kpis.get('avg_pain_intensity', ''), "#8B5CF6")
        kc1, kc2, kc3, kc4 = st.columns(4)
        with kc1:
            st.metric("Sentiment Global", f"{kpis.get('global_score', 'N/A')}/100")
        with kc2:
            st.metric("Intensité Douleur", kpis.get('avg_pain_intensity', 'N/A'))
        with kc3:
            st.metric("Tendance Conversion", trend)
        with kc4:
            st.metric("Réunions Analysées", len(load_meetings()))
        topics = kpis.get('common_topics', [])
        if topics:
            tags_html = "".join([
                f'<span style="background:rgba(139,92,246,0.15);border:1px solid rgba(139,92,246,0.35);'
                f'border-radius:20px;padding:3px 12px;color:#A78BFA;font-size:0.8rem;margin:3px;display:inline-block;">'
                f'{t}</span>'
                for t in topics[:5]
            ])
            st.markdown(
                f'<div style="margin:1rem 0;"><span style="color:#64748B;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.1em;">'
                f'Top Sujets</span><br/><div style="margin-top:0.5rem;">{tags_html}</div></div>',
                unsafe_allow_html=True
            )
        st.markdown("---")

    if "global_audit" in st.session_state:
        st.download_button(
            "📄 Télécharger l'Audit (PDF)",
            st.session_state.global_pdf_bytes,
            "Audit_Global_Strategique.pdf",
            "application/pdf",
            use_container_width=True
        )
        if st.button("🗑️ Effacer l'Audit", type="primary"):
            del st.session_state.global_audit
            if "global_kpis" in st.session_state:
                del st.session_state.global_kpis
            del st.session_state.global_pdf_bytes
            st.rerun()

    st.markdown("---")



meetings = load_meetings()

st.header("🎤 Nouvelle Réunion")
st.caption("Uploadez un audio ou vidéo — transcription et analyse automatiques via Gemini AI")

uploaded_file = st.file_uploader(
    "Sélectionnez un fichier (MP3, WAV, M4A, MP4)", 
    type=['mp3', 'wav', 'm4a', 'aac', 'mp4', 'mov', 'avi']
)

col1, col2 = st.columns([3, 1])
with col1:
    meeting_title = st.text_input("Titre de la réunion (facultatif)", placeholder="Ex: Démo CRM - Client X")
with col2:
    lang_choice = st.selectbox("Langue fr/en", ["Français", "Anglais", "Mixte"])

if st.button("🚀 Lancer la Transcription", use_container_width=True, type="primary"):
    if not uploaded_file:
        st.error("Veuillez sélectionner un fichier avant de lancer la transcription.")
    elif not MODEL:
        st.error("Modèle Gemini non configuré. Veuillez vérifier la sidebar.")
    else:
        with st.spinner(f"Traitement de {uploaded_file.name} en cours... (Cela peut prendre plusieurs minutes)"):
            try:
                import time
                import os
                from datetime import datetime
                import utils_transcription
                
                # Sauvegarde locale temporaire
                os.makedirs("tmp", exist_ok=True)
                tmp_filepath = os.path.join("tmp", f"upload_{int(time.time())}_{uploaded_file.name}")
                
                with open(tmp_filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                    
                # Appel de la fonction de transcription et nettoyage
                transcription_text, transcription_clean = utils_transcription.transcribe_and_clean_audio(
                    filepath=tmp_filepath, 
                    model=MODEL, 
                    lang_choice=lang_choice
                )
                
                # Extraction des segments et du texte pur
                segments, pure_text = utils_transcription.parse_transcript_to_segments(transcription_text)
                segments_clean, pure_text_clean = utils_transcription.parse_transcript_to_segments(transcription_clean)
                
                # Stockage temporaire dans la session pour validation manuelle
                st.session_state["pending_meeting"] = {
                    "title": meeting_title if meeting_title else uploaded_file.name,
                    "meeting_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
                    "filename": uploaded_file.name,
                    "segments": segments,
                    "transcript": pure_text,
                    "transcript_clean": pure_text_clean,
                    "segments_clean": segments_clean
                }
                
                st.session_state["transcription_finished"] = True
                
                # Suppression du fichier temp local
                os.remove(tmp_filepath)
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la transcription : {e}")

# Zone de confirmation de sauvegarde (hors du bloc bouton pour persister)
if "pending_meeting" in st.session_state:
    st.markdown("---")
    st.info(f"📍 **Transcription prête pour : {st.session_state['pending_meeting']['title']}**")
    
    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("💾 Enregistrer dans la base de données", type="primary", use_container_width=True):
            meetings = load_meetings()
            meetings.insert(0, st.session_state["pending_meeting"])
            save_meetings(meetings)
            st.success("✅ Meeting enregistré avec succès !")
            del st.session_state["pending_meeting"]
            if "transcription_finished" in st.session_state:
                del st.session_state["transcription_finished"]
            st.rerun()
            
    with col_cancel:
        if st.button("🗑️ Annuler / Recommencer", use_container_width=True):
            del st.session_state["pending_meeting"]
            if "transcription_finished" in st.session_state:
                del st.session_state["transcription_finished"]
            st.rerun()

    with st.expander("👁️ Voir la transcription nettoyée avant enregistrement", expanded=True):
        st.text_area("Texte propre", st.session_state["pending_meeting"]["transcript_clean"], height=400)

                
st.markdown("---")

st.header("📂 Meetings Enregistrés")
st.caption(f"Base de données — {len(meetings)} réunion(s) disponible(s)")


if not meetings:
    st.info("Aucun meeting disponible")
else:

    labels = [
        f"{i} - {m.get('title', m.get('filename', 'Sans titre'))}"
        for i, m in enumerate(meetings)
    ]

    selected = st.multiselect(
        "Sélectionne un ou plusieurs meetings",
        labels
    )
    



    if st.button("📊 Générer rapport d'amélioration", type="primary"):

        if len(selected) == 0:
            st.warning("Sélectionne au moins un meeting")
        else:
            selected_indices = [int(i.split(" - ")[0]) for i in selected]
            transcripts = [
                meetings[idx]["transcript"]
                for idx in selected_indices
            ]

            with st.spinner("Analyse en cours..."):
                try:
                    # Store text and kpi in session state
                    report_text, kpis, pdf_header = generate_improvement_report(transcripts, MODEL)
                    st.session_state.improvement_report = report_text
                    st.session_state.kpis = kpis
                    st.session_state.pdf_header = pdf_header
                    st.session_state.selected_indices = selected_indices
                except ResourceExhausted:
                    st.error(f"❌ Quota API épuisé pour le modèle `{MODEL.model_name}`. Veuillez patienter une minute ou passer à un modèle avec des quotas plus élevés (Gemini 1.5 Flash).")
                except Exception as e:
                    st.error(f"❌ Une erreur est survenue lors de l'analyse avec `{MODEL.model_name}` : {e}")
            
            # Clear old Pro report when a new analysis is started
            if "pro_report" in st.session_state:
                del st.session_state.pro_report
            if "pro_pdf_bytes" in st.session_state:
                del st.session_state.pro_pdf_bytes
            if "pro_audio_bytes" in st.session_state:
                del st.session_state.pro_audio_bytes



    # Display results if available
    if "improvement_report" in st.session_state and st.session_state.improvement_report:
        
        st.markdown("### 📝 Option : Compte Rendu Formel")
        st.caption("Générez un document formel (Minutes) basé sur l'analyse stratégique.")
        if st.button("📝 Générer le Compte Rendu Pro (Formel)", use_container_width=True, key="btn_gen_pro_re_fixed", type="primary"):
            report_text = st.session_state.improvement_report
            with st.spinner("Rédaction en cours..."):
                try:
                    selected_indices = [int(i.split(" - ")[0]) for i in selected]
                    selected_meetings = [meetings[idx] for idx in selected_indices]
                    titles = [m.get("title", "Sans titre") for m in selected_meetings]
                    pro_minutes = generate_pro_minutes(report_text, MODEL, titles=titles)
                    st.session_state.pro_report = pro_minutes
                    st.session_state.pro_pdf_header = "COMPTE RENDU DE RÉUNION"
                    import utils_pdf
                    st.session_state.pro_pdf_bytes = utils_pdf.create_pdf(pro_minutes, title=st.session_state.pro_pdf_header)
                    st.success("✅ Compte rendu prêt !")
                except Exception as e:
                    st.error(f"❌ Erreur : {e}")
        
        # Immediate display of controls if report exists
        if "pro_report" in st.session_state:
            st.markdown("---")
            st.markdown("### 📝 Édition & Téléchargement")
            st.info("💡 Modifiez le texte ci-dessous puis cliquez sur 'Enregistrer' pour mettre à jour le PDF.")
            
            edited_report = st.text_area("Validation & Modification du contenu", st.session_state.pro_report, height=400, key="pro_report_editor_main")
            
            if st.button("💾 Enregistrer les modifications", use_container_width=True, key="save_pro_edits_main", type="primary"):
                st.session_state.pro_report = edited_report
                import utils_pdf
                st.session_state.pro_pdf_bytes = utils_pdf.create_pdf(edited_report, title=st.session_state.pro_pdf_header)
                st.success("✅ PDF mis à jour avec vos modifications !")
                st.rerun()

            c1, c2 = st.columns(2)
            with c1:
                if "pro_pdf_bytes" in st.session_state:
                    st.download_button(
                        label="📄 Télécharger le Compte Rendu (PDF)",
                        data=st.session_state.pro_pdf_bytes,
                        file_name="compte_rendu_pro.pdf",
                        mime="application/pdf",
                        key="dl_pro_main",
                        use_container_width=True
                    )
            with c2:
                if st.button("🔊 Préparer la version audio", key="gen_audio_pro_main", use_container_width=True, type="primary"):
                    with st.spinner("Génération..."):
                        audio_raw = utils_audio.text_to_speech(st.session_state.pro_report)
                        if audio_raw:
                            st.session_state.pro_audio_bytes = audio_raw
            
            if "pro_audio_bytes" in st.session_state:
                st.audio(st.session_state.pro_audio_bytes, format="audio/mp3")
        
        st.markdown("---")
        
        # Display KPIs Dashboard if available
        if "kpis" in st.session_state and st.session_state.kpis:
            kpis = st.session_state.kpis

            st.header("🎯 Tableau de Bord de Performance")
            st.caption("KPIs extraits par l'IA depuis l'analyse de la réunion")

            # Top row KPI cards
            pain_colors = {"Forte": "#EF4444", "Moyenne": "#F59E0B", "Faible": "#10B981"}
            listen_val = kpis.get('listen_ratio_client', 0)
            listen_color = "#10B981" if listen_val >= 50 else ("#F59E0B" if listen_val >= 30 else "#EF4444")
            score_val = kpis.get('global_score', 0)
            score_color = "#10B981" if score_val >= 70 else ("#F59E0B" if score_val >= 45 else "#EF4444")
            pain_color = pain_colors.get(kpis.get('pain_intensity', ''), "#8B5CF6")

            k1, k2, k3 = st.columns(3)
            with k1:
                st.metric("Score Global", f"{score_val}/100")
            with k2:
                st.metric("Douleur Client", kpis.get('pain_intensity', 'N/A'))
            with k3:
                st.metric("Ratio Écoute", f"{listen_val}%")

            st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

            # Phase Alignment — custom colored bars
            phases = kpis.get("phases_alignment", {})
            if phases:
                st.subheader("Alignement des Phases (1–5)")
                for phase, score in phases.items():
                    st.write(f"**{phase}** : {score}/5")
                    st.progress(int(score) / 5.0)

            st.markdown("---")

        st.text_area("Rapport d'amélioration", st.session_state.improvement_report, height=450)
        
        # PDF Download only
        try:
            import utils_pdf
            # Append KPIs to PDF text for completeness
            pdf_text = st.session_state.improvement_report
            if "kpis" in st.session_state and st.session_state.kpis:
                 k = st.session_state.kpis
                 pdf_text = f"SCORE GLOBAL: {k.get('global_score')}/100\n\n" + pdf_text
                 
            pdf_bytes = utils_pdf.create_pdf(pdf_text, title=st.session_state.get("pdf_header"))
            st.download_button(
                label="📄 Télécharger en PDF",
                data=pdf_bytes,
                file_name="rapport_amelioration.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Erreur PDF: {e}")

        st.markdown("---")

    # Follow-up Email section below
    if "improvement_report" in st.session_state and st.session_state.improvement_report:
        st.caption("Générez un email de suivi prêt à envoyer, basé sur l'analyse de ce meeting.")
        
        if st.button("✨ Générer l'Email de Suivi", type="primary"):
            with st.spinner("Rédaction de l'email en cours..."):
                try:
                    email_draft = generate_followup_email(
                        st.session_state.improvement_report, 
                        st.session_state.kpis, 
                        MODEL
                    )
                    st.session_state.email_draft = email_draft
                except ResourceExhausted:
                    st.error("❌ Quota API épuisé. Impossible de générer l'email pour le moment.")
                except Exception as e:
                    st.error(f"❌ Erreur : {e}")
        
        if "email_draft" in st.session_state:
            st.text_area("Brouillon d'Email (Copier/Coller)", st.session_state.email_draft, height=250)
            st.info("💡 Astuce Pro : Personnalisez toujours la première phrase avant d'envoyer !")

        st.markdown("---")

        # ⚠️ Objection Extractor
        st.markdown("### ⚠️ Analyse des Blocages & Objections (Beta)")
        st.caption("Détection automatique des freins clients et suggestions de réponses.")

        if st.button("🔍 Analyser les Objections", type="primary"):
            with st.spinner("Analyse approfondie des objections..."):
                # Reconstruct full transcript from selected meetings used for report
                # Note: improvement_report uses 'transcripts' list which isn't stored in session_state, 
                # but we stored 'selected_indices'.
                if "selected_indices" in st.session_state:
                    try:
                        full_transcript = ""
                        for idx in st.session_state.selected_indices:
                            full_transcript += meetings[idx].get("transcript", "") + "\n\n"
                        
                        objections = extract_objections(full_transcript, MODEL)
                        st.session_state.objections = objections
                    except ResourceExhausted:
                        st.error("❌ Quota API épuisé. Impossible d'analyser les objections pour le moment.")
                    except Exception as e:
                        st.error(f"❌ Erreur : {e}")
                else:
                    st.error("Impossible de récupérer les transcripts. Veuillez régénérer le rapport.")

        if "objections" in st.session_state and st.session_state.objections:
            for obj in st.session_state.objections:
                st.markdown(f"**{obj.get('type')}** ({obj.get('technique')})")
                st.info(f"\"{obj.get('objection')}\"")
                st.success(f"Réponse : {obj.get('reponse')}")
        elif "objections" in st.session_state:
            st.success("✅ Aucune objection majeure détectée par l'IA.")



