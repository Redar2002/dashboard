import os
import json
import streamlit as st
import config
from fpdf import FPDF
from utils_topic_pdf import create_topic_pdf
import time
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable, InternalServerError, DeadlineExceeded
import utils_audio
import utils_sql
import utils_ai_structurer
import utils_auth
import utils_data

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION DE LA PAGE
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Meeting Intelligence", 
    page_icon="🎙️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════
# CSS PREMIUM - DESIGN SAAS MODERNE
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* GLOBAL */
    /* ─────────────────────────────────────────────────────────────────── */
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        background-color: #F8FAFC;
        padding: 2rem 1rem;
    }
    
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* HERO SECTION */
    /* ─────────────────────────────────────────────────────────────────── */
    
    .hero-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        margin-bottom: 2.5rem;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 24px rgba(124, 58, 237, 0.08);
        text-align: center;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #7C3AED 0%, #D946EF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #475569;
        font-weight: 400;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    .hero-tagline {
        font-size: 1.5rem;
        color: #1E293B;
        font-weight: 600;
        margin-top: 1rem;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #7C3AED 0%, #D946EF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* FEATURE CARDS */
    /* ─────────────────────────────────────────────────────────────────── */
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2.5rem;
    }
    
    .feature-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 1.8rem;
        border: 1px solid #E5E7EB;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(124, 58, 237, 0.15);
        border-color: #D946EF;
    }
    
    .feature-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #8B5CF6 0%, #D946EF 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        color: #64748B;
        line-height: 1.6;
    }
    
    @media (max-width: 768px) {
        .feature-grid {
            grid-template-columns: 1fr !important;
            justify-items: center !important;
        }
        .feature-card {
            text-align: center !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            width: 100% !important;
            max-width: 350px !important;
            margin: 0 auto !important;
        }
        .feature-icon {
            margin: 0 auto 1rem auto !important;
        }
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* SECTION CARDS */
    /* ─────────────────────────────────────────────────────────────────── */
    
    .section-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid #E5E7EB;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #7C3AED;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .section-caption {
        font-size: 0.9rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* BADGES */
    /* ─────────────────────────────────────────────────────────────────── */
    
    .badge {
        display: inline-block;
        padding: 0.4rem 0.9rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    .badge-primary {
        background: linear-gradient(135deg, #8B5CF6 0%, #D946EF 100%);
        color: white;
    }
    
    .badge-count {
        background: rgba(124, 58, 237, 0.1);
        color: #7C3AED;
        border: 1px solid rgba(124, 58, 237, 0.2);
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* STATUS MESSAGES */
    /* ─────────────────────────────────────────────────────────────────── */
    
    .status-success {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
    }
    
    .status-success-title {
        color: #059669;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    .status-success-text {
        color: #047857;
        font-size: 0.9rem;
    }
    
    .status-error {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* SIDEBAR STYLING */
    /* ─────────────────────────────────────────────────────────────────── */
    
    [data-testid="stSidebar"] {
        background-color: #0F172A;
    }
    
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #F8FAFC !important;
    }
    
    /* Add emoji to app page in sidebar */
    [data-testid="stSidebarNav"] li:first-child a::before {
        content: "🏠";
        margin-right: 0px !important;
    }
    
    .sidebar-section-title {
        color: #F1F5F9 !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        padding-left: 0.25rem !important;
        opacity: 0.8 !important;
    }
    
    /* User Card in Sidebar */
    .user-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #475569;
    }
    
    .user-name {
        color: #F8FAFC !important;
        font-weight: 700;
        font-size: 1rem;
    }
    
    .user-role {
        color: #94A3B8 !important;
        font-size: 0.8rem;
    }
    
    /* Sidebar selectbox */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 12px !important;
        color: #F1F5F9 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox svg {
        fill: #94A3B8 !important;
    }
    
    /* Model Status Badge */
    .model-status {
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        background: rgba(16, 185, 129, 0.15) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        padding: 4px 10px !important;
        border-radius: 20px !important;
        margin-top: 0.5rem !important;
    }
    
    .status-dot {
        width: 6px !important;
        height: 6px !important;
        border-radius: 50% !important;
        background-color: #10B981 !important;
        box-shadow: 0 0 8px #10B981 !important;
    }
    
    .model-name {
        color: #10B981 !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* BUTTONS */
    /* ─────────────────────────────────────────────────────────────────── */
    
    .stButton > button {
        background: linear-gradient(135deg, #7C3AED 0%, #D946EF 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* INPUTS */
    /* ─────────────────────────────────────────────────────────────────── */
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 1px solid #E5E7EB;
        padding: 0.7rem 1rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #7C3AED;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* FILE UPLOADER */
    /* ─────────────────────────────────────────────────────────────────── */
    
    [data-testid="stFileUploader"] {
        background: #ffffff;
        border: 2px dashed #D1D5DB;
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #7C3AED;
        background: #F9FAFB;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* METRICS */
    /* ─────────────────────────────────────────────────────────────────── */
    
    [data-testid="stMetric"] {
        background: #ffffff;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
    }
    
    [data-testid="stMetricLabel"] {
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    [data-testid="stMetricValue"] {
        color: #7C3AED;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* SIDEBAR NAV FIX */
    /* ─────────────────────────────────────────────────────────────────── */
    
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
    
    
     
    /* ─────────────────────────────────────────────────────────────────── */
    /* EXPANDER */
    /* ─────────────────────────────────────────────────────────────────── */
    
    .streamlit-expanderHeader {
        background: #F9FAFB;
        border-radius: 10px;
        font-weight: 600;
        color: #1E293B;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* DIVIDER */
    /* ─────────────────────────────────────────────────────────────────── */
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #E5E7EB, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# LOGO SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════

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

# ═══════════════════════════════════════════════════════════════════════════
# AUTHENTIFICATION
# ═══════════════════════════════════════════════════════════════════════════

_current_user = utils_auth.require_auth()

# ═══════════════════════════════════════════════════════════════════════════
# UTILS FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

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
    
    text_content = response.text
    kpi_data = None
    
    if is_plural:
        intro = f"ANALYSE DES RÉUNIONS\n\nCe rapport identifie les forces et faiblesses de ces échanges et propose des actions concrètes d'amélioration.\n\n"
        pdf_header = "RAPPORT D'AMÉLIORATION (MULTIPLES)"
    else:
        intro = f"ANALYSE DE LA RÉUNION\n\nCe rapport identifie les forces et faiblesses de cet échange et propose des actions concrètes d'amélioration.\n\n"
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

def save_kpis_to_meeting(meeting_index, kpis):
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
    meetings = load_meetings()
    
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
    
    context_text = "\n\n".join([
        f"[{item['meeting_title']} - {int(item['start_time']//60)}:{int(item['start_time']%60):02d}] {item['text']}"
        for item in search_context[:100]
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
    meetings = load_meetings()
    
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

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    # User card
    utils_auth.render_user_sidebar()
    
    st.markdown('<div class="sidebar-section-title">CONFIGURATION</div>', unsafe_allow_html=True)
    
    # Model Selection (Simplified)
    QUOTA_LABELS = {
        "models/gemini-flash-latest":   "gemini-flash-latest   ⚡ Switch si 429",
    }
    
    selected_model = "models/gemini-flash-latest"
    selected_label = QUOTA_LABELS[selected_model]
    
    st.info(f"🤖 Modèle: {selected_label}")

    # Initialize Model
    try:
        MODEL = config.configure(model_name=selected_model)
        
        clean_model_name = MODEL.model_name.replace('models/', '')
        st.markdown(f"""
        <div class="model-status">
            <div class="status-dot"></div>
            <span class="model-name">Actif: {clean_model_name}</span>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erreur config model: {e}")
        MODEL = None

    st.markdown("---")

    # Test API Button
    if MODEL and st.button("🔌 Tester l'API", use_container_width=True, type="primary"):
        with st.spinner("Test en cours..."):
            try:
                test_response = MODEL.generate_content(
                    "Réponds uniquement par: OK",
                    generation_config={"max_output_tokens": 5}
                )
                st.markdown("""
                    <div class="status-success">
                        <div class="status-success-title">✅ API opérationnelle</div>
                        <div class="status-success-text">Quota disponible — vous pouvez générer des rapports.</div>
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                err = str(e)
                if "429" in err or "ResourceExhausted" in err:
                    st.markdown("""
                        <div class="status-error">
                            <div style="color:#EF4444; font-weight:700; margin-bottom:0.3rem;">🔴 Quota épuisé (429)</div>
                            <div style="color:#DC2626; font-size:0.9rem;">Réessayez demain après 00h00 UTC ou activez la facturation.</div>
                        </div>
                    """, unsafe_allow_html=True)
                elif "404" in err or "NotFound" in err:
                    st.markdown("""
                        <div class="status-error">
                            <div style="color:#F97316; font-weight:700; margin-bottom:0.3rem;">⚠️ Modèle introuvable (404)</div>
                            <div style="color:#EA580C; font-size:0.9rem;">Ce modèle n'est pas disponible. Changez de modèle.</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"❌ Erreur inattendue : {err[:120]}")

    st.markdown("---")

    # SQL Server Test
    st.markdown('<div class="sidebar-section-title">SQL SERVER</div>', unsafe_allow_html=True)
    if st.button("🗄️ Tester la connexion SQL", use_container_width=True):
        with st.spinner("Connexion en cours..."):
            result = utils_sql.check_connection()
            if result["ok"]:
                st.markdown(f"""
                    <div class="status-success">
                        <div class="status-success-title">✅ SQL Server connecté</div>
                        <div class="status-success-text">Base : <strong>{result['database']}</strong> · Driver : {result['driver']}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="status-error">
                        <div style="color:#EF4444; font-weight:700;">❌ Connexion échouée</div>
                        <div style="color:#DC2626; font-size:0.9rem;">{result['message']}</div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Global Audit Section
    st.markdown('<div class="sidebar-section-title">CONSOLE D\'ADMINISTRATION</div>', unsafe_allow_html=True)
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

    # KPI Dashboard
    if "global_kpis" in st.session_state and st.session_state.global_kpis:
        kpis = st.session_state.global_kpis
        st.markdown("---")
        

        
        topics = kpis.get('common_topics', [])
        if topics:
            tags_html = "".join([
                f'<span style="background:rgba(139,92,246,0.15);border:1px solid rgba(139,92,246,0.35);'
                f'border-radius:20px;padding:3px 12px;color:#A78BFA;font-size:0.8rem;margin:3px;display:inline-block;">'
                f'{t}</span>'
                for t in topics[:5]
            ])
            st.markdown(
                f'<div style="margin:1rem 0;"><span style="color:#94A3B8;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.1em;">'
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

# ═══════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════════════

# Hero Section
st.markdown("""
<div class="hero-card">
    <div class="hero-title">Meeting Intelligence</div>
    <div class="hero-subtitle">
        Plateforme IA pour transcription automatique, analyse stratégique et reporting commercial.
    </div>
    <div class="hero-tagline">
        Transformez vos <span class="gradient-text">réunions</span> en <span class="gradient-text">insights</span> actionnables
    </div>
</div>
""", unsafe_allow_html=True)

# Feature Cards
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">🎙️</div>
        <div class="feature-title">Transcription Automatique</div>
        <div class="feature-desc">Conversion audio/vidéo en texte structuré avec Gemini AI</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <div class="feature-title">Analyse Intelligente</div>
        <div class="feature-desc">Rapports MEDDIC, KPIs, objections et recommandations stratégiques</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Tableaux Power BI</div>
        <div class="feature-desc">Synchronisation SQL Server pour dashboards décisionnels</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Recherche Sémantique</div>
        <div class="feature-desc">Retrouvez instantanément l'information dans vos réunions</div>
    </div>
</div>
""", unsafe_allow_html=True)

meetings = load_meetings()

# ═══════════════════════════════════════════════════════════════════════════
# NOUVELLE RÉUNION SECTION
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="section-card">
    <div class="section-title">🎤 Nouvelle Réunion</div>
    <div class="section-caption">Uploadez un audio ou vidéo — transcription et analyse automatiques via Gemini AI</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Sélectionnez un fichier (MP3, WAV, M4A, MP4)", 
    type=['mp3', 'wav', 'm4a', 'aac', 'mp4', 'mov', 'avi']
)

col1, col2 = st.columns([3, 1])
with col1:
    meeting_title = st.text_input("Titre de la réunion (facultatif)", placeholder="Ex: Démo CRM - Client X")
with col2:
    lang_choice = st.selectbox("Langue", ["Français", "Anglais", "Mixte"])

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
                
                os.makedirs("tmp", exist_ok=True)
                tmp_filepath = os.path.join("tmp", f"upload_{int(time.time())}_{uploaded_file.name}")
                
                with open(tmp_filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                    
                transcription_text, transcription_clean = utils_transcription.transcribe_and_clean_audio(
                    filepath=tmp_filepath, 
                    model=MODEL, 
                    lang_choice=lang_choice
                )
                
                segments, pure_text = utils_transcription.parse_transcript_to_segments(transcription_text)
                segments_clean, pure_text_clean = utils_transcription.parse_transcript_to_segments(transcription_clean)
                
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
                os.remove(tmp_filepath)
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la transcription : {e}")

# Zone de confirmation
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

# ═══════════════════════════════════════════════════════════════════════════
# MEETINGS ENREGISTRÉS SECTION
# ═══════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="section-card">
    <div class="section-title">
        📂 Meetings Enregistrés
        <span class="badge badge-count">{len(meetings)} réunion(s)</span>
    </div>
    <div class="section-caption">Base de données — Sélectionnez une ou plusieurs réunions pour analyse</div>
</div>
""", unsafe_allow_html=True)

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

    _btn_rapport_col, _btn_sql_col = st.columns(2)

    with _btn_rapport_col:
        _btn_rapport = st.button("📊 Générer rapport d'amélioration", type="primary", use_container_width=True)
    with _btn_sql_col:
        _btn_sql_direct = st.button("🗄️ Structurer & Enregistrer dans SQL Server", type="primary", use_container_width=True, key="btn_sql_pipeline")

    # ══════════════════════════════════════════════════════════════════
    # GÉNÉRATION DU RAPPORT
    # ══════════════════════════════════════════════════════════════════
    
    if _btn_rapport:
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
                    report_text, kpis, pdf_header = generate_improvement_report(transcripts, MODEL)
                    st.session_state.improvement_report = report_text
                    st.session_state.kpis = kpis
                    st.session_state.pdf_header = pdf_header
                    st.session_state.selected_indices = selected_indices
                except ResourceExhausted:
                    st.error(f"❌ Quota API épuisé pour le modèle `{MODEL.model_name}`. Veuillez patienter une minute ou passer à un modèle avec des quotas plus élevés (Gemini 1.5 Flash).")
                except Exception as e:
                    st.error(f"❌ Une erreur est survenue lors de l'analyse avec `{MODEL.model_name}` : {e}")
            
            if "pro_report" in st.session_state:
                del st.session_state.pro_report
            if "pro_pdf_bytes" in st.session_state:
                del st.session_state.pro_pdf_bytes
            if "pro_audio_bytes" in st.session_state:
                del st.session_state.pro_audio_bytes

    # ══════════════════════════════════════════════════════════════════
    # STRUCTURATION SQL
    # ══════════════════════════════════════════════════════════════════
    
    if _btn_sql_direct:
        if len(selected) == 0:
            st.warning("Sélectionne au moins un meeting")
        elif not MODEL:
            st.error("Modèle Gemini non configuré.")
        else:
            _sql_selected_indices = [int(i.split(" - ")[0]) for i in selected]

            _sql_check = utils_sql.check_connection()
            if not _sql_check["ok"]:
                st.error(f"❌ Impossible de joindre SQL Server : {_sql_check['message']}")
                st.stop()

            with st.spinner("🧠 Étape 1/2 — Gemini structure les données depuis la transcription..."):
                try:
                    _structured_all = []
                    for _idx in _sql_selected_indices:
                        _m = meetings[_idx]
                        _src_id = _m.get("meeting_id", str(_idx))
                        if utils_sql.meeting_already_inserted(_src_id):
                            st.warning(f"⏭️ '{_m.get('title','?')}' déjà présent en base — ignoré.")
                            continue
                        _transcript = _m.get("transcript_clean", _m.get("transcript", ""))
                        _structured = utils_ai_structurer.structure_transcript_for_sql(
                            transcript=_transcript,
                            report_text=_transcript,
                            kpis=None,
                            model=MODEL,
                            meeting_title=_m.get("title", "Réunion")
                        )
                        _valid, _errs = utils_ai_structurer.validate_structured_data(_structured)
                        if not _valid:
                            st.warning(f"⚠️ Données partiellement invalides pour '{_m.get('title','?')}' : {_errs}")
                        _structured_all.append((_idx, _src_id, _m, _structured))

                    st.session_state.sql_structured_data = _structured_all
                except Exception as _e:
                    st.error(f"❌ Erreur lors de la structuration IA : {_e}")
                    st.stop()

            if st.session_state.get("sql_structured_data"):
                with st.spinner("🗄️ Étape 2/2 — Insertion dans SQL Server..."):
                    try:
                        _all_stats = []
                        for (_idx, _src_id, _m, _structured) in st.session_state.sql_structured_data:
                            _raw_segs = _m.get("segments_clean", _m.get("segments", []))
                            _stats = utils_sql.insert_meeting_full(
                                structured=_structured,
                                source_meeting_id=_src_id,
                                raw_segments=_raw_segs
                            )
                            _all_stats.append((_m.get("title", "?"), _stats))
                        st.session_state.sql_insert_stats = _all_stats
                    except Exception as _e:
                        st.error(f"❌ Erreur SQL lors de l'insertion : {_e}")
                        st.stop()

            st.rerun()

    # Affichage des résultats SQL
    if "sql_insert_stats" in st.session_state:
        for _title, _stats in st.session_state.sql_insert_stats:
            _total_rows = sum(v for k, v in _stats.items() if k not in ["meeting_id_sql", "success"])
            st.markdown(f"""
            <div class="status-success">
                <div class="status-success-title">✅ Synchronisé avec SQL Server — {_title}</div>
                <div class="status-success-text">
                    meeting_id SQL : <strong>#{_stats.get('meeting_id_sql')}</strong> ·
                    {_stats.get('segments',0)} segments ·
                    {_stats.get('topics',0)} topics ·
                    {_stats.get('decisions',0)} décisions ·
                    {_stats.get('actions',0)} actions ·
                    1 rapport
                    <span style="color:#64748B;">({_total_rows} lignes insérées)</span>
                </div>
                <div style="margin-top:0.5rem; font-size:0.78rem; color:#64748B;">
                    Power BI peut actualiser son dataset pour voir les nouvelles données.
                </div>
            </div>
            """, unsafe_allow_html=True)

    if "sql_structured_data" in st.session_state and st.session_state.sql_structured_data:
        with st.expander("🔍 Aperçu des données structurées par l'IA (JSON)", expanded=False):
            for (_idx, _src_id, _m, _structured) in st.session_state.sql_structured_data:
                st.caption(f"Meeting : {_m.get('title','?')} — source_meeting_id : {_src_id}")
                st.json(_structured)

    if "sql_insert_stats" in st.session_state or "sql_structured_data" in st.session_state:
        if st.button("🗑️ Effacer les résultats SQL", key="btn_sql_reset"):
            for _k in ["sql_structured_data", "sql_insert_stats"]:
                st.session_state.pop(_k, None)
            st.rerun()

    # ══════════════════════════════════════════════════════════════════
    # AFFICHAGE DU RAPPORT
    # ══════════════════════════════════════════════════════════════════
    
    if "improvement_report" in st.session_state and st.session_state.improvement_report:
        
        st.markdown("---")
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
        
        st.text_area("Rapport d'amélioration", st.session_state.improvement_report, height=450)
        
        try:
            import utils_pdf
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

    # Email de suivi
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

        # Analyse des objections
        st.markdown("### ⚠️ Analyse des Blocages & Objections (Beta)")
        st.caption("Détection automatique des freins clients et suggestions de réponses.")

        if st.button("🔍 Analyser les Objections", type="primary"):
            with st.spinner("Analyse approfondie des objections..."):
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