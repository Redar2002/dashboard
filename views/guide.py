import streamlit as st
from google.api_core.exceptions import ResourceExhausted

import ui
import utils_data
from services.analyse import generate_topic_explanation
from services.modele import get_model
from utils_topic_pdf import create_topic_pdf

MODEL, _model_error = get_model()

ui.page_header(
    "Guide explicatif",
    "Générez un guide détaillé sur un produit, un service ou un concept abordé dans vos réunions.",
    eyebrow="Meeting Intelligence",
)

meetings = utils_data.load_meetings()

if not meetings:
    ui.empty_state("Aucune réunion disponible", "Enregistrez d'abord une réunion depuis la page Réunions.")
    st.stop()

with st.container(border=True, key="card_guide_1"):
    labels = [
        f"{i} — {m.get('title', m.get('filename', 'Sans titre'))}"
        for i, m in enumerate(meetings)
    ]
    selected = st.multiselect(
        "Réunions sources",
        labels,
        placeholder="Choisir les réunions qui parlent du sujet…",
    )
    topic_input = st.text_input(
        "Sujet",
        placeholder="Ex. : Kommo CRM, agent IA, gestion des leads…",
        key="topic_input",
    )
    generate_button = st.button("Générer le guide", icon=":material/auto_stories:", type="primary", disabled=MODEL is None)

if generate_button:
    if not topic_input:
        st.warning("Saisissez un sujet.")
    elif not selected:
        st.warning("Sélectionnez au moins une réunion.")
    else:
        selected_indices = [int(i.split(" — ")[0]) for i in selected]
        with st.spinner(f"Rédaction du guide « {topic_input} »…"):
            try:
                st.session_state.topic_explanation = generate_topic_explanation(topic_input, selected_indices, MODEL)
                st.session_state.topic_name = topic_input
            except ResourceExhausted:
                st.error("Quota API épuisé. Patientez une minute puis réessayez.")
            except Exception as e:
                st.error(f"Erreur : {e}")

if st.session_state.get("topic_explanation"):
    with st.container(border=True, key="card_guide_2"):
        st.markdown(st.session_state.topic_explanation)

    file_base = f"guide_{st.session_state.topic_name.replace(' ', '_')}"
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="Télécharger (PDF)",
            icon=":material/picture_as_pdf:",
            data=create_topic_pdf(st.session_state.topic_explanation, st.session_state.topic_name),
            file_name=f"{file_base}.pdf",
            mime="application/pdf",
            key="download_topic_pdf",
            width="stretch",
        )
    with col_dl2:
        st.download_button(
            label="Télécharger (Markdown)",
            icon=":material/download:",
            data=st.session_state.topic_explanation,
            file_name=f"{file_base}.md",
            mime="text/markdown",
            key="download_topic_md",
            width="stretch",
        )
