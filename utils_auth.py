"""
utils_auth.py — INSPIRIGENCE ULTRA PREMIUM PRO MAX
Zone gauche redessinée avec texture, glassmorphism et effets premium
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
# 🎨 CSS ULTRA PREMIUM - ZONE GAUCHE REDESSINÉE
# ══════════════════════════════════════════════════════════════════════════════

_LOGIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700;800&display=swap');

*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
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
    --border-radius-sm: 10px;
    --border-radius-md: 16px;
    --border-radius-lg: 24px;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    --transition-fast: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-base: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    --spring: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

html, body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-weight: 400;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
    overflow-x: hidden;
}

#MainMenu, footer, header {
    visibility: hidden !important;
}

[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🌌 BACKGROUND AVEC GRADIENT MESH */
/* ════════════════════════════════════════════════════════════════════════════ */

.stApp {
    min-height: 100vh !important;
    background: #0A0118 !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow-x: hidden !important;
    position: relative;
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
    margin: 0 !important;
    position: relative;
    z-index: 2;
    min-height: 100vh;
    display: flex !important;
    justify-content: center;
    align-items: center;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🎬 ANIMATIONS FLUIDES */
/* ════════════════════════════════════════════════════════════════════════════ */

@keyframes slideInLeft {
    0% {
        opacity: 0;
        transform: translateX(-60px) scale(0.95);
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
        transform: translateX(60px) scale(0.95);
        filter: blur(10px);
    }
    100% {
        opacity: 1;
        transform: translateX(0) scale(1);
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

@keyframes scaleIn {
    0% {
        opacity: 0;
        transform: scale(0.9);
    }
    100% {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
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

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
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

@keyframes lds-ring {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes iconPop {
    0% { transform: scale(0.8); opacity: 0; }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); opacity: 1; }
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 📐 LAYOUT SPLIT-SCREEN */
/* ════════════════════════════════════════════════════════════════════════════ */

[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
    align-items: stretch !important;
    min-height: 100vh !important;
    max-height: 100vh !important;
    position: relative !important;
    z-index: 10 !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🎨 PARTIE GAUCHE - REDESIGN PREMIUM */
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
    position: relative;
    overflow: hidden;
    box-shadow: 
        4px 0 60px rgba(0, 0, 0, 0.08),
        inset -1px 0 0 rgba(124, 58, 237, 0.1);
}

/* Texture subtile sur fond gauche */
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

/* Gradient border top */
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
    position: relative;
    z-index: 1;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🏷️ LOGO PREMIUM */
/* ════════════════════════════════════════════════════════════════════════════ */

.insp-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--dark-text);
    letter-spacing: -0.03em;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 12px;
    animation: fadeInUp 0.6s ease-out;
    position: relative;
    padding: 1rem 1.5rem;
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.9), 
        rgba(248, 250, 252, 0.7)
    );
    border-radius: var(--border-radius-md);
    border: 1px solid rgba(124, 58, 237, 0.15);
    box-shadow: 
        0 4px 12px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}

.insp-logo::before {
    content: '';
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    box-shadow: 
        0 0 20px rgba(124, 58, 237, 0.6),
        0 2px 8px rgba(124, 58, 237, 0.3);
    animation: pulse 2s ease-in-out infinite;
}

.insp-logo em {
    font-style: italic;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s linear infinite;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🔒 BADGE "AUTHENTIFICATION SÉCURISÉE" REDESIGNÉ */
/* ════════════════════════════════════════════════════════════════════════════ */

.insp-auth-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--primary);
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 0.12), 
        rgba(139, 92, 246, 0.08)
    );
    border: 1.5px solid rgba(124, 58, 237, 0.25);
    border-radius: 100px;
    padding: 10px 18px;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 
        0 4px 12px rgba(124, 58, 237, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
    transition: var(--transition-base);
    animation: fadeInUp 0.6s ease-out 0.1s both;
    position: relative;
    overflow: hidden;
}

.insp-auth-badge::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.2), 
        transparent
    );
    opacity: 0;
    transition: opacity 0.3s;
}

.insp-auth-badge:hover {
    border-color: rgba(124, 58, 237, 0.5);
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 0.18), 
        rgba(139, 92, 246, 0.12)
    );
    box-shadow: 
        0 6px 16px rgba(124, 58, 237, 0.2),
        0 0 30px rgba(124, 58, 237, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.4);
    transform: scale(1.05) translateY(-2px);
}

.insp-auth-badge:hover::before {
    opacity: 1;
}

.insp-auth-badge-icon {
    font-size: 0.9rem;
    animation: iconPop 0.6s var(--spring) 0.2s both;
}

.insp-auth-badge-dot {
    width: 6px;
    height: 6px;
    background: var(--success);
    border-radius: 50%;
    box-shadow: 
        0 0 10px rgba(16, 185, 129, 0.6),
        0 0 20px rgba(16, 185, 129, 0.3);
    animation: pulse 2s ease-in-out infinite;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 📝 TYPOGRAPHY */
/* ════════════════════════════════════════════════════════════════════════════ */

.insp-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--dark-text);
    letter-spacing: -0.04em;
    line-height: 1.15;
    margin-bottom: 1rem;
    animation: fadeInUp 0.6s ease-out 0.2s both;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.insp-title-gradient {
    background: linear-gradient(135deg, 
        var(--primary) 0%, 
        var(--secondary) 50%, 
        var(--accent) 100%
    );
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 5s linear infinite;
    position: relative;
}

.insp-subtitle {
    font-size: 0.95rem;
    color: var(--gray-600);
    line-height: 1.7;
    margin-bottom: 2rem;
    font-weight: 400;
    animation: fadeInUp 0.6s ease-out 0.3s both;
}

.insp-divider {
    height: 1px;
    background: linear-gradient(90deg, 
        transparent, 
        var(--gray-300) 20%, 
        var(--gray-300) 80%, 
        transparent
    );
    margin: 2rem 0;
    animation: fadeInUp 0.6s ease-out 0.4s both;
    position: relative;
}

.insp-divider::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 8px;
    height: 8px;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border-radius: 50%;
    box-shadow: 
        0 0 12px rgba(124, 58, 237, 0.5),
        0 0 24px rgba(124, 58, 237, 0.3);
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 📧 FORM INPUTS - GLASSMORPHISM */
/* ════════════════════════════════════════════════════════════════════════════ */

.stTextInput {
    animation: fadeInUp 0.6s ease-out 0.5s both;
    margin-bottom: 1.5rem;
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
/* 🔘 BUTTON ULTRA PREMIUM */
/* ════════════════════════════════════════════════════════════════════════════ */

.stButton {
    animation: fadeInUp 0.6s ease-out 0.6s both;
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
    background-size: 200% 200%;
    box-shadow: 
        0 8px 24px rgba(124, 58, 237, 0.35),
        0 0 0 0 rgba(124, 58, 237, 0) !important;
    transition: var(--transition-base) !important;
    margin-top: 1.5rem !important;
    cursor: pointer !important;
    position: relative;
    overflow: hidden;
    text-transform: uppercase;
}

.stButton > button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.25), 
        transparent
    );
    opacity: 0;
    transition: opacity 0.3s;
    z-index: 1;
}

.stButton > button::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
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
    opacity: 1;
}

.stButton > button:hover::after {
    width: 300px;
    height: 300px;
    opacity: 0;
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
    animation: slideInUp 0.5s var(--spring);
    box-shadow: var(--shadow-md) !important;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🏷️ FOOTER */
/* ════════════════════════════════════════════════════════════════════════════ */

.insp-footer {
    margin-top: 2.5rem;
    text-align: center;
    animation: fadeInUp 0.6s ease-out 0.7s both;
}

.insp-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-size: 0.7rem;
    color: var(--primary);
    font-weight: 700;
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 0.1), 
        rgba(139, 92, 246, 0.05)
    );
    border: 1.5px solid rgba(124, 58, 237, 0.3);
    border-radius: 100px;
    padding: 10px 20px;
    margin-bottom: 16px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    backdrop-filter: blur(10px);
    transition: var(--transition-base);
    box-shadow: 0 2px 8px rgba(124, 58, 237, 0.1);
}

.insp-badge::before {
    content: '';
    width: 6px;
    height: 6px;
    background: var(--success);
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
    animation: pulse 2s ease-in-out infinite;
}

.insp-badge:hover {
    border-color: rgba(124, 58, 237, 0.6);
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 0.15), 
        rgba(139, 92, 246, 0.08)
    );
    box-shadow: 
        0 4px 12px rgba(124, 58, 237, 0.2),
        0 0 20px rgba(124, 58, 237, 0.15);
    transform: scale(1.05) translateY(-2px);
}

.insp-footer p {
    font-size: 0.8rem;
    color: var(--gray-600);
    line-height: 1.6;
    font-weight: 400;
    margin: 0;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🎨 PARTIE DROITE - BRANDING */
/* ════════════════════════════════════════════════════════════════════════════ */

[data-testid="stColumn"]:nth-child(2) {
    padding: 0 !important;
    background: transparent !important;
    position: relative !important;
    animation: slideInRight 0.9s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    overflow: hidden !important;
}

[data-testid="stColumn"]:nth-child(2) > [data-testid="stVerticalBlock"] {
    padding: 3.5rem 3rem !important;
    max-width: 680px !important;
    width: 100% !important;
}

.insp-panel-right {
    position: relative;
    z-index: 10;
}

.insp-brand-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: var(--light-text);
    line-height: 1.15;
    letter-spacing: -0.04em;
    margin-bottom: 1.8rem;
    text-shadow: 
        0 4px 20px rgba(0, 0, 0, 0.4),
        0 0 40px rgba(124, 58, 237, 0.3);
    animation: fadeInUp 0.6s ease-out 0.2s both;
}

.insp-brand-title span {
    background: linear-gradient(135deg, 
        #EC4899 0%, 
        #D946EF 50%, 
        #A78BFA 100%
    );
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 5s linear infinite;
}

.insp-brand-desc {
    font-size: 1rem;
    color: rgba(248, 250, 252, 0.85);
    font-weight: 400;
    line-height: 1.8;
    margin-bottom: 3rem;
    animation: fadeInUp 0.6s ease-out 0.3s both;
}

.insp-features {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
}

.insp-feat {
    display: flex;
    align-items: flex-start;
    gap: 1.2rem;
    padding: 1.5rem;
    border-radius: 18px;
    background: linear-gradient(135deg, 
        rgba(30, 27, 60, 0.7), 
        rgba(26, 15, 46, 0.5)
    );
    border: 1px solid rgba(139, 92, 246, 0.25);
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    transition: var(--transition-base);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.insp-feat:nth-child(1) { animation: fadeInUp 0.6s ease-out 0.4s both; }
.insp-feat:nth-child(2) { animation: fadeInUp 0.6s ease-out 0.5s both; }
.insp-feat:nth-child(3) { animation: fadeInUp 0.6s ease-out 0.6s both; }
.insp-feat:nth-child(4) { animation: fadeInUp 0.6s ease-out 0.7s both; }

.insp-feat::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 0.15), 
        rgba(217, 70, 239, 0.05)
    );
    opacity: 0;
    transition: opacity 0.4s;
}

.insp-feat:hover {
    background: linear-gradient(135deg, 
        rgba(30, 27, 60, 0.9), 
        rgba(26, 15, 46, 0.7)
    );
    border-color: rgba(124, 58, 237, 0.5);
    transform: translateX(16px) translateY(-6px) scale(1.02);
    box-shadow: 
        0 12px 32px rgba(0, 0, 0, 0.4),
        0 0 40px rgba(124, 58, 237, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.insp-feat:hover::before {
    opacity: 1;
}

.insp-feat-icon {
    width: 50px;
    height: 50px;
    border-radius: 14px;
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 0.3), 
        rgba(139, 92, 246, 0.2)
    );
    border: 1px solid rgba(139, 92, 246, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
    backdrop-filter: blur(10px);
    transition: var(--transition-base);
    box-shadow: 
        0 4px 12px rgba(124, 58, 237, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    animation: iconPop 0.6s var(--spring);
}

.insp-feat:hover .insp-feat-icon {
    transform: scale(1.15) rotate(10deg);
    background: linear-gradient(135deg, 
        rgba(124, 58, 237, 0.5), 
        rgba(139, 92, 246, 0.3)
    );
    box-shadow: 
        0 8px 24px rgba(124, 58, 237, 0.4),
        0 0 40px rgba(124, 58, 237, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.insp-feat strong {
    display: block;
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--light-text);
    margin-bottom: 0.4rem;
    letter-spacing: 0.01em;
}

.insp-feat span {
    font-size: 0.85rem;
    color: rgba(248, 250, 252, 0.7);
    font-weight: 400;
    line-height: 1.6;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 🎉 SUCCESS OVERLAY */
/* ════════════════════════════════════════════════════════════════════════════ */

.success-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    animation: fadeIn 0.3s ease-out;
}

.success-card {
    background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
    border: 2px solid #22c55e;
    border-radius: 24px;
    padding: 60px 45px;
    text-align: center;
    max-width: 480px;
    box-shadow: 
        0 25px 60px rgba(0, 0, 0, 0.3),
        0 0 60px rgba(34, 197, 94, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.5);
    animation: successPulse 0.6s var(--spring);
}

.success-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 30px;
    background: linear-gradient(135deg, #22c55e, #16a34a);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: float 2s ease-in-out infinite;
    box-shadow: 
        0 10px 30px rgba(34, 197, 94, 0.4),
        inset 0 2px 0 rgba(255, 255, 255, 0.3);
}

.checkmark {
    width: 50px;
    height: 50px;
    stroke: white;
    stroke-width: 3;
    stroke-linecap: round;
    stroke-linejoin: round;
    fill: none;
    animation: checkmarkDraw 0.8s cubic-bezier(0.4, 0, 0.2, 1) 0.2s both;
    stroke-dasharray: 100;
}

.success-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--dark-text);
    margin-bottom: 12px;
    animation: fadeInUp 0.6s ease-out 0.4s both;
}

.success-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    color: var(--gray-600);
    line-height: 1.6;
    margin-bottom: 28px;
    animation: fadeInUp 0.6s ease-out 0.5s both;
}

.success-details {
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 28px;
    animation: fadeInUp 0.6s ease-out 0.6s both;
    box-shadow: 0 2px 8px rgba(34, 197, 94, 0.1);
}

.success-details p {
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    color: var(--dark-text);
    margin: 0;
    font-weight: 500;
}

.loading-ring {
    display: inline-block;
    position: relative;
    width: 30px;
    height: 30px;
    margin-right: 10px;
}

.loading-ring::after {
    content: "";
    display: block;
    width: 24px;
    height: 24px;
    margin: 3px;
    border-radius: 50%;
    border: 3px solid #22c55e;
    border-color: #22c55e transparent transparent transparent;
    animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
}

.success-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    font-family: 'Inter', sans-serif;
    color: #22c55e;
    font-weight: 600;
    font-size: 0.95rem;
}

/* ════════════════════════════════════════════════════════════════════════════ */
/* 📱 RESPONSIVE */
/* ════════════════════════════════════════════════════════════════════════════ */

@media (max-width: 1400px) {
    .insp-brand-title {
        font-size: 2.6rem;
    }
}

@media (max-width: 1200px) {
    .insp-brand-title {
        font-size: 2.3rem;
    }
    
    .insp-title {
        font-size: 2.2rem;
    }
}

@media (max-width: 1024px) {
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }

    [data-testid="stColumn"]:nth-child(2) {
        display: none !important;
    }

    .insp-title {
        font-size: 2rem;
    }
}

@media (max-width: 768px) {
    [data-testid="stColumn"]:nth-child(1) > [data-testid="stVerticalBlock"] {
        padding: 2.5rem 2rem !important;
    }

    .insp-logo {
        font-size: 1.4rem;
    }

    .insp-title {
        font-size: 1.9rem;
    }

    .stTextInput > div > div > input {
        height: 52px !important;
    }

    .stButton > button {
        height: 52px !important;
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
    outline: 2px solid var(--primary);
    outline-offset: 3px;
    border-radius: 4px;
}

::selection {
    background: rgba(124, 58, 237, 0.2);
    color: var(--dark-text);
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
        Accédez à la plateforme intelligente de transcription<br>
        et analyse des réunions propulsée par Gemini AI.
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
        Plateforme IA de nouvelle génération pour la transcription automatique,<br>
        l'analyse intelligente et le reporting avancé de vos réunions d'entreprise.
    </div>
    <div class="insp-features">
        <div class="insp-feat">
            <div class="insp-feat-icon">🎙️</div>
            <div>
                <strong>Transcription Automatique</strong>
                <span>Gemini AI — Précision 99.2% — Support multi-langue — Temps réel</span>
            </div>
        </div>
        <div class="insp-feat">
            <div class="insp-feat-icon">✨</div>
            <div>
                <strong>Analyse Intelligente</strong>
                <span>Résumés automatiques, action items, décisions clés et insights</span>
            </div>
        </div>
        <div class="insp-feat">
            <div class="insp-feat-icon">📊</div>
            <div>
                <strong>Tableaux de Bord Power BI</strong>
                <span>Visualisation temps réel, KPIs et reporting personnalisé</span>
            </div>
        </div>
        <div class="insp-feat">
            <div class="insp-feat-icon">🔍</div>
            <div>
                <strong>Recherche Sémantique Avancée</strong>
                <span>Retrouvez instantanément chaque moment clé de vos réunions</span>
            </div>
        </div>
    </div>
</div>
"""

_FOOTER_HTML = """
<div class="insp-footer">
    <div class="insp-badge">🔒 Enterprise SSL/TLS Encryption</div>
    <p>© 2026 Inspirigence Groupe · Powered by Gemini AI · SOC 2 Type II Certified</p>
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
        <div class="success-subtitle">Vous êtes maintenant authentifié en tant qu'administrateur.</div>
        <div class="success-details">
            <p>✨ Redirection en cours vers le tableau de bord…</p>
        </div>
        <div class="success-loading">
            <div class="loading-ring"></div>
            Chargement de votre espace…
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

    # 📐 Split layout
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