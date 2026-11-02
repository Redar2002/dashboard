"""
app.py — Point d'entrée de Meeting Intelligence.
Configure la page, applique le thème, vérifie la connexion puis affiche la page choisie.
Lancement : streamlit run app.py
"""
import streamlit as st

st.set_page_config(
    page_title="Meeting Intelligence",
    page_icon=":material/graphic_eq:",
    layout="wide",
    initial_sidebar_state="expanded",
)

import ui
import utils_auth
import utils_sql
from services.modele import get_model, model_label

ui.apply_theme()
utils_auth.require_auth()

st.logo(ui.LOGO_PATH, size="large")

page = st.navigation({
    "Espace de travail": [
        st.Page("views/accueil.py", title="Réunions", icon=":material/graphic_eq:", default=True),
        st.Page("views/recherche.py", title="Recherche", icon=":material/search:"),
        st.Page("views/guide.py", title="Guide explicatif", icon=":material/menu_book:"),
    ],
    "Reporting": [
        st.Page("views/power_bi.py", title="Power BI", icon=":material/bar_chart:"),
    ],
})

# ── Barre latérale commune ────────────────────────────────────────────────
with st.sidebar:
    model, model_error = get_model()
    if model:
        ui.status_line(f"Gemini · {model_label(model)}")
    else:
        st.error(f"Gemini non configuré : {model_error}", icon=":material/error:")

    with st.expander("Diagnostic", icon=":material/build:"):
        if st.button("Tester l'API Gemini", width="stretch", disabled=model is None):
            with st.spinner("Test en cours…"):
                try:
                    model.generate_content(
                        "Réponds uniquement par: OK",
                        generation_config={"max_output_tokens": 5},
                    )
                    st.success("API opérationnelle.", icon=":material/check_circle:")
                except Exception as e:
                    err = str(e)
                    if "429" in err or "ResourceExhausted" in err:
                        st.error("Quota épuisé (429). Réessayez plus tard ou activez la facturation.")
                    elif "404" in err or "NotFound" in err:
                        st.error("Modèle introuvable (404).")
                    else:
                        st.error(f"Erreur : {err[:160]}")

        if st.button("Tester SQL Server", width="stretch"):
            with st.spinner("Connexion…"):
                result = utils_sql.check_connection()
            if result["ok"]:
                st.success(f"Connecté à **{result['database']}** ({result['driver']}).", icon=":material/check_circle:")
            else:
                st.error(f"Connexion échouée : {result['message']}")

    st.divider()
    utils_auth.render_user_sidebar()

page.run()
