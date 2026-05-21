"""
utils_auth.py — INSPIRIGENCE ULTRA PREMIUM PRO MAX
🚀 REDESIGN COMPLET - MODE PHONE RÉVOLUTIONNAIRE
"""
import streamlit as st
import os
import base64
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import auth

_SESSION_USER_KEY = "_auth_user"
_SESSION_LOGGEDIN = "_auth_logged_in"

# ══════════════════════════════════════════════════════════════════════════════
# 🎨 CSS RÉVOLUTIONNAIRE - FULL RESPONSIVE MAGIC
# ══════════════════════════════════════════════════════════════════════════════

_LOGIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700;800&display=swap');

*, *::before, *::after {
    box-sizing: border-box !important;
    margin: 0 !important;
    padding: 0 !important;
}

:root {
    --primary: #7C3AED;
    --primary-light: #8B5CF6;
    --primary-lighter: #A78BFA;
    --secondary: #D946EF;
    --accent: #EC4899;
    --accent-light: #F472B6;
    --dark-bg: #0A0118;
    --dark-bg-light: #1A0F2E;
    --dark-bg-card: #1E1B3C;
    --light-bg: #F8FAFB;
    --light-bg-alt: #F1F4F9;
    --light-text: #F8FAFC;
    --dark-text: #0F172A;
    --gray-50: #F9FAFB;
    --gray-100: #F3F4F6;
    --gray-200: #E5E7EB;
    --gray-300: #D1D5DB;
    --gray-400: #9CA3AF;
    --gray-500: #6B7280;
    --gray-600: #4B5563;
    --gray-700: #374151;
    --gray-800: #1F2937;
    --gray-900: #111827;
    --success: #10B981;
    --warning: #F59E0B;
    --error: #EF4444;
    --transition-fast: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-base: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    --spring: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

html, body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-weight: 400;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
    overflow-x: hidden !important;
    width: 100% !important;
    height: 100% !important;
}

#MainMenu, footer, header {
    display: none !important;
}

[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🌌 BACKGROUND ANIMATE */
/* ════════════════════════════════════════════════════════════════════════════ */

.stApp {
    width: 100% !important;
    min-height: 100vh !important;
    background: #0A0118 !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow-x: hidden !important;
    position: relative !important;
    display: flex !important;
    flex-direction: column !important;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background: 
        radial-gradient(circle at 15% 20%, rgba(124, 58, 237, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 85% 80%, rgba(217, 70, 239, 0.12) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.08) 0%, transparent 60%),
        radial-gradient(circle at 30% 70%, rgba(236, 72, 153, 0.1) 0%, transparent 45%);
    pointer-events: none;
    z-index: 1;
    animation: meshPulse 12s ease-in-out infinite;
}

@keyframes meshPulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 !important;
    position: relative !important;
    z-index: 2 !important;
    min-height: 100vh !important;
    display: grid !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🎬 KEYFRAMES MAGIQUES */
/* ════════════════════════════════════════════════════════════════════════════ */

@keyframes slideInLeft {
    0% {
        opacity: 0;
        transform: translateX(-100px) scale(0.95);
        filter: blur(10px);
    }
    100% {
        opacity: 1;
        transform: translateX(0) scale(1);
        filter: blur(0);
    }
}

@keyframes slideInRight {
    0% {
        opacity: 0;
        transform: translateX(100px) scale(0.95);
        filter: blur(10px);
    }
    100% {
        opacity: 1;
        transform: translateX(0) scale(1);
        filter: blur(0);
    }
}

@keyframes slideInDown {
    0% {
        opacity: 0;
        transform: translateY(-100px) scale(0.95);
        filter: blur(10px);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
        filter: blur(0);
    }
}

@keyframes slideInUp {
    0% {
        opacity: 0;
        transform: translateY(30px);
        filter: blur(5px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
        filter: blur(0);
    }
}

@keyframes fadeInUp {
    0% {
        opacity: 0;
        transform: translateY(30px);
        filter: blur(5px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
        filter: blur(0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

@keyframes iconPop {
    0% { transform: scale(0.8); opacity: 0; }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); opacity: 1; }
}

@keyframes checkmarkDraw {
    0% {
        stroke-dashoffset: 100;
        opacity: 0;
    }
    50% {
        opacity: 1;
    }
    100% {
        stroke-dashoffset: 0;
        opacity: 1;
    }
}

@keyframes successPulse {
    0% {
        transform: scale(0.8);
        opacity: 0;
    }
    50% {
        transform: scale(1.05);
    }
    100% {
        transform: scale(1);
        opacity: 1;
    }
}

@keyframes lds-ring {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes glow {
    0%, 100% {
        box-shadow: 
            0 0 20px rgba(124, 58, 237, 0.4),
            0 0 40px rgba(124, 58, 237, 0.2);
    }
    50% {
        box-shadow: 
            0 0 30px rgba(124, 58, 237, 0.6),
            0 0 60px rgba(124, 58, 237, 0.3);
    }
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 📐 LAYOUT PRINCIPAL */
/* ════════════════════════════════════════════════════════════════════════════ */

[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
    align-items: stretch !important;
    width: 100% !important;
    min-height: 100vh !important;
    position: relative !important;
    z-index: 10 !important;
    padding: 0 !important;
    margin: 0 !important;
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    grid-auto-flow: row !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🎨 PANEL GAUCHE - FORM */
/* ════════════════════════════════════════════════════════════════════════════ */

[data-testid="stColumn"]:nth-child(1) {
    background: 
        linear-gradient(135deg, 
            rgba(248, 250, 251, 0.98) 0%, 
            rgba(241, 244, 249, 0.95) 50%,
            rgba(248, 250, 251, 0.98) 100%
        ) !important;
    padding: 0 !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    z-index: 20 !important;
    animation: slideInLeft 0.9s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 
        4px 0 60px rgba(0, 0, 0, 0.08),
        inset -1px 0 0 rgba(124, 58, 237, 0.1) !important;
    width: 100% !important;
    height: auto !important;
    min-height: 100vh !important;
}

[data-testid="stColumn"]:nth-child(1)::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: 
        radial-gradient(circle at 20% 30%, rgba(124, 58, 237, 0.03) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, rgba(217, 70, 239, 0.02) 0%, transparent 50%),
        url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%237C3AED' fill-opacity='0.015'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 1;
}

[data-testid="stColumn"]:nth-child(1)::after {
    content: '';
    position: absolute;
    top: 0;
    left: 10%;
    right: 10%;
    height: 2px;
    background: linear-gradient(90deg, 
        transparent, 
        rgba(124, 58, 237, 0.3) 20%, 
        rgba(217, 70, 239, 0.3) 80%, 
        transparent
    );
    animation: fadeIn 1s ease-out 0.5s both;
    box-shadow: 0 0 20px rgba(124, 58, 237, 0.4);
}

[data-testid="stColumn"]:nth-child(1) > [data-testid="stVerticalBlock"] {
    padding: 3rem 2.5rem !important;
    max-width: 500px !important;
    width: 100% !important;
    position: relative !important;
    z-index: 1 !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🏷️ LOGO */
/* ════════════════════════════════════════════════════════════════════════════ */

.insp-logo {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    color: var(--dark-text) !important;
    letter-spacing: -0.03em !important;
    margin-bottom: 2rem !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    animation: fadeInUp 0.6s ease-out !important;
    position: relative !important;
    padding: 1rem 1.5rem !important;
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.9), 
        rgba(248, 250, 252, 0.7)
    ) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(124, 58, 237, 0.15) !important;
    box-shadow: 
        0 4px 12px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
}

.insp-logo::before {
    content: '' !important;
    width: 10px !important;
    height: 10px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    box-shadow: 
        0 0 20px rgba(124, 58, 237, 0.6),
        0 2px 8px rgba(124, 58, 237, 0.3) !important;
    animation: pulse 2s ease-in-out infinite !important;
}

.insp-logo em {
    font-style: italic !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
    background-size: 200% 200% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    animation: shimmer 4s linear infinite !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🔒 BADGE */
/* ════════════════════════════════════════════════════════════════════════════ */

.insp-auth-badge {
    display: inline-flex !important;
    align-items: center !important;
    gap: 10px !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--primary) !important;
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 0.12), 
        rgba(139, 92, 246, 0.08)
    ) !important;
    border: 1.5px solid rgba(124, 58, 237, 0.25) !important;
    border-radius: 100px !important;
    padding: 10px 18px !important;
    margin-bottom: 1.5rem !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    box-shadow: 
        0 4px 12px rgba(124, 58, 237, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    transition: var(--transition-base) !important;
    animation: fadeInUp 0.6s ease-out 0.1s both !important;
    position: relative !important;
    overflow: hidden !important;
}

.insp-auth-badge::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.2), 
        transparent
    ) !important;
    opacity: 0 !important;
    transition: opacity 0.3s !important;
}

.insp-auth-badge:hover {
    border-color: rgba(124, 58, 237, 0.5) !important;
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 0.18), 
        rgba(139, 92, 246, 0.12)
    ) !important;
    box-shadow: 
        0 6px 16px rgba(124, 58, 237, 0.2),
        0 0 30px rgba(124, 58, 237, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
    transform: scale(1.05) translateY(-2px) !important;
}

.insp-auth-badge:hover::before {
    opacity: 1 !important;
}

.insp-auth-badge-icon {
    font-size: 0.9rem !important;
    animation: iconPop 0.6s var(--spring) 0.2s both !important;
}

.insp-auth-badge-dot {
    width: 6px !important;
    height: 6px !important;
    background: var(--success) !important;
    border-radius: 50% !important;
    box-shadow: 
        0 0 10px rgba(16, 185, 129, 0.6),
        0 0 20px rgba(16, 185, 129, 0.3) !important;
    animation: pulse 2s ease-in-out infinite !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 📝 TYPOGRAPHY */
/* ════════════════════════════════════════════════════════════════════════════ */

.insp-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    color: var(--dark-text) !important;
    letter-spacing: -0.04em !important;
    line-height: 1.15 !important;
    margin-bottom: 1rem !important;
    animation: fadeInUp 0.6s ease-out 0.2s both !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.02) !important;
}

.insp-title-gradient {
    background: linear-gradient(135deg, 
        var(--primary) 0%, 
        var(--secondary) 50%, 
        var(--accent) 100%
    ) !important;
    background-size: 300% 300% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    animation: shimmer 5s linear infinite !important;
    position: relative !important;
}

.insp-subtitle {
    font-size: 0.95rem !important;
    color: var(--gray-600) !important;
    line-height: 1.7 !important;
    margin-bottom: 2rem !important;
    font-weight: 400 !important;
    animation: fadeInUp 0.6s ease-out 0.3s both !important;
}

.insp-divider {
    height: 1px !important;
    background: linear-gradient(90deg, 
        transparent, 
        var(--gray-300) 20%, 
        var(--gray-300) 80%, 
        transparent
    ) !important;
    margin: 2rem 0 !important;
    animation: fadeInUp 0.6s ease-out 0.4s both !important;
    position: relative !important;
}

.insp-divider::after {
    content: '' !important;
    position: absolute !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    width: 8px !important;
    height: 8px !important;
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    border-radius: 50% !important;
    box-shadow: 
        0 0 12px rgba(124, 58, 237, 0.5),
        0 0 24px rgba(124, 58, 237, 0.3) !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 📧 INPUTS */
/* ════════════════════════════════════════════════════════════════════════════ */

.stTextInput {
    animation: fadeInUp 0.6s ease-out 0.5s both !important;
    margin-bottom: 1.5rem !important;
}

.stTextInput > label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--gray-700) !important;
    margin-bottom: 0.7rem !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}

.stTextInput > div > div > input {
    height: 56px !important;
    border-radius: 14px !important;
    border: 2px solid var(--gray-200) !important;
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.95), 
        rgba(248, 250, 252, 0.85)
    ) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    padding: 16px 20px !important;
    font-size: 0.95rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    color: var(--dark-text) !important;
    transition: var(--transition-base) !important;
    box-shadow: 
        0 2px 8px rgba(0, 0, 0, 0.04),
        inset 0 1px 2px rgba(255, 255, 255, 0.9) !important;
    width: 100% !important;
}

.stTextInput > div > div > input::placeholder {
    color: var(--gray-400) !important;
    font-weight: 400 !important;
}

.stTextInput > div > div > input:focus {
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 1), 
        rgba(248, 250, 252, 0.95)
    ) !important;
    border-color: var(--primary) !important;
    box-shadow:
        0 0 0 4px rgba(124, 58, 237, 0.1),
        0 8px 24px rgba(124, 58, 237, 0.2),
        inset 0 1px 3px rgba(255, 255, 255, 1) !important;
    outline: none !important;
    transform: translateY(-2px) scale(1.005) !important;
}

.stTextInput > div > div > input:hover {
    border-color: var(--gray-300) !important;
    box-shadow: 
        0 4px 12px rgba(0, 0, 0, 0.06),
        inset 0 1px 2px rgba(255, 255, 255, 0.9) !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🔘 BUTTON */
/* ════════════════════════════════════════════════════════════════════════════ */

.stButton {
    animation: fadeInUp 0.6s ease-out 0.6s both !important;
    width: 100% !important;
}

.stButton > button {
    width: 100% !important;
    height: 56px !important;
    border-radius: 14px !important;
    border: none !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.05em !important;
    color: #fff !important;
    background: linear-gradient(135deg, 
        var(--primary) 0%, 
        var(--primary-light) 50%, 
        var(--secondary) 100%
    ) !important;
    background-size: 200% 200% !important;
    box-shadow: 
        0 8px 24px rgba(124, 58, 237, 0.35),
        0 0 0 0 rgba(124, 58, 237, 0) !important;
    transition: var(--transition-base) !important;
    margin-top: 1.5rem !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
    text-transform: uppercase !important;
}

.stButton > button::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.25), 
        transparent
    ) !important;
    opacity: 0 !important;
    transition: opacity 0.3s !important;
    z-index: 1 !important;
}

.stButton > button::after {
    content: '' !important;
    position: absolute !important;
    top: 50% !important;
    left: 50% !important;
    width: 0 !important;
    height: 0 !important;
    border-radius: 50% !important;
    background: rgba(255, 255, 255, 0.3) !important;
    transform: translate(-50%, -50%) !important;
    transition: width 0.6s, height 0.6s !important;
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.01) !important;
    box-shadow: 
        0 12px 32px rgba(124, 58, 237, 0.45),
        0 0 40px rgba(124, 58, 237, 0.3),
        0 0 0 4px rgba(124, 58, 237, 0.1) !important;
    background-position: 100% 0 !important;
}

.stButton > button:hover::before {
    opacity: 1 !important;
}

.stButton > button:hover::after {
    width: 300px !important;
    height: 300px !important;
    opacity: 0 !important;
}

.stButton > button:active {
    transform: translateY(-1px) scale(0.98) !important;
    box-shadow: 
        0 4px 12px rgba(124, 58, 237, 0.3),
        inset 0 2px 8px rgba(0, 0, 0, 0.2) !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* ⚠️ ALERTS */
/* ════════════════════════════════════════════════════════════════════════════ */

div[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    margin: 1.5rem 0 !important;
    border-left: 4px solid !important;
    padding: 16px 20px !important;
    backdrop-filter: blur(10px) !important;
    animation: slideInUp 0.5s var(--spring) !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🏷️ FOOTER */
/* ════════════════════════════════════════════════════════════════════════════ */

.insp-footer {
    margin-top: 2.5rem !important;
    text-align: center !important;
    animation: fadeInUp 0.6s ease-out 0.7s both !important;
}

.insp-badge {
    display: inline-flex !important;
    align-items: center !important;
    gap: 10px !important;
    font-size: 0.7rem !important;
    color: var(--primary) !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 0.1), 
        rgba(139, 92, 246, 0.05)
    ) !important;
    border: 1.5px solid rgba(124, 58, 237, 0.3) !important;
    border-radius: 100px !important;
    padding: 10px 20px !important;
    margin-bottom: 16px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    backdrop-filter: blur(10px) !important;
    transition: var(--transition-base) !important;
    box-shadow: 0 2px 8px rgba(124, 58, 237, 0.1) !important;
}

.insp-badge::before {
    content: '' !important;
    width: 6px !important;
    height: 6px !important;
    background: var(--success) !important;
    border-radius: 50% !important;
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.6) !important;
    animation: pulse 2s ease-in-out infinite !important;
}

.insp-badge:hover {
    border-color: rgba(124, 58, 237, 0.6) !important;
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 0.15), 
        rgba(139, 92, 246, 0.08)
    ) !important;
    box-shadow: 
        0 4px 12px rgba(124, 58, 237, 0.2),
        0 0 20px rgba(124, 58, 237, 0.15) !important;
    transform: scale(1.05) translateY(-2px) !important;
}

.insp-footer p {
    font-size: 0.8rem !important;
    color: var(--gray-600) !important;
    line-height: 1.6 !important;
    font-weight: 400 !important;
    margin: 0 !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🎨 PANEL DROIT - BRANDING */
/* ════════════════════════════════════════════════════════════════════════════ */

[data-testid="stColumn"]:nth-child(2) {
    padding: 0 !important;
    background: transparent !important;
    position: relative !important;
    animation: slideInRight 0.9s cubic-bezier(0.4, 0, 0.2, 1) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    overflow: hidden !important;
    width: 100% !important;
    height: auto !important;
    min-height: 100vh !important;
}

[data-testid="stColumn"]:nth-child(2) > [data-testid="stVerticalBlock"] {
    padding: 3.5rem 3rem !important;
    max-width: 680px !important;
    width: 100% !important;
}

.insp-panel-right {
    position: relative !important;
    z-index: 10 !important;
}

.insp-brand-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    color: var(--light-text) !important;
    line-height: 1.15 !important;
    letter-spacing: -0.04em !important;
    margin-bottom: 1.8rem !important;
    text-shadow: 
        0 4px 20px rgba(0, 0, 0, 0.4),
        0 0 40px rgba(124, 58, 237, 0.3) !important;
    animation: fadeInUp 0.6s ease-out 0.2s both !important;
}

.insp-brand-title span {
    background: linear-gradient(135deg, 
        #EC4899 0%, 
        #D946EF 50%, 
        #A78BFA 100%
    ) !important;
    background-size: 300% 300% !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    animation: shimmer 5s linear infinite !important;
}

.insp-brand-desc {
    font-size: 1rem !important;
    color: rgba(248, 250, 252, 0.85) !important;
    font-weight: 400 !important;
    line-height: 1.8 !important;
    margin-bottom: 3rem !important;
    animation: fadeInUp 0.6s ease-out 0.3s both !important;
}

.insp-features {
    display: flex !important;
    flex-direction: column !important;
    gap: 1.2rem !important;
}

.insp-feat {
    display: flex !important;
    align-items: flex-start !important;
    gap: 1.2rem !important;
    padding: 1.5rem !important;
    border-radius: 18px !important;
    background: linear-gradient(135deg, 
        rgba(30, 27, 60, 0.7), 
        rgba(26, 15, 46, 0.5)
    ) !important;
    border: 1px solid rgba(139, 92, 246, 0.25) !important;
    backdrop-filter: blur(30px) !important;
    -webkit-backdrop-filter: blur(30px) !important;
    transition: var(--transition-base) !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
}

.insp-feat:nth-child(1) { animation: fadeInUp 0.6s ease-out 0.4s both !important; }
.insp-feat:nth-child(2) { animation: fadeInUp 0.6s ease-out 0.5s both !important; }
.insp-feat:nth-child(3) { animation: fadeInUp 0.6s ease-out 0.6s both !important; }
.insp-feat:nth-child(4) { animation: fadeInUp 0.6s ease-out 0.7s both !important; }

.insp-feat::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 0.15), 
        rgba(217, 70, 239, 0.05)
    ) !important;
    opacity: 0 !important;
    transition: opacity 0.4s !important;
}

.insp-feat:hover {
    background: linear-gradient(135deg, 
        rgba(30, 27, 60, 0.9), 
        rgba(26, 15, 46, 0.7)
    ) !important;
    border-color: rgba(124, 58, 237, 0.5) !important;
    transform: translateX(16px) translateY(-6px) scale(1.02) !important;
    box-shadow: 
        0 12px 32px rgba(0, 0, 0, 0.4),
        0 0 40px rgba(124, 58, 237, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
}

.insp-feat:hover::before {
    opacity: 1 !important;
}

.insp-feat-icon {
    width: 50px !important;
    height: 50px !important;
    border-radius: 14px !important;
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 0.3), 
        rgba(139, 92, 246, 0.2)
    ) !important;
    border: 1px solid rgba(139, 92, 246, 0.4) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1.5rem !important;
    flex-shrink: 0 !important;
    backdrop-filter: blur(10px) !important;
    transition: var(--transition-base) !important;
    box-shadow: 
        0 4px 12px rgba(124, 58, 237, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    animation: iconPop 0.6s var(--spring) !important;
}

.insp-feat:hover .insp-feat-icon {
    transform: scale(1.15) rotate(10deg) !important;
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 0.5), 
        rgba(139, 92, 246, 0.3)
    ) !important;
    box-shadow: 
        0 8px 24px rgba(124, 58, 237, 0.4),
        0 0 40px rgba(124, 58, 237, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}

.insp-feat strong {
    display: block !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: var(--light-text) !important;
    margin-bottom: 0.4rem !important;
    letter-spacing: 0.01em !important;
}

.insp-feat span {
    font-size: 0.85rem !important;
    color: rgba(248, 250, 252, 0.7) !important;
    font-weight: 400 !important;
    line-height: 1.6 !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🎉 SUCCESS OVERLAY */
/* ════════════════════════════════════════════════════════════════════════════ */

.success-overlay {
    position: fixed !important;
    inset: 0 !important;
    background: rgba(0, 0, 0, 0.5) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    z-index: 9999 !important;
    animation: fadeIn 0.3s ease-out !important;
}

.success-card {
    background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%) !important;
    border: 2px solid #22c55e !important;
    border-radius: 24px !important;
    padding: 60px 45px !important;
    text-align: center !important;
    max-width: 480px !important;
    box-shadow: 
        0 25px 60px rgba(0, 0, 0, 0.3),
        0 0 60px rgba(34, 197, 94, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
    animation: successPulse 0.6s var(--spring) !important;
}

.success-icon {
    width: 80px !important;
    height: 80px !important;
    margin: 0 auto 30px !important;
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    animation: float 2s ease-in-out infinite !important;
    box-shadow: 
        0 10px 30px rgba(34, 197, 94, 0.4),
        inset 0 2px 0 rgba(255, 255, 255, 0.3) !important;
}

.checkmark {
    width: 50px !important;
    height: 50px !important;
    stroke: white !important;
    stroke-width: 3 !important;
    stroke-linecap: round !important;
    stroke-linejoin: round !important;
    fill: none !important;
    animation: checkmarkDraw 0.8s cubic-bezier(0.4, 0, 0.2, 1) 0.2s both !important;
    stroke-dasharray: 100 !important;
}

.success-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    color: var(--dark-text) !important;
    margin-bottom: 12px !important;
    animation: fadeInUp 0.6s ease-out 0.4s both !important;
}

.success-subtitle {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    color: var(--gray-600) !important;
    line-height: 1.6 !important;
    margin-bottom: 28px !important;
    animation: fadeInUp 0.6s ease-out 0.5s both !important;
}

.success-details {
    background: rgba(34, 197, 94, 0.1) !important;
    border: 1px solid rgba(34, 197, 94, 0.3) !important;
    border-radius: 14px !important;
    padding: 18px !important;
    margin-bottom: 28px !important;
    animation: fadeInUp 0.6s ease-out 0.6s both !important;
    box-shadow: 0 2px 8px rgba(34, 197, 94, 0.1) !important;
}

.success-details p {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    color: var(--dark-text) !important;
    margin: 0 !important;
    font-weight: 500 !important;
}

.loading-ring {
    display: inline-block !important;
    position: relative !important;
    width: 30px !important;
    height: 30px !important;
    margin-right: 10px !important;
}

.loading-ring::after {
    content: "" !important;
    display: block !important;
    width: 24px !important;
    height: 24px !important;
    margin: 3px !important;
    border-radius: 50% !important;
    border: 3px solid #22c55e !important;
    border-color: #22c55e transparent transparent transparent !important;
    animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite !important;
}

.success-loading {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 10px !important;
    font-family: 'Inter', sans-serif !important;
    color: #22c55e !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 📱 RESPONSIVE MAGIC */
/* ════════════════════════════════════════════════════════════════════════════ */

/* ÉCRAN MOYEN - 1200px */
@media (max-width: 1200px) {
    .insp-brand-title {
        font-size: 2.3rem !important;
    }
    
    .insp-title {
        font-size: 2.2rem !important;
    }

    [data-testid="stColumn"]:nth-child(1) > [data-testid="stVerticalBlock"] {
        padding: 2.5rem 1.8rem !important;
    }

    [data-testid="stColumn"]:nth-child(2) > [data-testid="stVerticalBlock"] {
        padding: 2.5rem 2rem !important;
    }
}

/* TABLET - 1024px - LE POINT CRITIQUE */
@media (max-width: 1024px) {
    [data-testid="stHorizontalBlock"] {
        grid-template-columns: 1fr !important;
        min-height: auto !important;
        max-height: none !important;
    }

    [data-testid="stColumn"]:nth-child(1) {
        min-height: auto !important;
        box-shadow: none !important;
        padding: 0 !important;
        background: 
            linear-gradient(135deg, 
                rgba(248, 250, 251, 0.98) 0%, 
                rgba(241, 244, 249, 0.95) 100%
            ) !important;
        animation: slideInDown 0.9s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    [data-testid="stColumn"]:nth-child(1) > [data-testid="stVerticalBlock"] {
        padding: 3rem 2.5rem !important;
        max-width: 100% !important;
    }

    [data-testid="stColumn"]:nth-child(2) {
        display: flex !important;
        background: rgba(0, 0, 0, 0.3) !important;
        animation: slideInUp 0.9s cubic-bezier(0.4, 0, 0.2, 1) !important;
        min-height: auto !important;
        padding: 0 !important;
    }

    [data-testid="stColumn"]:nth-child(2) > [data-testid="stVerticalBlock"] {
        padding: 3rem 2.5rem !important;
        max-width: 100% !important;
    }

    .insp-title {
        font-size: 2rem !important;
    }

    .insp-brand-title {
        font-size: 2rem !important;
        text-align: center !important;
        margin-bottom: 1.5rem !important;
    }

    .insp-brand-desc {
        text-align: center !important;
        margin-bottom: 2rem !important;
    }

    .insp-features {
        gap: 1rem !important;
    }

    .insp-feat {
        flex-direction: row !important;
        align-items: center !important;
        padding: 1.2rem !important;
        gap: 1.2rem !important;
    }

    .insp-feat-icon {
        width: 50px !important;
        height: 50px !important;
        font-size: 1.5rem !important;
        margin: 0 !important;
        flex-shrink: 0 !important;
    }

    .insp-feat > div {
        text-align: left !important;
        flex: 1 !important;
    }

    .insp-feat strong {
        text-align: left !important;
    }

    .insp-feat span {
        text-align: left !important;
    }

    .insp-footer {
        margin-top: 2rem !important;
    }
}

/* SMALL TABLET - 768px */
@media (max-width: 768px) {
    [data-testid="stHorizontalBlock"] {
        grid-template-columns: 1fr !important;
    }

    [data-testid="stColumn"]:nth-child(1) > [data-testid="stVerticalBlock"] {
        padding: 2rem 1.5rem !important;
        max-width: 100% !important;
    }

    [data-testid="stColumn"]:nth-child(2) > [data-testid="stVerticalBlock"] {
        padding: 2rem 1.5rem !important;
    }

    .insp-logo {
        font-size: 1.3rem !important;
        padding: 0.8rem 1.2rem !important;
        margin-bottom: 1.5rem !important;
    }

    .insp-title {
        font-size: 1.8rem !important;
        margin-bottom: 0.8rem !important;
    }

    .insp-subtitle {
        font-size: 0.9rem !important;
        margin-bottom: 1.5rem !important;
    }

    .insp-auth-badge {
        font-size: 0.65rem !important;
        padding: 8px 14px !important;
    }

    .stTextInput > label {
        font-size: 0.7rem !important;
    }

    .stTextInput > div > div > input {
        height: 52px !important;
        padding: 14px 16px !important;
        font-size: 0.9rem !important;
    }

    .stButton > button {
        height: 52px !important;
        font-size: 0.9rem !important;
    }

    .insp-brand-title {
        font-size: 1.8rem !important;
    }

    .insp-brand-desc {
        font-size: 0.9rem !important;
    }

    .insp-feat {
        padding: 1rem !important;
        gap: 1rem !important;
        flex-direction: row !important;
        align-items: center !important;
    }

    .insp-feat > div {
        text-align: left !important;
        flex: 1 !important;
    }

    .insp-feat-icon {
        width: 44px !important;
        height: 44px !important;
        font-size: 1.3rem !important;
        margin: 0 !important;
        flex-shrink: 0 !important;
    }

    .insp-footer p {
        font-size: 0.75rem !important;
    }
}

/* PHONE PORTRAIT - 480px - ULTRA COMPACT */
@media (max-width: 480px) {
    .stApp {
        min-height: 100vh !important;
        display: flex !important;
        flex-direction: column !important;
    }

    [data-testid="stHorizontalBlock"] {
        grid-template-columns: 1fr !important;
        min-height: auto !important;
        max-height: auto !important;
    }

    [data-testid="stColumn"]:nth-child(1) {
        min-height: auto !important;
        box-shadow: none !important;
        padding: 1.5rem 1rem !important;
    }

    [data-testid="stColumn"]:nth-child(1) > [data-testid="stVerticalBlock"] {
        padding: 1.5rem 0 !important;
        max-width: 100% !important;
    }

    [data-testid="stColumn"]:nth-child(2) {
        display: flex !important;
        padding: 2rem 1rem !important;
        min-height: auto !important;
    }

    [data-testid="stColumn"]:nth-child(2) > [data-testid="stVerticalBlock"] {
        padding: 0 !important;
        max-width: 100% !important;
    }

    .insp-logo {
        font-size: 1.1rem !important;
        padding: 0.6rem 1rem !important;
        margin-bottom: 1.2rem !important;
        width: 100% !important;
        justify-content: center !important;
    }

    .insp-logo::before {
        width: 8px !important;
        height: 8px !important;
    }

    .insp-title {
        font-size: 1.6rem !important;
        line-height: 1.2 !important;
        margin-bottom: 0.8rem !important;
        text-align: center !important;
    }

    .insp-subtitle {
        font-size: 0.85rem !important;
        margin-bottom: 1.2rem !important;
        text-align: center !important;
        line-height: 1.6 !important;
    }

    .insp-auth-badge {
        font-size: 0.6rem !important;
        padding: 6px 12px !important;
        justify-content: center !important;
        width: 100% !important;
        margin: 0 auto 1.2rem !important;
        display: flex !important;
    }

    .insp-divider {
        margin: 1.5rem 0 !important;
    }

    .stTextInput {
        margin-bottom: 1.2rem !important;
    }

    .stTextInput > label {
        font-size: 0.65rem !important;
        margin-bottom: 0.5rem !important;
    }

    .stTextInput > div > div > input {
        height: 48px !important;
        padding: 12px 14px !important;
        font-size: 0.85rem !important;
        border-radius: 12px !important;
    }

    .stButton > button {
        height: 48px !important;
        font-size: 0.85rem !important;
        margin-top: 1.2rem !important;
        border-radius: 12px !important;
    }

    .insp-brand-title {
        font-size: 1.5rem !important;
        line-height: 1.3 !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
    }

    .insp-brand-desc {
        font-size: 0.85rem !important;
        text-align: center !important;
        margin-bottom: 1.5rem !important;
        line-height: 1.6 !important;
    }

    .insp-features {
        align-items: center !important;
        gap: 1rem !important;
    }

    .insp-feat {
        padding: 0.8rem !important;
        gap: 0.8rem !important;
        flex-direction: row !important;
        align-items: center !important;
        border-radius: 12px !important;
        width: 100% !important;
    }

    .insp-feat > div {
        text-align: left !important;
        flex: 1 !important;
    }

    .insp-feat:hover {
        transform: translateY(-2px) !important;
    }

    .insp-feat-icon {
        width: 40px !important;
        height: 40px !important;
        font-size: 1.2rem !important;
        border-radius: 10px !important;
        margin: 0 !important;
        flex-shrink: 0 !important;
    }

    .insp-feat strong {
        font-size: 0.85rem !important;
        margin-bottom: 0.2rem !important;
        text-align: left !important;
    }

    .insp-feat span {
        font-size: 0.75rem !important;
        text-align: left !important;
    }

    .insp-footer {
        margin-top: 1.5rem !important;
    }

    .insp-badge {
        font-size: 0.65rem !important;
        padding: 8px 14px !important;
        margin-bottom: 12px !important;
    }

    .insp-footer p {
        font-size: 0.7rem !important;
        line-height: 1.5 !important;
    }

    .success-card {
        padding: 40px 25px !important;
        border-radius: 20px !important;
        max-width: 90vw !important;
    }

    .success-icon {
        width: 60px !important;
        height: 60px !important;
        margin: 0 auto 20px !important;
    }

    .checkmark {
        width: 40px !important;
        height: 40px !important;
    }

    .success-title {
        font-size: 1.5rem !important;
        margin-bottom: 10px !important;
    }

    .success-subtitle {
        font-size: 0.85rem !important;
        margin-bottom: 20px !important;
    }

    .success-loading {
        font-size: 0.85rem !important;
    }
}

/* TRÈS PETIT PHONE - 375px */
@media (max-width: 375px) {
    .insp-logo {
        font-size: 0.95rem !important;
        padding: 0.5rem 0.8rem !important;
    }

    .insp-title {
        font-size: 1.4rem !important;
    }

    .insp-subtitle {
        font-size: 0.8rem !important;
    }

    .insp-brand-title {
        font-size: 1.3rem !important;
    }

    .stTextInput > div > div > input {
        font-size: 0.8rem !important;
    }

    .insp-feat {
        padding: 1.2rem !important;
        max-width: 280px !important;
    }

    .insp-feat-icon {
        width: 40px !important;
        height: 40px !important;
        font-size: 1.2rem !important;
        margin: 0 auto 0.4rem auto !important;
        min-width: 40px !important;
    }
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* ♿ ACCESSIBILITY */
/* ════════════════════════════════════════════════════════════════════════════ */

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

*:focus-visible {
    outline: 2px solid var(--primary) !important;
    outline-offset: 3px !important;
    border-radius: 4px !important;
}

::selection {
    background: rgba(124, 58, 237, 0.2) !important;
    color: var(--dark-text) !important;
}
</style>
"""

# ══════════════════════════════════════════════════════════════════════════════
# 🧩 HTML COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════

_HEADER_HTML = """
<div class="insp-panel-left">
    <div class="insp-logo">
        Inspirigence <em>Group</em>
    </div>
    <div class="insp-auth-badge">
        <span class="insp-auth-badge-icon">🔒</span>
        Authentification Sécurisée
        <span class="insp-auth-badge-dot"></span>
    </div>
    <h1 class="insp-title">
        Bienvenue<br>
        <span class="insp-title-gradient">administrateur</span>
    </h1>
    <div class="insp-subtitle">
        Accédez à la plateforme intelligente de transcription et analyse des réunions propulsée par Gemini AI.
    </div>
    <div class="insp-divider"></div>
</div>
"""

_BRAND_HTML = """
<div class="insp-panel-right">
    <div class="insp-brand-title">
        Transformez vos<br><span>réunions</span> en insights.
    </div>
    <div class="insp-brand-desc">
        Plateforme IA de nouvelle génération pour la transcription automatique, l'analyse intelligente et le reporting avancé.
    </div>
    <div class="insp-features">
        <div class="insp-feat">
            <div class="insp-feat-icon">🎙️</div>
            <div>
                <strong>Transcription Automatique</strong>
                <span>Gemini AI — Précision 99.2% — Multi-langue — Temps réel</span>
            </div>
        </div>
        <div class="insp-feat">
            <div class="insp-feat-icon">✨</div>
            <div>
                <strong>Analyse Intelligente</strong>
                <span>Résumés auto, action items, décisions & insights</span>
            </div>
        </div>
        <div class="insp-feat">
            <div class="insp-feat-icon">📊</div>
            <div>
                <strong>Tableaux de Bord Power BI</strong>
                <span>Temps réel, KPIs & reporting personnalisé</span>
            </div>
        </div>
        <div class="insp-feat">
            <div class="insp-feat-icon">🔍</div>
            <div>
                <strong>Recherche Sémantique</strong>
                <span>Retrouvez les moments clés instantanément</span>
            </div>
        </div>
    </div>
</div>
"""

_FOOTER_HTML = """
<div class="insp-footer">
    <div class="insp-badge">🔒 Enterprise SSL/TLS Encryption</div>
    <p>© 2026 Inspirigence · Powered by Gemini AI · SOC 2 Type II</p>
</div>
"""

_SUCCESS_ANIMATION_HTML = """
<div class="success-overlay">
    <div class="success-card">
        <div class="success-icon">
            <svg class="checkmark" viewBox="0 0 52 52">
                <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
            </svg>
        </div>
        <div class="success-title">Connexion réussie! 🎉</div>
        <div class="success-subtitle">Authentification en tant qu'administrateur réussie.</div>
        <div class="success-details">
            <p>✨ Redirection vers le tableau de bord…</p>
        </div>
        <div class="success-loading">
            <div class="loading-ring"></div>
            Chargement…
        </div>
    </div>
</div>
"""

# ══════════════════════════════════════════════════════════════════════════════
# 🔐 AUTHENTICATION FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def check_auth() -> bool:
    """Vérifie si l'utilisateur est connecté"""
    return st.session_state.get(_SESSION_LOGGEDIN, False)

def get_current_user() -> dict | None:
    """Récupère les données de l'utilisateur connecté"""
    if check_auth():
        return st.session_state.get(_SESSION_USER_KEY)
    return None

def logout():
    """Déconnexion de l'utilisateur"""
    for key in [_SESSION_USER_KEY, _SESSION_LOGGEDIN]:
        st.session_state.pop(key, None)
    st.rerun()

def render_user_sidebar():
    """Affiche les informations utilisateur dans la sidebar"""
    user = get_current_user()
    if not user:
        return

    role = user.get("role", "user")
    role_label = "Administration" if role == "admin" else "Utilisateur"
    role_icon = "⚡" if role == "admin" else "👤"
    initiale = user['full_name'][0].upper()

    st.markdown(f"""
<div style="background: linear-gradient(135deg, rgba(124, 58, 237, 0.12), rgba(139, 92, 246, 0.06));
            border: 1.5px solid rgba(124, 58, 237, 0.35);
            border-left: 4px solid #7C3AED;
            border-radius: 16px;
            padding: 20px 18px;
            margin-bottom: 20px;
            font-family: 'Inter', sans-serif;
            backdrop-filter: blur(20px);
            box-shadow: 
                0 4px 12px rgba(0, 0, 0, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);">
    <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 16px;">
        <div style="width: 48px; height: 48px; border-radius: 12px;
                    background: linear-gradient(135deg, #7C3AED, #8B5CF6);
                    display: flex; align-items: center; justify-content: center;
                    font-size: 1rem; font-weight: 800; color: #fff; flex-shrink: 0;
                    box-shadow: 
                        0 4px 12px rgba(124, 58, 237, 0.35),
                        inset 0 1px 0 rgba(255, 255, 255, 0.2);">
            {initiale}
        </div>
        <div style="flex: 1; min-width: 0;">
            <div style="color: #ffffff; font-weight: 700; font-size: 0.95rem; 
                       white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                {user['full_name']}
            </div>
            <div style="color: #9ca3af; font-size: 0.8rem; margin-top: 4px; 
                       white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                {user['email']}
            </div>
        </div>
    </div>
    <span style="display: inline-flex; align-items: center; gap: 8px;
                 font-size: 0.7rem; letter-spacing: 0.08em;
                 text-transform: uppercase; color: #7C3AED; font-weight: 700;
                 background: rgba(124, 58, 237, 0.15);
                 padding: 6px 14px; border-radius: 100px;
                 border: 1px solid rgba(124, 58, 237, 0.35);
                 box-shadow: 0 2px 8px rgba(124, 58, 237, 0.1);">
        {role_icon} {role_label}
    </span>
</div>
""", unsafe_allow_html=True)

    if st.button("🚪 Se déconnecter", use_container_width=True, key="_btn_logout_sidebar"):
        logout()

def login_page():
    """Page de connexion ultra premium"""
    auth.ensure_users_table()
    
    # 🎨 Inject CSS
    st.markdown(_LOGIN_CSS, unsafe_allow_html=True)

    # 📐 Split layout - FULLY RESPONSIVE
    col_left, col_right = st.columns([0.45, 0.55])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 📝 LEFT PANEL - LOGIN FORM
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with col_left:
        st.markdown(_HEADER_HTML, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(
                "📧 Adresse email",
                placeholder="prenom.nom@inspirigence.ma",
                key="login_email_field"
            )
            password = st.text_input(
                "🔑 Mot de passe",
                type="password",
                placeholder="••••••••••••",
                key="login_password_field"
            )
            submitted = st.form_submit_button("🔐 SE CONNECTER", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("⚠️ Veuillez renseigner vos identifiants.", icon="🔑")
            else:
                with st.spinner("🔐 Authentification en cours…"):
                    result = auth.login_user(email=email, password=password)

                if result["ok"]:
                    if result["user"]["role"] != "admin":
                        st.error("❌ Accès refusé — administrateurs uniquement.", icon="🚫")
                    else:
                        # ✅ Set session state
                        st.session_state[_SESSION_LOGGEDIN] = True
                        st.session_state[_SESSION_USER_KEY] = result["user"]
                        
                        # 🎬 Show success animation
                        st.markdown(_SUCCESS_ANIMATION_HTML, unsafe_allow_html=True)
                        st.balloons()
                        
                        # ⏳ Wait for animation
                        time.sleep(2.5)
                        
                        # 🔄 Redirect
                        st.rerun()
                else:
                    st.error(f"❌ {result['message']}", icon="⚠️")

        st.markdown(_FOOTER_HTML, unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 🎨 RIGHT PANEL - BRANDING
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with col_right:
        st.markdown(_BRAND_HTML, unsafe_allow_html=True)

def require_auth() -> dict:
    """Protège une page - Redirige vers login si non authentifié"""
    if not check_auth():
        login_page()
        st.stop()
    return get_current_user()