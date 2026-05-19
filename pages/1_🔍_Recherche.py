import streamlit as st
import sys
import os

# Add parent directory to path to import shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import config
import utils_auth
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
                    wait = retry_delay * (2 ** attempt)
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
# UI Configuration
# -------------------------
st.set_page_config(page_title="Recherche Intelligente", page_icon="🔍", layout="wide")

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

/* Status messages in sidebar */
.status-success {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-left: 3px solid #10B981;
    color: #10B981;
    padding: 0.75rem 1rem;
    border-radius: 10px;
    font-weight: 500;
    font-size: 0.85rem;
    margin-top: 0.75rem;
}

.status-error {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-left: 3px solid #EF4444;
    color: #FCA5A5;
    padding: 0.75rem 1rem;
    border-radius: 10px;
    font-weight: 500;
    font-size: 0.85rem;
    margin-top: 0.75rem;
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
.search-page-header {
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

.search-page-header:hover {
    box-shadow: 
        0 4px 12px rgba(0, 0, 0, 0.08),
        0 0 0 1px rgba(139, 92, 246, 0.1);
}

.search-icon-box {
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

.search-title {
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

.search-subtitle {
    color: #64748B;
    font-size: 1.05rem;
    margin-top: 0.5rem;
    line-height: 1.6;
    font-weight: 400;
}

/* ═══════════════════════════════════════════════════════════
   SEARCH FORM CARD
   ═══════════════════════════════════════════════════════════ */
.search-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 22px;
    padding: 2.5rem 2.75rem;
    margin-bottom: 2rem;
    box-shadow: 
        0 1px 3px rgba(0, 0, 0, 0.04),
        0 0 0 1px rgba(139, 92, 246, 0.03);
}

.search-form-title {
    color: #1F2937;
    font-size: 1.35rem;
    font-weight: 700;
    margin-bottom: 1.75rem;
    display: flex;
    align-items: center;
    gap: 0.65rem;
    letter-spacing: -0.02em;
}

.search-form-title svg {
    flex-shrink: 0;
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

/* ═══════════════════════════════════════════════════════════
   CAPTIONS & WARNINGS
   ═══════════════════════════════════════════════════════════ */
.stCaption {
    color: #94A3B8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

.search-warning {
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
   SEARCH RESULTS - SUMMARY CARD
   ═══════════════════════════════════════════════════════════ */
.search-summary-card {
    background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
    border: 1.5px solid #DDD6FE;
    border-left: 4px solid #8B5CF6;
    border-radius: 18px;
    padding: 1.75rem 2rem;
    margin-bottom: 2.25rem;
    box-shadow: 
        0 2px 8px rgba(139, 92, 246, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.5);
}

.search-summary-label {
    color: #7C3AED;
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.search-summary-text {
    color: #1F2937;
    line-height: 1.8;
    font-size: 1.05rem;
    font-weight: 500;
}

/* ═══════════════════════════════════════════════════════════
   SEARCH RESULTS - HEADER
   ═══════════════════════════════════════════════════════════ */
.results-count-header {
    color: #1F2937;
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
    margin-top: 2.5rem;
    display: flex;
    align-items: center;
    gap: 0.85rem;
    letter-spacing: -0.02em;
}

.results-count-badge {
    background: linear-gradient(135deg, #7C3AED 0%, #8B5CF6 100%);
    color: #FFFFFF;
    font-size: 0.85rem;
    font-weight: 800;
    padding: 0.35rem 0.85rem;
    border-radius: 24px;
    box-shadow: 
        0 2px 8px rgba(124, 58, 237, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* ═══════════════════════════════════════════════════════════
   SEARCH RESULTS - RESULT CARDS
   ═══════════════════════════════════════════════════════════ */
.result-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.25rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.result-card:hover {
    border-color: #C4B5FD;
    box-shadow: 
        0 8px 24px rgba(139, 92, 246, 0.12),
        0 0 0 1px rgba(139, 92, 246, 0.08);
    transform: translateY(-3px);
}

.result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    gap: 1rem;
}

.result-meeting-name {
    color: #111827;
    font-weight: 700;
    font-size: 1.1rem;
    letter-spacing: -0.01em;
}

.result-timestamp {
    color: #64748B;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.45rem;
}

.result-text {
    color: #374151;
    line-height: 1.8;
    font-size: 0.95rem;
    font-weight: 400;
    padding: 1rem 1.25rem;
    background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
    border-radius: 12px;
    border-left: 3px solid #E5E7EB;
}

/* ═══════════════════════════════════════════════════════════
   BADGES (Relevance)
   ═══════════════════════════════════════════════════════════ */
.result-badge {
    font-size: 0.75rem;
    font-weight: 800;
    padding: 0.4rem 0.95rem;
    border-radius: 24px;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    white-space: nowrap;
}

.badge-high {
    background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
    color: #065F46;
    border: 1.5px solid #6EE7B7;
    box-shadow: 0 2px 6px rgba(16, 185, 129, 0.15);
}

.badge-medium {
    background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
    color: #78350F;
    border: 1.5px solid #FCD34D;
    box-shadow: 0 2px 6px rgba(245, 158, 11, 0.15);
}

.badge-low {
    background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
    color: #7F1D1D;
    border: 1.5px solid #FCA5A5;
    box-shadow: 0 2px 6px rgba(239, 68, 68, 0.15);
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
    .search-page-header {
        flex-direction: column;
        text-align: center;
        padding: 2rem 1.5rem;
    }
    
    .search-icon-box {
        width: 64px;
        height: 64px;
    }
    
    .search-title {
        font-size: 1.75rem;
    }
    
    .search-card {
        padding: 1.75rem 1.5rem;
    }
    
    .result-card {
        padding: 1.25rem 1.5rem;
    }
    
    .result-header {
        flex-direction: column;
        align-items: flex-start;
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
    
    QUOTA_LABELS = {
        "models/gemini-2.5-flash":      "gemini-2.5-flash",
        "models/gemini-2.0-flash":      "gemini-2.0-flash",
        "models/gemini-1.5-flash":      "gemini-1.5-flash",
        "models/gemini-flash-latest":   "gemini-flash-latest",
    }
    
    try:
        available_models = config.list_available_models()
        if not available_models:
            available_models = ["models/gemini-flash-latest"]
            
        labels = [QUOTA_LABELS.get(m, m.replace("models/", "")) for m in available_models]
        
        default_idx = 0
        for i, m in enumerate(available_models):
            if "flash-latest" in m.lower():
                default_idx = i
                break
        
        selected_label = st.selectbox(
            "🤖 Modèle Gemini", 
            labels, 
            index=default_idx,
            help="Sélectionnez le modèle IA pour la recherche"
        )
        selected_model = available_models[labels.index(selected_label)]
        
        # Active model badge
        st.markdown(f"""
        <div class="model-active-badge">
            Modèle actif : {selected_label}
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erreur chargement modèles: {e}")
        selected_model = "models/gemini-flash-latest"
    
    # Initialize Model
    try:
        MODEL = config.configure(model_name=selected_model)
    except Exception as e:
        st.error(f"Erreur init modèle: {e}")
        
    st.markdown("---")
    
    # Test API Button
    if MODEL and st.button("🔌 Tester l'API", use_container_width=True, type="primary"):
        with st.spinner("Test en cours..."):
            try:
                test_prompt = "Dis 'OK' si tu me reçois, en 1 seul mot."
                response = MODEL.generate_content(test_prompt, request_options={"timeout": 60})
                if "OK" in response.text.upper():
                    st.markdown('<div class="status-success">✅ API Connectée !</div>', unsafe_allow_html=True)
                else:
                    st.warning(f"⚠️ Réponse inattendue: {response.text}")
            except Exception as e:
                st.markdown(f'<div class="status-error">❌ Erreur API: {str(e)}</div>', unsafe_allow_html=True)

# -------------------------
# MAIN PAGE
# -------------------------

# Hero Header
st.markdown("""
<div class="search-page-header">
    <div class="search-icon-box">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19Z" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M21 21L16.65 16.65" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    <div>
        <div class="search-title">Recherche Intelligente</div>
        <div class="search-subtitle">Posez une question en langage naturel — l'IA retrouve les réponses dans vos réunions</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Load meetings
meetings = load_meetings()

if not meetings:
    st.markdown("""
    <div class="empty-state-card">
        <div class="empty-state-icon">🔍</div>
        <h3>Aucun meeting disponible</h3>
        <p>Veuillez d'abord analyser des meetings depuis la page principale<br>pour utiliser la recherche intelligente.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Search Form Card
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="search-form-title">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2.5">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.35-4.35"/>
        </svg>
        Formulaire de recherche
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
        help="Choisissez un ou plusieurs meetings dans lesquels effectuer la recherche intelligente"
    )
    
    # Search input
    search_query = st.text_input(
        "💬 Votre question",
        placeholder="Exemple : Quel était le budget discuté ? Quelles objections ont été mentionnées ?",
        key="search_input"
    )
    
    # Search button area
    col1, col2 = st.columns([1, 3])
    with col1:
        search_button = st.button("🔎 Rechercher", type="primary", use_container_width=True)
    with col2:
        if len(selected) == 0 and search_query:
            st.markdown("""
            <div class="search-warning">
                ⚠️ Veuillez sélectionner au moins un meeting avant de lancer la recherche
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close search-card
    
    # -------------------------
    # Display Search Results
    # -------------------------
    if search_button and search_query and len(selected) > 0:
        selected_indices = [int(i.split(" — ")[0]) for i in selected]
        
        with st.spinner("🔍 Recherche en cours dans vos meetings..."):
            try:
                search_results = semantic_search(search_query, selected_indices)
            except ResourceExhausted:
                st.error("❌ Quota API épuisé. Veuillez patienter une minute ou passer à un modèle avec des quotas plus élevés (Gemini 1.5 Flash).")
                search_results = None
            except Exception as e:
                st.error(f"❌ Erreur : {e}")
                search_results = None
        
        if search_results:
            st.markdown("<hr>", unsafe_allow_html=True)
            
            # Display summary
            summary_text = search_results.get("summary", "Aucun résumé disponible")
            st.markdown(f"""
<div class="search-summary-card">
    <div class="search-summary-label">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2.5">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
            <path d="M2 17l10 5 10-5"/>
            <path d="M2 12l10 5 10-5"/>
        </svg>
        Résumé IA
    </div>
    <div class="search-summary-text">{summary_text}</div>
</div>
""", unsafe_allow_html=True)
            
            # Display results
            results = search_results.get("results", [])
            if results:
                st.markdown(f"""
<div class="results-count-header">
    Résultats trouvés
    <span class="results-count-badge">{len(results)}</span>
</div>
""", unsafe_allow_html=True)
                
                for result in results:
                    rel = result.get('relevance', 0)
                    badge_class = 'badge-high' if rel >= 80 else 'badge-medium' if rel >= 50 else 'badge-low'
                    badge_text = f"{rel}% pertinent"
                    
                    st.markdown(f"""
<div class="result-card">
    <div class="result-header">
        <span class="result-meeting-name">{result.get('meeting_title', 'Sans titre')}</span>
        <span class="result-badge {badge_class}">{badge_text}</span>
    </div>
    <div class="result-timestamp">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2.5">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 6v6l4 2"/>
        </svg>
        {result.get('timestamp', '--:--')}
    </div>
    <div class="result-text">{result.get('text', '')}</div>
</div>
""", unsafe_allow_html=True)
            else:
                st.markdown("""
<div class="empty-state-card">
    <div class="empty-state-icon">🤷</div>
    <h3>Aucun résultat pertinent trouvé</h3>
    <p>Essayez de reformuler votre question ou de sélectionner d'autres meetings.<br>L'IA n'a pas trouvé d'informations correspondant à votre recherche.</p>
</div>
""", unsafe_allow_html=True)