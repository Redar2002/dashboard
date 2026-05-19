import streamlit as st
import os
import sys
import base64

# Add parent directory to path to import shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils_auth

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Power BI Dashboard", page_icon="📊", layout="wide")

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
    padding-bottom: 2rem !important;
    max-width: 1600px !important;
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

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid rgba(148, 163, 184, 0.15) !important;
    margin: 1.5rem 0 !important;
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

/* ═══════════════════════════════════════════════════════════
   PAGE HEADER
   ═══════════════════════════════════════════════════════════ */
.powerbi-page-header {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 24px;
    padding: 2.5rem 2.75rem;
    margin-bottom: 2rem;
    box-shadow: 
        0 1px 3px rgba(0, 0, 0, 0.05),
        0 0 0 1px rgba(242, 200, 17, 0.05);
    display: flex;
    align-items: center;
    gap: 1.75rem;
    transition: all 0.3s ease;
}

.powerbi-page-header:hover {
    box-shadow: 
        0 4px 12px rgba(0, 0, 0, 0.08),
        0 0 0 1px rgba(242, 200, 17, 0.1);
}

.powerbi-icon-box {
    background: linear-gradient(135deg, #F2C811 0%, #E8A000 100%);
    width: 72px;
    height: 72px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 
        0 8px 24px rgba(242, 200, 17, 0.35),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    flex-shrink: 0;
}

.powerbi-title {
    background: linear-gradient(135deg, #F2C811 0%, #E8A000 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
    font-size: 2.25rem;
    margin: 0;
    line-height: 1.2;
    letter-spacing: -0.03em;
}

.powerbi-subtitle {
    color: #64748B;
    font-size: 1.05rem;
    margin-top: 0.5rem;
    line-height: 1.6;
    font-weight: 400;
}

/* ═══════════════════════════════════════════════════════════
   STATUS BADGES
   ═══════════════════════════════════════════════════════════ */
.status-badges-container {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #FFFFFF;
    border: 1.5px solid #E5E7EB;
    border-radius: 16px;
    padding: 0.75rem 1.25rem;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    transition: all 0.3s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.status-badge:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.status-badge-green {
    border-color: rgba(16, 185, 129, 0.3);
    color: #065F46;
}

.status-badge-green .badge-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 8px rgba(16, 185, 129, 0.6);
}

.status-badge-purple {
    border-color: rgba(139, 92, 246, 0.3);
    color: #5B21B6;
}

.status-badge-blue {
    border-color: rgba(59, 130, 246, 0.3);
    color: #1E40AF;
}

/* ═══════════════════════════════════════════════════════════
   POWER BI IFRAME WRAPPER
   ═══════════════════════════════════════════════════════════ */
.powerbi-wrapper {
    width: 100%;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.08),
        0 0 0 1px rgba(242, 200, 17, 0.1);
    border: 1px solid #E5E7EB;
    background: #FFFFFF;
    position: relative;
    margin-bottom: 2rem;
    transition: all 0.3s ease;
}

.powerbi-wrapper:hover {
    box-shadow: 
        0 12px 40px rgba(0, 0, 0, 0.12),
        0 0 0 1px rgba(242, 200, 17, 0.15);
}

.powerbi-header {
    background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
    border-bottom: 1px solid #E5E7EB;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.pbi-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    transition: all 0.2s ease;
}

.pbi-dot:hover {
    transform: scale(1.2);
}

.powerbi-header-text {
    margin-left: 8px;
    color: #64748B;
    font-size: 0.8rem;
    font-weight: 500;
    font-family: 'SF Mono', Monaco, monospace !important;
}

/* ═══════════════════════════════════════════════════════════
   INFO FOOTER
   ═══════════════════════════════════════════════════════════ */
.info-footer {
    background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
    border: 1.5px solid rgba(242, 200, 17, 0.2);
    border-left: 4px solid #F2C811;
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}

.info-footer svg {
    flex-shrink: 0;
    margin-top: 2px;
}

.info-footer-text {
    color: #78350F;
    font-size: 0.9rem;
    line-height: 1.7;
    font-weight: 500;
}

.info-footer-text strong {
    color: #92400E;
    font-weight: 700;
}

/* ═══════════════════════════════════════════════════════════
   ANIMATIONS
   ═══════════════════════════════════════════════════════════ */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-in {
    animation: fadeInUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

.animate-delay-1 {
    animation-delay: 0.1s;
}

.animate-delay-2 {
    animation-delay: 0.2s;
}

.animate-delay-3 {
    animation-delay: 0.3s;
}

.animate-delay-4 {
    animation-delay: 0.4s;
}

.animate-delay-5 {
    animation-delay: 0.5s;
}

/* ═══════════════════════════════════════════════════════════
   DIVIDERS
   ═══════════════════════════════════════════════════════════ */
hr {
    border: none !important;
    border-top: 1px solid #E5E7EB !important;
    margin: 2rem 0 !important;
}

/* ═══════════════════════════════════════════════════════════
   CAPTIONS
   ═══════════════════════════════════════════════════════════ */
.stCaption {
    color: #94A3B8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ═══════════════════════════════════════════════════════════
   RESPONSIVE
   ═══════════════════════════════════════════════════════════ */
@media (max-width: 768px) {
    .powerbi-page-header {
        flex-direction: column;
        text-align: center;
        padding: 2rem 1.5rem;
    }
    
    .powerbi-icon-box {
        width: 64px;
        height: 64px;
    }
    
    .powerbi-title {
        font-size: 1.75rem;
    }
    
    .status-badges-container {
        flex-direction: column;
        gap: 0.75rem;
    }
    
    .status-badge {
        justify-content: center;
    }
    
    .info-footer {
        flex-direction: column;
    }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Logo Sidebar
# -------------------------
try:
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo_inspirigence.jpg")
    with open(logo_path, "rb") as f:
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
    utils_auth.render_user_sidebar()

# -------------------------
# MAIN PAGE
# -------------------------

# Hero Header
st.markdown("""
<div class="powerbi-page-header animate-in">
    <div class="powerbi-icon-box">
        <svg width="36" height="36" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="6" y="18" width="4" height="8" rx="1.5" fill="#FFFFFF"/>
            <rect x="14" y="12" width="4" height="14" rx="1.5" fill="#FFFFFF"/>
            <rect x="22" y="6" width="4" height="20" rx="1.5" fill="#FFFFFF"/>
            <path d="M8 10 L14 7 L20 9 L26 4" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="26" cy="4" r="2.5" fill="#FFFFFF"/>
        </svg>
    </div>
    <div>
        <div class="powerbi-title">Power BI Dashboard</div>
        <div class="powerbi-subtitle">Visualisation interactive des données commerciales — Propulsé par Microsoft Power BI</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Status Badges
st.markdown("""
<div class="status-badges-container">
    <div class="status-badge status-badge-green animate-in animate-delay-1">
        <div class="badge-dot"></div>
        Rapport connecté
    </div>
    <div class="status-badge status-badge-purple animate-in animate-delay-2">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="2.5">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
        </svg>
        Authentification automatique
    </div>
    <div class="status-badge status-badge-blue animate-in animate-delay-3">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2.5">
            <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>
        </svg>
        Plein écran disponible
    </div>
</div>
""", unsafe_allow_html=True)

# Power BI Iframe
st.markdown("""
<div class="powerbi-wrapper animate-in animate-delay-4">
    <div class="powerbi-header">
        <div class="pbi-dot" style="background:#EF4444;"></div>
        <div class="pbi-dot" style="background:#F59E0B;"></div>
        <div class="pbi-dot" style="background:#10B981;"></div>
        <span class="powerbi-header-text">
            app.powerbi.com — Rapport interactif
        </span>
    </div>
    <iframe
        title="power"
        width="100%"
        height="720"
        src="https://app.powerbi.com/reportEmbed?reportId=b5d118c4-3dcc-4b39-8a97-9147e1807410&autoAuth=true&ctid=993f3397-d964-4599-8045-90049af66354&actionBarEnabled=true"
        frameborder="0"
        allowFullScreen="true"
        style="display: block; border: none;"
    ></iframe>
</div>
""", unsafe_allow_html=True)

# Info Footer
st.markdown("""
<div class="info-footer animate-in animate-delay-5">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="10" stroke="#F2C811" stroke-width="2.5"/>
        <path d="M12 8v4M12 16h.01" stroke="#F2C811" stroke-width="2.5" stroke-linecap="round"/>
    </svg>
    <div class="info-footer-text">
        Ce rapport est alimenté en temps réel par les données SQL Server.
        Utilisez les filtres interactifs directement dans le rapport Power BI.
        En cas de problème d'affichage, vérifiez que vous avez accès au tenant <strong>993f3397-d964-4599-8045-90049af66354</strong>.
    </div>
</div>
""", unsafe_allow_html=True)