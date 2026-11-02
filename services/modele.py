"""
services/modele.py — Modèle Gemini partagé par toutes les pages.
"""
import streamlit as st

import config


@st.cache_resource(show_spinner=False)
def _configure():
    return config.configure()


def get_model():
    """Retourne (modèle, message_erreur). Le modèle vaut None si la configuration échoue."""
    try:
        return _configure(), None
    except Exception as e:
        return None, str(e)


def model_label(model) -> str:
    return model.model_name.replace("models/", "") if model else "non configuré"
