import streamlit as st
import sys
import os

# Add parent directory to path to import shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import config
import utils_theme
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
# UI
st.set_page_config(page_title="Guide Explicatif", page_icon="📚", layout="wide")
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

# Hero Header
st.title("📚 Générer un Guide Explicatif")
st.caption("Créez un rapport expert sur n’importe quel sujet mentionné dans vos réunions")

st.caption("Créez un rapport détaillé expliquant comment fonctionne un service/produit mentionné dans vos meetings")

# Sidebar - Model Selection
with st.sidebar:
    st.header("⚙️ Configuration")
    utils_theme.render_theme_toggle()
    
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
            "Modèle Gemini",
            model_options,
            index=default_idx
        )
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


# Load meetings
meetings = load_meetings()

if not meetings:
    st.warning("Aucun meeting disponible. Veuillez d'abord analyser des meetings depuis la page principale.")
else:
    # Meeting selection
    labels = [
        f"{i} - {m.get('title', m.get('filename', 'Sans titre'))}"
        for i, m in enumerate(meetings)
    ]
    
    selected = st.multiselect(
        "Sélectionnez les meetings à analyser",
        labels,
        help="Choisissez un ou plusieurs meetings contenant des informations sur le sujet"
    )
    
    # Topic input
    topic_input = st.text_input(
        "Sujet à expliquer",
        placeholder="Ex: Kommo CRM, Agent IA, Système de gestion des leads...",
        key="topic_input",
        help="Entrez le nom du service, produit ou concept que vous voulez expliquer"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_button = st.button("📘 Générer le Guide", type="primary")
    with col2:
        if len(selected) == 0:
            st.caption("⚠️ Sélectionnez au moins un meeting")
    
    # Generate and display guide
    if generate_button and topic_input and len(selected) > 0:
        selected_indices = [int(i.split(" - ")[0]) for i in selected]
        
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
        st.write(st.session_state.topic_explanation)
        
        st.markdown("---")
        
        # Download buttons
        st.markdown("### 📥 Télécharger le Guide")
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
