"""
ui — Thème et composants visuels partagés par toutes les pages.
Les textes venant des utilisateurs ou de l'IA sont échappés avant d'être injectés en HTML.
"""
from html import escape
from pathlib import Path

import streamlit as st

_ROOT = Path(__file__).resolve().parent.parent
_CSS_PATH = Path(__file__).resolve().parent / "theme.css"
LOGO_PATH = str(_ROOT / "logo_inspirigence.jpg")


@st.cache_data(show_spinner=False)
def _load_css() -> str:
    return _CSS_PATH.read_text(encoding="utf-8")


def apply_theme():
    """Injecte la feuille de style de l'application (une fois par exécution)."""
    st.markdown(f"<style>{_load_css()}</style>", unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", eyebrow: str = ""):
    eyebrow_html = f'<div class="mi-eyebrow">{escape(eyebrow)}</div>' if eyebrow else ""
    subtitle_html = f'<div class="mi-page-subtitle">{escape(subtitle)}</div>' if subtitle else ""
    st.markdown(
        f'<div class="mi-page-header">{eyebrow_html}'
        f'<div class="mi-page-title">{escape(title)}</div>{subtitle_html}</div>',
        unsafe_allow_html=True,
    )


def section_header(title: str, caption: str = "", count=None):
    count_html = f' <span class="mi-count">{escape(str(count))}</span>' if count is not None else ""
    caption_html = f'<div class="mi-section-caption">{escape(caption)}</div>' if caption else ""
    st.markdown(
        f'<div class="mi-section"><div class="mi-section-title">{escape(title)}{count_html}</div>'
        f"{caption_html}</div>",
        unsafe_allow_html=True,
    )


def empty_state(title: str, text: str = ""):
    st.markdown(
        f'<div class="mi-empty"><div class="mi-empty-title">{escape(title)}</div>'
        f'<div class="mi-empty-text">{escape(text)}</div></div>',
        unsafe_allow_html=True,
    )


def tags(items):
    html = "".join(f'<span class="mi-tag">{escape(str(t))}</span>' for t in items)
    st.markdown(f'<div class="mi-tags">{html}</div>', unsafe_allow_html=True)


def search_result(meeting_title: str, timestamp: str, text: str, relevance):
    try:
        rel = int(relevance)
    except (TypeError, ValueError):
        rel = 0
    level = "high" if rel >= 80 else "mid" if rel >= 50 else "low"
    st.markdown(
        f'<div class="mi-result"><div class="mi-result-head">'
        f'<span class="mi-result-title">{escape(meeting_title)}</span>'
        f'<span class="mi-score mi-score-{level}">Pertinence {rel}%</span></div>'
        f'<div class="mi-result-meta">Horodatage {escape(timestamp)}</div>'
        f'<div class="mi-result-text">{escape(text)}</div></div>',
        unsafe_allow_html=True,
    )


def user_card(user: dict):
    name = user.get("full_name") or user.get("email", "")
    initial = escape(name[:1].upper() or "?")
    role = "Administrateur" if user.get("role") == "admin" else "Utilisateur"
    st.markdown(
        f'<div class="mi-user"><div class="mi-avatar">{initial}</div>'
        f'<div class="mi-user-info"><div class="mi-user-name">{escape(name)}</div>'
        f'<div class="mi-user-mail">{escape(role)} · {escape(user.get("email", ""))}</div></div></div>',
        unsafe_allow_html=True,
    )


def status_line(text: str):
    st.markdown(
        f'<div class="mi-status"><span class="mi-dot"></span>{escape(text)}</div>',
        unsafe_allow_html=True,
    )
