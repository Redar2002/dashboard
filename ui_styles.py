"""
ui_styles.py — Design Original "Ultra Premium" (Aurora, Neon, Glassmorphism)
Usage : from ui_styles import get_css; st.markdown(get_css(), unsafe_allow_html=True)
"""


def get_css() -> str:
    return """
<style>
/* ═══════════════════════════════════════════════════════════════
   GOOGLE FONTS
═══════════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Syne:wght@600;800&display=swap');

/* ═══════════════════════════════════════════════════════════════
   ANIMATIONS
═══════════════════════════════════════════════════════════════ */
@keyframes float1 {
    0%   { transform: translate(0, 0) scale(1); }
    33%  { transform: translate(30px, -50px) scale(1.1); }
    66%  { transform: translate(-20px, 20px) scale(0.9); }
    100% { transform: translate(0, 0) scale(1); }
}

@keyframes float2 {
    0%   { transform: translate(0, 0) scale(1); }
    33%  { transform: translate(-30px, 40px) scale(1.15); }
    66%  { transform: translate(20px, -20px) scale(0.85); }
    100% { transform: translate(0, 0) scale(1); }
}

@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}

@keyframes fadeInUp {
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulseBorder {
    0% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.4); }
    70% { box-shadow: 0 0 0 8px rgba(139, 92, 246, 0); }
    100% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0); }
}

/* ═══════════════════════════════════════════════════════════════
   DESIGN TOKENS
═══════════════════════════════════════════════════════════════ */
:root {
    --c-bg: #080C14;
    --c-glass: rgba(17, 24, 39, 0.6);
    --c-glass-border: rgba(255, 255, 255, 0.08);
    --c-glass-border-hover: rgba(139, 92, 246, 0.4);
    
    --c-neon-violet: #8B5CF6;
    --c-neon-indigo: #4F46E5;
    --c-neon-fuchsia: #D946EF;
    
    --c-text: #F8FAFC;
    --c-text-muted: #94A3B8;
    
    --glow-violet: 0 0 20px rgba(139, 92, 246, 0.3);
    
    --border-radius-lg: 22px;
    --border-radius-md: 14px;
    --border-radius-sm: 8px;
    
    --transition-smooth: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

*, *::before, *::after { box-sizing: border-box; }

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
    font-size: 15px;
    color: var(--c-text);
}

/* ── AURORA BACKGROUND ─────────────────────────────────────── */
.stApp {
    background-color: var(--c-bg);
}

.stApp::before, .stApp::after {
    content: "";
    position: fixed;
    width: 60vw;
    height: 60vw;
    border-radius: 50%;
    z-index: -1;
    filter: blur(100px);
    opacity: 0.15;
    pointer-events: none;
}

.stApp::before {
    background: radial-gradient(circle, var(--c-neon-violet) 0%, transparent 70%);
    top: -20%;
    left: -10%;
    animation: float1 15s ease-in-out infinite;
}

.stApp::after {
    background: radial-gradient(circle, var(--c-neon-indigo) 0%, transparent 70%);
    bottom: -20%;
    right: -10%;
    animation: float2 18s ease-in-out infinite;
}

/* ── TYPOGRAPHY ────────────────────────────────────────────── */
h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #FFFFFF 0%, #A5B4FC 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.5));
    margin-bottom: 0.5rem !important;
}

h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #E2E8F0 !important;
}

h2 {
    font-size: 1.4rem !important;
    border-bottom: 1px solid var(--c-glass-border);
    padding-bottom: 1rem;
    margin-top: 2rem !important;
}

/* ── SIDEBAR ───────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: rgba(10, 15, 30, 0.4) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
}

/* ── METRIC CARDS ──────────────────────────────────────────── */
div[data-testid="stMetric"] {
    background: var(--c-glass);
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    border: 1px solid var(--c-glass-border);
    border-radius: var(--border-radius-lg);
    padding: 1.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    transition: var(--transition-smooth);
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px) scale(1.02);
    border-color: var(--c-glass-border-hover);
    box-shadow: var(--glow-violet);
}

div[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    color: #FFFFFF !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    text-shadow: 0 2px 10px rgba(139, 92, 246, 0.3);
}

div[data-testid="stMetricLabel"] {
    color: var(--c-text-muted) !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* ── BUTTONS (SHIMMER & NEON) ──────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%) !important;
    border: 1px solid var(--c-glass-border) !important;
    color: #E2E8F0 !important;
    border-radius: var(--border-radius-md) !important;
    padding: 0.6rem 1.2rem !important;
    font-weight: 600 !important;
    transition: var(--transition-smooth) !important;
    backdrop-filter: blur(10px);
}

.stButton > button:hover {
    border-color: var(--c-neon-violet) !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.3), inset 0 0 10px rgba(139, 92, 246, 0.1) !important;
    transform: translateY(-2px);
}

button[kind="primary"] {
    background: linear-gradient(90deg, #8B5CF6, #D946EF, #8B5CF6) !important;
    background-size: 200% auto !important;
    border: none !important;
    color: #FFFFFF !important;
    animation: shimmer 3s linear infinite !important;
    box-shadow: var(--glow-violet) !important;
}

button[kind="primary"]:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 0 25px rgba(217, 70, 239, 0.5) !important;
}

/* ── INPUTS & SELECTS ──────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox [data-baseweb="select"] > div,
.stMultiSelect [data-baseweb="select"] > div {
    background: rgba(0, 0, 0, 0.3) !important;
    border: 1px solid var(--c-glass-border) !important;
    border-radius: var(--border-radius-md) !important;
    color: #FFFFFF !important;
    transition: var(--transition-smooth) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox [data-baseweb="select"]:focus-within > div {
    border-color: var(--c-neon-violet) !important;
    box-shadow: inset 0 0 8px rgba(139, 92, 246, 0.2), 0 0 10px rgba(139, 92, 246, 0.2) !important;
}

/* ── EXPANDERS ─────────────────────────────────────────────── */
details {
    background: var(--c-glass) !important;
    border: 1px solid var(--c-glass-border) !important;
    border-radius: var(--border-radius-lg) !important;
    margin-bottom: 1rem !important;
    transition: var(--transition-smooth) !important;
}

details:hover {
    border-color: rgba(255,255,255,0.15) !important;
}

details[open] {
    border-color: var(--c-neon-violet) !important;
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.15) !important;
}

details > summary {
    font-family: 'Syne', sans-serif !important;
    color: #FFFFFF !important;
    padding: 1rem !important;
}

/* ── PROGRESS BARS ─────────────────────────────────────────── */
div[data-testid="stProgress"] > div > div > div {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 8px !important;
    height: 8px !important;
    border: 1px solid rgba(255,255,255,0.05);
}

div[data-testid="stProgress"] > div > div > div > div {
    background: linear-gradient(90deg, #4F46E5, #8B5CF6) !important;
    border-radius: 8px !important;
    height: 8px !important;
    box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
}

/* ── FILE UPLOADER ─────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--c-glass) !important;
    border: 2px dashed rgba(255,255,255,0.1) !important;
    border-radius: var(--border-radius-lg) !important;
    padding: 2rem !important;
    text-align: center !important;
    transition: var(--transition-smooth) !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--c-neon-violet) !important;
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.1) !important;
}

/* ── ALERTS ────────────────────────────────────────────────── */
div[data-testid="stInfo"], div[data-testid="stSuccess"], div[data-testid="stWarning"], div[data-testid="stError"] {
    background: var(--c-glass) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid var(--c-glass-border) !important;
    border-radius: var(--border-radius-lg) !important;
}
div[data-testid="stSuccess"] { border-left: 4px solid #10B981 !important; color: #D1FAE5 !important;}
div[data-testid="stInfo"]    { border-left: 4px solid #3B82F6 !important; color: #DBEAFE !important;}
div[data-testid="stWarning"] { border-left: 4px solid #F59E0B !important; color: #FEF3C7 !important;}
div[data-testid="stError"]   { border-left: 4px solid #EF4444 !important; color: #FEE2E2 !important;}

hr {
    border-color: rgba(255,255,255,0.05) !important;
    margin: 2.5rem 0 !important;
}
</style>
"""


def get_hero_html(icon: str, title: str, subtitle: str = "") -> str:
    """Renders a premium animated hero header."""
    sub_html = f'<p style="color:#94A3B8; font-size:1.1rem; margin-top:0.5rem; max-width:600px;">{subtitle}</p>' if subtitle else ""
    return f"""
<div style="margin-bottom: 3rem; animation: fadeInUp 0.8s ease backwards;">
    <div style="display:flex; align-items:center; gap:1.5rem;">
        <div style="
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 1.2rem;
            border-radius: 20px;
            font-size: 2.5rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            display: flex; align-items: center; justify-content: center;
        ">{icon}</div>
        <div>
            <h1 style="margin:0; padding:0; line-height:1.1;">{title}</h1>
            {sub_html}
        </div>
    </div>
</div>
"""


def get_kpi_card_html(value, label: str, icon: str = "📊", color: str = "#8B5CF6", suffix: str = "") -> str:
    """Renders a premium HTML KPI card with neon accent."""
    return f"""
<div style="
    background: rgba(17, 24, 39, 0.6);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 22px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    border-left: 4px solid {color};
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    transition: all 0.4s ease;
" onmouseover="this.style.transform='translateY(-5px) scale(1.02)'; this.style.boxShadow='0 0 20px {color}66';" 
  onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 8px 32px 0 rgba(0, 0, 0, 0.3)';">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem;">
        <div style="color:#94A3B8; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.1em;">{label}</div>
        <div style="font-size:1.5rem; filter:drop-shadow(0 0 8px {color}88);">{icon}</div>
    </div>
    <div style="font-family:'Syne', sans-serif; font-size:2.2rem; font-weight:800; color:#FFFFFF; line-height:1; text-shadow:0 2px 10px {color}33;">
        {value}<span style="font-size:1.2rem; color:#64748B; margin-left:5px; font-weight:600;">{suffix}</span>
    </div>
</div>
"""


def get_phase_bar_html(phase: str, score: int, max_score: int = 5) -> str:
    """Renders a custom colored progress bar for phase alignment."""
    pct = int((score / max_score) * 100)
    color = "#10B981" if score >= 4 else "#F59E0B" if score >= 3 else "#EF4444"
        
    return f"""
<div style="margin-bottom:1.2rem;">
    <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem;">
        <span style="color:#E2E8F0; font-weight:500;">{phase}</span>
        <span style="color:{color}; font-family:'Syne', sans-serif; font-weight:800;">{score}/{max_score}</span>
    </div>
    <div style="background:rgba(255,255,255,0.05); border-radius:8px; height:8px; overflow:hidden; border:1px solid rgba(255,255,255,0.05);">
        <div style="width:{pct}%; height:100%; background:linear-gradient(90deg, transparent, {color}); border-radius:8px; box-shadow:0 0 10px {color};"></div>
    </div>
</div>
"""


def get_model_badge_html(model_name: str) -> str:
    """Renders an animated active model badge."""
    return f"""
<div style="
    background: rgba(17, 24, 39, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1rem;
    margin-top: 1rem;
    position: relative;
    overflow: hidden;
">
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.4rem;">
        <div style="width:8px; height:8px; border-radius:50%; background:#10B981; animation:pulseBorder 2s infinite;"></div>
        <span style="color:#64748B; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em;">Modèle Actif</span>
    </div>
    <div style="color:#F8FAFC; font-family:'Syne', sans-serif; font-weight:600; font-size:0.95rem;">
        {model_name.replace('models/', '')}
    </div>
</div>
"""


def get_objection_card_html(obj: dict) -> str:
    """Renders a styled objection card with color coding."""
    colors = {
        "Prix": "#F59E0B", "Concurrent": "#EF4444", "Timing": "#8B5CF6",
        "Autorite": "#3B82F6", "Confiance": "#D946EF", "Besoin": "#10B981"
    }
    col = colors.get(obj.get("type"), "#94A3B8")
    
    return f"""
<div style="
    background: rgba(17, 24, 39, 0.6);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-left: 4px solid {col};
    border-radius: 16px;
    padding: 1.25rem;
    margin-bottom: 1rem;
">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;">
        <span style="color:{col}; font-weight:700; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.05em; text-shadow:0 0 10px {col}44;">{obj.get('type')}</span>
        <span style="background:rgba(255,255,255,0.05); padding:2px 8px; border-radius:6px; color:#94A3B8; font-size:0.75rem;">{obj.get('technique')}</span>
    </div>
    <div style="color:#F8FAFC; font-style:italic; margin-bottom:1rem; font-size:0.95rem; opacity:0.9;">"{obj.get('objection')}"</div>
    <div style="background:rgba(0,0,0,0.2); padding:1rem; border-radius:12px; border:1px solid rgba(255,255,255,0.02); color:#E2E8F0; font-size:0.9rem; line-height:1.5;">
        <strong style="color:{col};">Réponse idéale :</strong> {obj.get('reponse')}
    </div>
</div>
"""


def get_search_result_card_html(result: dict) -> str:
    """Renders a styled search result card."""
    rel = result.get('relevance', 0)
    col = "#10B981" if rel >= 80 else "#F59E0B" if rel >= 50 else "#EF4444"
    
    return f"""
<div style="
    background: rgba(17, 24, 39, 0.6);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-left: 3px solid {col};
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
" onmouseover="this.style.background='rgba(30, 41, 59, 0.6)';" onmouseout="this.style.background='rgba(17, 24, 39, 0.6)';">
    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
        <span style="color:#A5B4FC; font-weight:600; font-size:0.95rem;">{result.get('meeting_title')}</span>
        <span style="color:{col}; background:rgba({int(col[1:3],16)},{int(col[3:5],16)},{int(col[5:],16)},0.1); padding:2px 8px; border-radius:6px; font-size:0.8rem; font-weight:600;">{rel}% match</span>
    </div>
    <div style="color:#94A3B8; font-size:0.8rem; margin-bottom:1rem;">{result.get('timestamp')}</div>
    <div style="color:#E2E8F0; line-height:1.6; font-size:0.95rem;">{result.get('text')}</div>
</div>
"""


def get_section_header_html(icon: str, title: str, subtitle: str = "") -> str:
    """Renders a stylish section header with a gradient line."""
    sub = f'<div style="color:#94A3B8; font-size:0.9rem; margin-top:0.4rem;">{subtitle}</div>' if subtitle else ""
    return f"""
<div style="margin: 2.5rem 0 1.5rem 0;">
    <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.5rem;">
        <span style="font-size:1.5rem; filter:drop-shadow(0 0 8px rgba(139,92,246,0.6));">{icon}</span>
        <h2 style="margin:0; padding:0; border:none; color:#FFFFFF; font-family:'Syne', sans-serif; font-size:1.4rem;">{title}</h2>
    </div>
    <div style="height:2px; width:100%; background:linear-gradient(90deg, #8B5CF6 0%, rgba(139,92,246,0) 100%); opacity:0.5; border-radius:2px;"></div>
    {sub}
</div>
"""
