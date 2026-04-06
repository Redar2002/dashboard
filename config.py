import os
import warnings
# Suppress the FutureWarning from the deprecated google.generativeai SDK
warnings.filterwarnings(
    "ignore",
    message=".*google.generativeai.*",
    category=FutureWarning
)

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# ✅ Modèles supportés (Stable API)
# gemini-flash-latest est le plus robuste pour le Free Tier
HIGH_QUOTA_DEFAULT = "models/gemini-flash-latest" 

ALLOWED_MODELS = [
    "models/gemini-flash-latest",     # Seul modèle fonctionnel confirmé
]


def _resolve_model_name(model_name):
    """Validates and resolves a model name against the allowed list."""
    if model_name not in ALLOWED_MODELS:
        clean_name = model_name.split("/")[-1]
        for allowed in ALLOWED_MODELS:
            if clean_name in allowed:
                return allowed
        print(f"[config] Modèle '{model_name}' inconnu → fallback vers {HIGH_QUOTA_DEFAULT}")
        return HIGH_QUOTA_DEFAULT
    return model_name


def configure(model_name=HIGH_QUOTA_DEFAULT):
    """Configures the Gemini API and returns a GenerativeModel.
    Uses temperature=0.3 for balanced, consistent text generation.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY manquante dans le fichier .env")

    model_name = _resolve_model_name(model_name)
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name,
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            max_output_tokens=8192,
        )
    )


def configure_json(model_name=HIGH_QUOTA_DEFAULT):
    """Configures the Gemini API for structured JSON outputs.
    Uses temperature=0.0 for fully deterministic, parseable responses.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY manquante dans le fichier .env")

    model_name = _resolve_model_name(model_name)
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name,
        generation_config=genai.types.GenerationConfig(
            temperature=0.0,
            max_output_tokens=4096,
        )
    )


def list_available_models():
    """Returns the verified available models for the sidebar."""
    return list(ALLOWED_MODELS)

# --- GLOSSARY & CORRECTIONS ---
# Common misspellings or transcription errors handled globally
GLOSSARY = {
    "Monsez": "Montacer",
    "monsez": "Montacer",
    "moncef": "Montacer",
    "Moncef": "Montacer",
    "kinza" : "kenza",
}

def clean_text_glossary(text):
    """Applies glossary corrections to any given text."""
    if not text or not isinstance(text, str):
        return text
    for wrong, right in GLOSSARY.items():
        text = text.replace(wrong, right)
    return text

# ─── GESTION DE QUOTA & RÉSILIENCE (Centralisée) ─────────────────────────────

def generate_with_retry(model_name: str, content, generation_config=None, safety_settings=None, request_options=None, max_retries=5):
    """
    Exécute un appel Gemini avec exponential backoff et rotation de modèle.
    Supporte les erreurs de quota (429), les erreurs serveur et les absences de modèle.
    """
    import time
    import streamlit as st
    from google.api_core.exceptions import ResourceExhausted, InternalServerError, ServiceUnavailable, DeadlineExceeded
    
    # Configuration par défaut si non fournie
    if generation_config is None:
        generation_config = {"temperature": 0.3}
    if request_options is None:
        request_options = {"timeout": 600}
        
    # Liste de repli basée sur les modèles réellement disponibles (diag_models.py)
    models_to_try = [
        model_name,
        "models/gemini-flash-latest",      # Backup stable #1
        "models/gemini-2.0-flash-lite",    # Backup stable #2 (lite)
        "models/gemini-pro-latest",         # Backup stable #3
    ]
    
    # Élimine les doublons tout en gardant l'ordre
    unique_models = []
    for m in models_to_try:
        if m not in unique_models: unique_models.append(m)
        
    last_exception = None
    
    for current_model_name in unique_models:
        model = genai.GenerativeModel(current_model_name)
        wait_time = 12 # Pause initiale pour quota 429
        
        for attempt in range(max_retries):
            try:
                response = model.generate_content(
                    content,
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                    request_options=request_options
                )
                return response, current_model_name
                
            except ResourceExhausted as e:
                last_exception = e
                st.warning(f"⚠️ Quota 429 ({current_model_name}). Pause de {wait_time}s... (Tentative {attempt+1}/{max_retries})")
                time.sleep(wait_time)
                wait_time *= 2 # Backoff exponentiel
                
            except (InternalServerError, ServiceUnavailable, DeadlineExceeded) as e:
                last_exception = e
                st.warning(f"⚠️ Erreur serveur {type(e).__name__}. Nouvel essai dans 5s... (Tentative {attempt+1}/{max_retries})")
                time.sleep(5)
                
            except Exception as e:
                # Si c'est un problème de "model not found" (404), on change de modèle immédiatement
                if "404" in str(e) or "not found" in str(e).lower():
                    st.warning(f"⚠️ Modèle {current_model_name} introuvable (404).")
                    break # On tente le modèle suivant

                if "safety" in str(e).lower():
                    st.error(f"❌ Blocage Safety sur {current_model_name} : {e}")
                    raise e
                
                st.warning(f"⚠️ Erreur sur {current_model_name} : {e}. Rotation...")
                break # On change de modèle
                
        if current_model_name != unique_models[-1]:
            st.info(f"🔄 Saturation détectée sur {current_model_name}. Essai du modèle suivant...")

    raise last_exception if last_exception else Exception("Échec total après retries et rotation.")
