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

_ARROW = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.5"><path d="M7 17 17 7M8 7h9v9"/></svg>'
)
_CHEVRON = (
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.5"><path d="m6 9 6 6 6-6"/></svg>'
)


@st.cache_data(show_spinner=False)
def _load_css(mtime: float) -> str:
    # mtime fait partie de la clé de cache : une modification du fichier est prise en compte
    return _CSS_PATH.read_text(encoding="utf-8")


def apply_theme():
    """Injecte la feuille de style de l'application (une fois par exécution)."""
    st.markdown(f"<style>{_load_css(_CSS_PATH.stat().st_mtime)}</style>", unsafe_allow_html=True)


def hero(title: str, phrases, text: str = "", label: str = "", index: str = ""):
    """Grand titre d'accueil avec effet machine à écrire sur 3 phrases."""
    typed = "".join(f"<span>{escape(p)}</span>" for p in phrases[:3])
    st.markdown(
        f'<section class="mi-hero">'
        f'<div class="mi-hero-top"><span class="mi-label">{escape(label)}</span>'
        f'<span class="mi-label">{escape(index)}</span></div>'
        f'<div class="mi-hero-title" role="heading" aria-level="1">{escape(title)}<span class="mi-typed">{typed}</span></div>'
        f'<div class="mi-hero-sub"><div class="mi-hero-text">{escape(text)}</div>'
        f'<div class="mi-scroll mi-label">Faire défiler {_CHEVRON}</div></div>'
        f"</section>",
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = "", eyebrow: str = "", index: str = ""):
    subtitle_html = f'<div class="mi-page-subtitle">{escape(subtitle)}</div>' if subtitle else ""
    st.markdown(
        f'<div class="mi-page-header"><div class="mi-label"><span>{escape(eyebrow)}</span>'
        f"<span>{escape(index)}</span></div>"
        f'<div class="mi-page-title">{escape(title)}</div>{subtitle_html}</div>',
        unsafe_allow_html=True,
    )


def section_header(title: str, caption: str = "", count=None, number: str = ""):
    count_html = f'<span class="mi-count">({escape(str(count))})</span>' if count is not None else ""
    caption_html = f'<div class="mi-section-caption">{escape(caption)}</div>' if caption else ""
    number_html = f'<span class="mi-label mi-section-num">{escape(number)}</span>' if number else ""
    st.markdown(
        f'<div class="mi-section">{number_html}<div><div class="mi-section-title">{escape(title)}{count_html}</div>'
        f"{caption_html}</div></div>",
        unsafe_allow_html=True,
    )


def marquee(items):
    """Bandeau défilant infini (contenu dupliqué pour une boucle sans à-coup)."""
    one = "".join(
        f'<span class="mi-marquee-item">{escape(str(i))}<span class="mi-dash">—</span></span>' for i in items
    )
    st.markdown(
        f'<div class="mi-marquee" aria-hidden="true"><div class="mi-marquee-track">{one}{one}</div></div>',
        unsafe_allow_html=True,
    )


def editorial_rows(rows):
    """Lignes façon sommaire : (numéro, catégorie, titre, date)."""
    html = "".join(
        f'<div class="mi-row"><span class="mi-label mi-row-num">{escape(num)}</span>'
        f'<div><div class="mi-label">{escape(cat)}</div><div class="mi-row-title">{escape(title)}</div></div>'
        f'<span class="mi-label mi-row-date">{escape(date)}</span>'
        f'<span class="mi-row-arrow">{_ARROW}</span></div>'
        for num, cat, title, date in rows
    )
    st.markdown(f'<div class="mi-rows">{html}</div>', unsafe_allow_html=True)


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
        f'<span class="mi-score mi-score-{level}">{rel}%</span></div>'
        f'<div class="mi-label mi-result-meta">Horodatage {escape(timestamp)}</div>'
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
        f'<div class="mi-status mi-label"><span class="mi-dot"></span>{escape(text)}</div>',
        unsafe_allow_html=True,
    )


def footer():
    st.markdown(
        '<footer class="mi-footer">'
        '<div class="mi-footer-big">Transformez vos réunions<br><span>en décisions.</span></div>'
        '<div class="mi-footer-cols">'
        '<div><div class="mi-label">Studio</div><div>Inspirigence Group</div></div>'
        '<div><div class="mi-label">Produit</div><div>Meeting Intelligence</div></div>'
        '<div><div class="mi-label">Moteur</div><div>Gemini · Power BI</div></div>'
        '<div><div class="mi-label">Accès</div><div>Administrateurs</div></div>'
        "</div></footer>",
        unsafe_allow_html=True,
    )
