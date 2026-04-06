import streamlit as st
import sys
import os

# Add parent directory to path to import shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import config
import utils_theme
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
            
        # Backfill transcript if missing
        for meeting in data:
            if "transcript" not in meeting and "segments" in meeting:
                meeting["transcript"] = "\n".join([s.get("text", "") for s in meeting["segments"]])
                
        return data


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
                response = MODEL.generate_content(
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
                    wait = retry_delay * (2 ** attempt)  # Exponential: 15s, 30s, 60s
                    print(f"[semantic_search] Quota 429 — attente {wait}s (tentative {attempt+1}/{max_retries})")
                    import time
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
            import re
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            else:
                result_text = result_text.replace("```json", "").replace("```", "").strip()

        search_results = json.loads(result_text)
        return search_results
    except json.JSONDecodeError as e:
        return {
            "results": [],
            "summary": f"Erreur de format dans la réponse de l'IA. Veuillez réessayer."
        }
    except Exception as e:
        return {
            "results": [],
            "summary": f"Erreur lors de la recherche: {str(e)}"
        }



# -------------------------
# UI
st.set_page_config(page_title="Recherche Intelligente", page_icon="🔍", layout="wide")
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
st.title("🔍 Recherche Intelligente")
st.caption("Posez une question en langage naturel — l’IA trouve les réponses dans vos réunions")

st.caption("Posez une question pour trouver rapidement des informations dans vos meetings")

# Sidebar - Model Selection
with st.sidebar:
    st.header("⚙️ Configuration")
    utils_theme.render_theme_toggle()
    
    QUOTA_LABELS = {
        "models/gemini-2.5-flash":      "gemini-2.5-flash      ⚠️ QUOTA LIMITÉ (20/j)",
        "models/gemini-2.0-flash":      "gemini-2.0-flash      ✅ RECOMMANDÉ (Stable)",
        "models/gemini-1.5-flash":      "gemini-1.5-flash      🚀 Quota de secours",
        "models/gemini-flash-latest":   "gemini-flash-latest   ⚡ Dernier Stable",
    }
    
    try:
        available_models = config.list_available_models()
        if not available_models:
            available_models = ["models/gemini-flash-latest"]
            
        labels = [QUOTA_LABELS.get(m, m) for m in available_models]
        
        # Standardize default to flash-latest if available
        default_idx = 0
        for i, m in enumerate(available_models):
            if "flash-latest" in m.lower():
                default_idx = i
                break
        
        selected_label = st.selectbox("🤖 Choisir le modèle", labels, index=default_idx)
        selected_model = available_models[labels.index(selected_label)]
        
    except Exception as e:
        st.error(f"Erreur chargement modèles: {e}")
        selected_model = "models/gemini-flash-latest"
    
    # Initialize Model with selection
    try:
        MODEL = config.configure(model_name=selected_model)
    except Exception as e:
        st.error(f"Erreur init modèle: {e}")
        
    st.markdown("---")
    
    # ── Bouton Test API ──────────────────────────────────────────
    if MODEL and st.button("🔌 Tester l'API", use_container_width=True, type="primary"):
        with st.spinner("Test en cours..."):
            try:
                test_prompt = "Dis 'OK' si tu me reçois, en 1 seul mot."
                response = MODEL.generate_content(test_prompt, request_options={"timeout": 60})
                if "OK" in response.text.upper():
                    st.success("✅ API Connectée !")
                else:
                    st.warning(f"⚠️ Réponse inattendue: {response.text}")
            except Exception as e:
                st.error(f"❌ Erreur API: {str(e)}")


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
        "Sélectionnez les meetings à rechercher",
        labels,
        help="Choisissez un ou plusieurs meetings dans lesquels chercher"
    )
    
    # Search input
    search_query = st.text_input(
        "Votre question",
        placeholder="Ex: Quel était le budget du client ? Quelles objections ont été mentionnées ?",
        key="search_input"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        search_button = st.button("🔎 Rechercher", type="primary")
    with col2:
        if len(selected) == 0:
            st.caption("⚠️ Sélectionnez au moins un meeting")
    
    # Display search results
    if search_button and search_query and len(selected) > 0:
        selected_indices = [int(i.split(" - ")[0]) for i in selected]
        
        with st.spinner("🔍 Recherche en cours..."):
            try:
                search_results = semantic_search(search_query, selected_indices)
            except ResourceExhausted:
                st.error("❌ Quota API épuisé. Veuillez patienter une minute ou passer à un modèle avec des quotas plus élevés (Gemini 1.5 Flash).")
                search_results = None
            except Exception as e:
                st.error(f"❌ Erreur : {e}")
                search_results = None
        
        if search_results:
            st.markdown("---")

            # Display summary
            summary_text = search_results.get("summary", "Aucun résumé disponible")
            st.markdown(f"""
<div style="
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1.5rem;
    animation: fade-in-up 0.4s ease both;
">
    <div style="color:#A78BFA;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;">💡 Résumé IA</div>
    <div style="color:#E2E8F0;line-height:1.7;">{summary_text}</div>
</div>
""", unsafe_allow_html=True)

            # Display results
            results = search_results.get("results", [])
            if results:
                st.subheader(f"📍 {len(results)} Résultat(s) trouvé(s)")
                for result in results:
                    with st.expander(f"{result.get('meeting_title')} - {result.get('relevance')}% match"):
                        st.caption(f"Horodatage: {result.get('timestamp')}")
                        st.write(result.get('text'))
            else:
                st.warning("Aucun résultat pertinent trouvé pour cette question.")
