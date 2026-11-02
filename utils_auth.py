"""
utils_auth.py — Session et page de connexion de Meeting Intelligence
"""
import os
import sys

import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import auth
import ui

_SESSION_USER_KEY = "_auth_user"
_SESSION_LOGGEDIN = "_auth_logged_in"

_LOGIN_CSS = """
<style>
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display: none; }
.block-container { max-width: 440px; }
</style>
"""


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
    """Carte utilisateur + déconnexion, en bas de la barre latérale."""
    user = get_current_user()
    if not user:
        return
    ui.user_card(user)
    if st.button("Se déconnecter", icon=":material/logout:", width="stretch", key="_btn_logout_sidebar"):
        logout()


def login_page():
    """Page de connexion."""
    auth.ensure_users_table()
    st.markdown(_LOGIN_CSS, unsafe_allow_html=True)

    st.markdown('<div class="mi-login-head"></div>', unsafe_allow_html=True)
    _, logo_col, _ = st.columns([1, 2, 1])
    with logo_col:
        st.image(ui.LOGO_PATH, width="stretch")
    st.markdown(
        '<div style="text-align:center;margin-bottom:1.5rem;">'
        '<div class="mi-login-title">Connexion</div>'
        '<div class="mi-login-subtitle">Accédez à votre espace Meeting Intelligence.</div></div>',
        unsafe_allow_html=True,
    )

    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Adresse email", placeholder="prenom.nom@inspirigence.ma", key="login_email_field")
        password = st.text_input("Mot de passe", type="password", key="login_password_field")
        submitted = st.form_submit_button("Se connecter", type="primary", width="stretch")

    if submitted:
        if not email or not password:
            st.error("Veuillez renseigner votre email et votre mot de passe.", icon=":material/error:")
        else:
            with st.spinner("Vérification…"):
                result = auth.login_user(email=email, password=password)

            if not result["ok"]:
                st.error(result["message"], icon=":material/error:")
            elif result["user"]["role"] != "admin":
                st.error("Accès réservé aux administrateurs.", icon=":material/block:")
            else:
                st.session_state[_SESSION_LOGGEDIN] = True
                st.session_state[_SESSION_USER_KEY] = result["user"]
                st.rerun()

    st.markdown('<div class="mi-login-foot">© Inspirigence Group · Meeting Intelligence</div>', unsafe_allow_html=True)


def require_auth() -> dict:
    """Affiche la page de connexion et arrête l'exécution si l'utilisateur n'est pas connecté."""
    if not check_auth():
        login_page()
        st.stop()
    return get_current_user()
