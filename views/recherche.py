import streamlit as st
from google.api_core.exceptions import ResourceExhausted

import ui
import utils_data
from services.analyse import semantic_search
from services.modele import get_model

MODEL, _model_error = get_model()

ui.page_header(
    "Recherche",
    "Posez une question en langage naturel : l'IA retrouve les passages pertinents dans vos réunions.",
    eyebrow="Meeting Intelligence",
)

meetings = utils_data.load_meetings()

if not meetings:
    ui.empty_state("Aucune réunion disponible", "Enregistrez d'abord une réunion depuis la page Réunions.")
    st.stop()

with st.container(border=True, key="card_recherche_1"):
    labels = [
        f"{i} — {m.get('title', m.get('filename', 'Sans titre'))}"
        for i, m in enumerate(meetings)
    ]
    selected = st.multiselect(
        "Réunions",
        labels,
        placeholder="Choisir les réunions où chercher…",
    )
    search_query = st.text_input(
        "Question",
        placeholder="Ex. : Quel budget a été évoqué ? Quelles objections le client a-t-il soulevées ?",
        key="search_input",
    )
    search_button = st.button("Rechercher", icon=":material/search:", type="primary", disabled=MODEL is None)

if search_button:
    if not search_query:
        st.warning("Saisissez une question.")
    elif not selected:
        st.warning("Sélectionnez au moins une réunion.")
    else:
        selected_indices = [int(i.split(" — ")[0]) for i in selected]
        with st.spinner("Recherche dans les réunions…"):
            try:
                st.session_state.search_results = semantic_search(search_query, selected_indices, MODEL)
            except ResourceExhausted:
                st.error("Quota API épuisé. Patientez une minute puis réessayez.")
            except Exception as e:
                st.error(f"Erreur : {e}")

search_results = st.session_state.get("search_results")
if search_results:
    with st.container(border=True, key="card_recherche_2"):
        ui.section_header("Réponse")
        st.write(search_results.get("summary", "Aucun résumé disponible."))

    results = search_results.get("results", [])
    if results:
        ui.section_header("Passages trouvés", count=len(results))
        for result in results:
            ui.search_result(
                result.get("meeting_title", "Sans titre"),
                result.get("timestamp", "--:--"),
                result.get("text", ""),
                result.get("relevance", 0),
            )
    else:
        ui.empty_state(
            "Aucun passage pertinent",
            "Reformulez la question ou sélectionnez d'autres réunions.",
        )
