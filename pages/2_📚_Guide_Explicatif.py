import streamlit as st
import sys
import os

# Add parent directory to path to import shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import config
import utils_auth
from utils_topic_pdf import create_topic_pdf
from google.api_core.exceptions import ResourceExhausted

# Initialize MODEL - will be set after model selection in sidebar
MODEL = None


# -------------------------
# Utils
# -------------------------

def load_meetings():
    data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "meetings.json")
    if not os.path.exists(data_file):
        return []
    with open(data_file, "r", encoding="utf8") as f:
        data = json.load(f)
        if isinstance(data, dict):
            data = [data]
        return data


def generate_topic_explanation(topic, selected_indices):
    """Generate an explanatory report about a specific topic from meeting transcripts"""
    meetings = load_meetings()
    
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
        response = MODEL.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erreur lors de la génération du rapport : {str(e)}"


# -------------------------
# UI Configuration
# -------------------------
st.set_page_config(page_title="Guide Explicatif", page_icon="📚", layout="wide")

# Authentification
_current_user = utils_auth.require_auth()

# -------------------------
# Custom CSS
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ═══════════════════════════════════════════════════════════
   GLOBAL RESET & BASE
   ═══════════════════════════════════════════════════════════ */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: #FFFFFF !important;
}

/* Flèche personnalisée pour ouvrir la sidebar */
[data-testid="collapsedControl"] svg {
    display: none !important;
}
[data-testid="collapsedControl"]::after {
    content: ">>" !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    color: #7C3AED !important;
    letter-spacing: -2px !important;
    display: inline-block !important;
}
[data-testid="collapsedControl"] {
    z-index: 999999 !important;
    background: transparent !important;
}

.main {
    background-color: #F8FAFC !important;
}

.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1400px !important;
}

/* Hide Streamlit branding */
#MainMenu, footer {
    visibility: hidden !important;
}

/* ═══════════════════════════════════════════════════════════
   SIDEBAR STYLING (Match Main Page)
   ═══════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
    border-right: 1px solid rgba(148, 163, 184, 0.1) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

/* Sidebar text colors */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #F1F5F9 !important;
}

/* Sidebar section title */
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

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #D946EF 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.25rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(139, 92, 246, 0.4) !important;
}

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid rgba(148, 163, 184, 0.15) !important;
    margin: 1.5rem 0 !important;
}

/* Logo in sidebar */
[data-testid="stSidebarNav"]::before {
    content: "";
    display: block;
    margin: 1.5rem auto 1.5rem auto;
    width: 85%;
    height: 110px;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
}

/* Add emoji to app page in sidebar */
[data-testid="stSidebarNav"] li:first-child a::before {
    content: "🏠";
    margin-right: 0px !important;
}

/* Active model badge */
.model-active-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #10B981;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 0.5rem;
}

.model-active-badge::before {
    content: "";
    width: 6px;
    height: 6px;
    background: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10B981;
}

/* ═══════════════════════════════════════════════════════════
   TYPOGRAPHY
   ═══════════════════════════════════════════════════════════ */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.02em !important;
}

h1 {
    color: #111827 !important;
    font-weight: 800 !important;
    font-size: 2.25rem !important;
    margin: 0 !important;
}

h2 {
    color: #1F2937 !important;
    font-weight: 700 !important;
    font-size: 1.65rem !important;
}

h3 {
    color: #374151 !important;
    font-weight: 600 !important;
    font-size: 1.25rem !important;
}

label {
    color: #374151 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}

/* ═══════════════════════════════════════════════════════════
   PAGE HEADER
   ═══════════════════════════════════════════════════════════ */
.guide-page-header {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 24px;
    padding: 2.5rem 2.75rem;
    margin-bottom: 2rem;
    box-shadow: 
        0 1px 3px rgba(0, 0, 0, 0.05),
        0 0 0 1px rgba(139, 92, 246, 0.05);
    display: flex;
    align-items: center;
    gap: 1.75rem;
    transition: all 0.3s ease;
}

.guide-page-header:hover {
    box-shadow: 
        0 4px 12px rgba(0, 0, 0, 0.08),
        0 0 0 1px rgba(139, 92, 246, 0.1);
}

.guide-icon-box {
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
    width: 72px;
    height: 72px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 
        0 8px 24px rgba(139, 92, 246, 0.35),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    flex-shrink: 0;
}

.guide-title {
    background: linear-gradient(135deg, #7C3AED 0%, #D946EF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
    font-size: 2.25rem;
    margin: 0;
    line-height: 1.2;
    letter-spacing: -0.03em;
}

.guide-subtitle {
    color: #64748B;
    font-size: 1.05rem;
    margin-top: 0.5rem;
    line-height: 1.6;
    font-weight: 400;
}

/* ═══════════════════════════════════════════════════════════
   FORM CARD
   ═══════════════════════════════════════════════════════════ */
.guide-form-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 22px;
    padding: 2.5rem 2.75rem;
    margin-bottom: 2rem;
    box-shadow: 
        0 1px 3px rgba(0, 0, 0, 0.04),
        0 0 0 1px rgba(139, 92, 246, 0.03);
}

.guide-form-title {
    color: #1F2937;
    font-size: 1.35rem;
    font-weight: 700;
    margin-bottom: 1.75rem;
    display: flex;
    align-items: center;
    gap: 0.65rem;
    letter-spacing: -0.02em;
}

/* Empty state */
.empty-state-card {
    background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
    border: 2px dashed #CBD5E1;
    border-radius: 20px;
    padding: 3.5rem 2rem;
    text-align: center;
}

.empty-state-icon {
    font-size: 4rem;
    margin-bottom: 1.25rem;
    opacity: 0.6;
}

.empty-state-card h3 {
    color: #64748B !important;
    font-weight: 600 !important;
    margin-bottom: 0.5rem !important;
}

.empty-state-card p {
    color: #94A3B8;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* ═══════════════════════════════════════════════════════════
   INPUTS & MULTISELECT
   ═══════════════════════════════════════════════════════════ */
input[type="text"] {
    background-color: #F8FAFC !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 14px !important;
    padding: 0.85rem 1.15rem !important;
    font-size: 0.95rem !important;
    color: #111827 !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

input[type="text"]:focus {
    background-color: #FFFFFF !important;
    border-color: #8B5CF6 !important;
    box-shadow: 
        0 0 0 4px rgba(139, 92, 246, 0.1),
        0 2px 8px rgba(139, 92, 246, 0.08) !important;
    outline: none !important;
}

input[type="text"]::placeholder {
    color: #94A3B8 !important;
    font-weight: 400 !important;
}

/* Multiselect */
.stMultiSelect > div > div {
    background-color: #F8FAFC !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 14px !important;
    transition: all 0.2s ease !important;
}

.stMultiSelect > div > div:focus-within {
    background-color: #FFFFFF !important;
    border-color: #8B5CF6 !important;
    box-shadow: 
        0 0 0 4px rgba(139, 92, 246, 0.1),
        0 2px 8px rgba(139, 92, 246, 0.08) !important;
}

.stMultiSelect span[data-baseweb="tag"] {
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    padding: 0.35rem 0.65rem !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    border: none !important;
}

.stMultiSelect span[data-baseweb="tag"] svg {
    fill: #FFFFFF !important;
}

/* ═══════════════════════════════════════════════════════════
   BUTTONS
   ═══════════════════════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #8B5CF6 0%, #D946EF 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 2.25rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: -0.01em !important;
    box-shadow: 
        0 4px 14px rgba(139, 92, 246, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 
        0 8px 20px rgba(139, 92, 246, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 
        0 2px 8px rgba(139, 92, 246, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}

/* Download buttons */
.stDownloadButton > button {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.75rem 1.75rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    box-shadow: 
        0 4px 14px rgba(16, 185, 129, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transition: all 0.3s ease !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 
        0 6px 18px rgba(16, 185, 129, 0.35),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}

/* ═══════════════════════════════════════════════════════════
   CAPTIONS & WARNINGS
   ═══════════════════════════════════════════════════════════ */
.stCaption {
    color: #94A3B8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

.guide-warning {
    background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
    border-left: 4px solid #F59E0B;
    color: #78350F;
    padding: 1rem 1.25rem;
    border-radius: 12px;
    font-size: 0.9rem;
    font-weight: 500;
    margin-top: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

/* ═══════════════════════════════════════════════════════════
   GENERATED CONTENT CARD
   ═══════════════════════════════════════════════════════════ */
.generated-content-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 20px;
    padding: 2.5rem 2.75rem;
    margin-top: 2rem;
    box-shadow: 
        0 2px 8px rgba(0, 0, 0, 0.04),
        0 0 0 1px rgba(139, 92, 246, 0.05);
}

.generated-content-card h1 {
    background: linear-gradient(135deg, #7C3AED 0%, #D946EF 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

.generated-content-card h2 {
    color: #A78BFA !important;
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
}

.generated-content-card h3 {
    color: #C084FC !important;
    margin-top: 1.5rem !important;
    margin-bottom: 0.75rem !important;
}

.generated-content-card p {
    color: #374151 !important;
    line-height: 1.8 !important;
    margin-bottom: 1rem !important;
}

.generated-content-card ul,
.generated-content-card ol {
    color: #374151 !important;
    line-height: 1.8 !important;
    margin-left: 1.5rem !important;
    margin-bottom: 1rem !important;
}

.generated-content-card strong {
    color: #1F2937 !important;
    font-weight: 700 !important;
}

.generated-content-card code {
    background: #F8FAFC !important;
    color: #7C3AED !important;
    padding: 0.2rem 0.4rem !important;
    border-radius: 4px !important;
    font-size: 0.9em !important;
    font-family: 'SF Mono', Monaco, monospace !important;
}

/* Download section */
.download-section {
    background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
    border: 1px solid #DDD6FE;
    border-radius: 18px;
    padding: 2rem 2.25rem;
    margin-top: 2.5rem;
}

.download-section h3 {
    color: #7C3AED !important;
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    margin-bottom: 1.5rem !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

/* ═══════════════════════════════════════════════════════════
   DIVIDERS
   ═══════════════════════════════════════════════════════════ */
hr {
    border: none !important;
    border-top: 1px solid #E5E7EB !important;
    margin: 2.5rem 0 !important;
}

/* ═══════════════════════════════════════════════════════════
   SPINNER
   ═══════════════════════════════════════════════════════════ */
.stSpinner > div {
    border-top-color: #8B5CF6 !important;
}

/* ═══════════════════════════════════════════════════════════
   RESPONSIVE
   ═══════════════════════════════════════════════════════════ */
@media (max-width: 768px) {
    .guide-page-header {
        flex-direction: column;
        text-align: center;
        padding: 2rem 1.5rem;
    }
    
    .guide-icon-box {
        width: 64px;
        height: 64px;
    }
    
    .guide-title {
        font-size: 1.75rem;
    }
    
    .guide-form-card {
        padding: 1.75rem 1.5rem;
    }
    
    .generated-content-card {
        padding: 1.75rem 1.5rem;
    }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Logo Sidebar
# -------------------------
import base64
try:
    with open("logo_inspirigence.jpg", "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(f"""
        <style>
        [data-testid="stSidebarNav"]::before {{
            background-image: url("data:image/jpeg;base64,{data}");
        }}
        </style>
    """, unsafe_allow_html=True)
except Exception:
    pass

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    # User info
    utils_auth.render_user_sidebar()
    st.markdown("---")
    
    # Configuration Section
    st.markdown('<div class="sidebar-section-title">⚙️ Configuration</div>', unsafe_allow_html=True)
    
    try:
        available_models = config.list_available_models()
        model_options = [m.replace("models/", "") for m in available_models]
        
        # Standardize default to 1.5-flash if available
        default_idx = 0
        for i, m in enumerate(model_options):
            if "flash" in m.lower() and "1.5" in m.lower() and "8b" not in m.lower():
                default_idx = i
                break
        
        selected_model = st.selectbox(
            "🤖 Modèle Gemini",
            model_options,
            index=default_idx,
            help="Sélectionnez le modèle IA pour générer le guide"
        )
        
        # Active model badge
        st.markdown(f"""
        <div class="model-active-badge">
            Modèle actif : {selected_model}
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erreur chargement modèles: {e}")
        selected_model = "gemini-1.5-flash"
    
    # Initialize Model with selection
    try:
        MODEL = config.configure(model_name=selected_model)
    except ValueError as e:
        st.stop()
    except Exception as e:
        st.error(f"Erreur init modèle: {e}")
        st.stop()

# -------------------------
# MAIN PAGE
# -------------------------

# Hero Header
st.markdown("""
<div class="guide-page-header">
    <div class="guide-icon-box">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 19.5C4 18.837 4.26339 18.2011 4.73223 17.7322C5.20107 17.2634 5.83696 17 6.5 17H20V2H6.5C5.83696 2 5.20107 2.26339 4.73223 2.73223C4.26339 3.20107 4 3.83696 4 4.5V19.5Z" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M4 19.5C4 20.163 4.26339 20.7989 4.73223 21.2678C5.20107 21.7366 5.83696 22 6.5 22H20" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    <div>
        <div class="guide-title">Guide Explicatif</div>
        <div class="guide-subtitle">Créez un rapport expert sur n'importe quel sujet mentionné dans vos réunions</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Load meetings
meetings = load_meetings()

if not meetings:
    st.markdown("""
    <div class="empty-state-card">
        <div class="empty-state-icon">📚</div>
        <h3>Aucun meeting disponible</h3>
        <p>Veuillez d'abord analyser des meetings depuis la page principale<br>pour générer des guides explicatifs.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Form Card
    st.markdown('<div class="guide-form-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="guide-form-title">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2.5">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
        </svg>
        Configuration du guide
    </div>
    """, unsafe_allow_html=True)
    
    # Meeting selection
    labels = [
        f"{i} — {m.get('title', m.get('filename', 'Sans titre'))}"
        for i, m in enumerate(meetings)
    ]
    
    selected = st.multiselect(
        "📂 Sélectionnez les meetings à analyser",
        labels,
        help="Choisissez un ou plusieurs meetings contenant des informations sur le sujet"
    )
    
    # Topic input
    topic_input = st.text_input(
        "📝 Sujet à expliquer",
        placeholder="Ex: Kommo CRM, Agent IA, Système de gestion des leads...",
        key="topic_input",
        help="Entrez le nom du service, produit ou concept que vous voulez expliquer"
    )
    
    # Generate button area
    col1, col2 = st.columns([1, 3])
    with col1:
        generate_button = st.button("📘 Générer le Guide", type="primary", use_container_width=True)
    with col2:
        if len(selected) == 0 and topic_input:
            st.markdown("""
            <div class="guide-warning">
                ⚠️ Veuillez sélectionner au moins un meeting avant de générer le guide
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close guide-form-card
    
    # Generate and display guide
    if generate_button and topic_input and len(selected) > 0:
        selected_indices = [int(i.split(" — ")[0]) for i in selected]
        
        with st.spinner(f"🔍 Analyse des meetings pour créer le guide sur '{topic_input}'..."):
            try:
                explanation_report = generate_topic_explanation(topic_input, selected_indices)
                st.session_state.topic_explanation = explanation_report
                st.session_state.topic_name = topic_input
            except ResourceExhausted:
                st.error("❌ Quota API épuisé. Veuillez patienter une minute ou passer à un modèle avec des quotas plus élevés (Gemini 1.5 Flash).")
            except Exception as e:
                st.error(f"❌ Erreur : {e}")
    
    # Display explanation if available
    if "topic_explanation" in st.session_state and st.session_state.topic_explanation:
        st.markdown("---")
        
        # Generated content card
        st.markdown('<div class="generated-content-card">', unsafe_allow_html=True)
        st.markdown(st.session_state.topic_explanation)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download section
        st.markdown('<div class="download-section">', unsafe_allow_html=True)
        st.markdown("""
        <h3>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2.5">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            Télécharger le Guide
        </h3>
        """, unsafe_allow_html=True)
        
        col_dl1, col_dl2 = st.columns(2)
        
        with col_dl1:
            st.download_button(
                label="📄 Télécharger en PDF",
                data=create_topic_pdf(st.session_state.topic_explanation, st.session_state.topic_name),
                file_name=f"guide_{st.session_state.topic_name.replace(' ', '_')}.pdf",
                mime="application/pdf",
                key="download_topic_pdf"
            )
        
        with col_dl2:
            st.download_button(
                label="📥 Télécharger en Markdown",
                data=st.session_state.topic_explanation,
                file_name=f"guide_{st.session_state.topic_name.replace(' ', '_')}.md",
                mime="text/markdown",
                key="download_topic_md"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)