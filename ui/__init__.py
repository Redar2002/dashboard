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
def _load_css(mtime: float) -> str:
    # mtime fait partie de la clé de cache : une modification du fichier est prise en compte
    return _CSS_PATH.read_text(encoding="utf-8")


def apply_theme():
    """Injecte la feuille de style de l'application (une fois par exécution)."""
    st.markdown(f"<style>{_load_css(_CSS_PATH.stat().st_mtime)}</style>", unsafe_allow_html=True)


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


_ICONS = {
    "mic": '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><path d="M12 19v3"/>',
    "text": '<path d="M4 6h16M4 12h16M4 18h10"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/>',
}


def banner(title: str, subtitle: str, badges=()):
    """Bandeau d'accueil coloré."""
    badges_html = "".join(f'<span class="mi-badge">{escape(b)}</span>' for b in badges)
    st.markdown(
        f'<div class="mi-banner"><div class="mi-banner-title">{escape(title)}</div>'
        f'<div class="mi-banner-text">{escape(subtitle)}</div>'
        f'<div class="mi-badges">{badges_html}</div></div>',
        unsafe_allow_html=True,
    )


def kpi(label: str, value, icon: str = "text", tone: str = "violet"):
    """Carte d'indicateur avec pastille d'icône colorée."""
    svg = (
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{_ICONS.get(icon, "")}</svg>'
    )
    st.markdown(
        f'<div class="mi-kpi"><div class="mi-kpi-icon mi-tone-{escape(tone)}">{svg}</div>'
        f'<div><div class="mi-kpi-label">{escape(label)}</div>'
        f'<div class="mi-kpi-value">{escape(str(value))}</div></div></div>',
        unsafe_allow_html=True,
    )


def meeting_list(items):
    """Liste compacte : (titre, date, nombre de mots)."""
    html = "".join(
        f'<div class="mi-meeting"><div class="mi-meeting-dot"></div>'
        f'<div class="mi-meeting-main"><div class="mi-meeting-title">{escape(title)}</div>'
        f'<div class="mi-meeting-meta">{escape(date)}</div></div>'
        f'<span class="mi-meeting-words">{escape(words)}</span></div>'
        for title, date, words in items
    )
    st.markdown(f'<div class="mi-meetings">{html}</div>', unsafe_allow_html=True)
