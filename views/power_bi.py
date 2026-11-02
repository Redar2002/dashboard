import streamlit as st

import ui

REPORT_URL = (
    "https://app.powerbi.com/reportEmbed?reportId=b5d118c4-3dcc-4b39-8a97-9147e1807410"
    "&autoAuth=true&ctid=993f3397-d964-4599-8045-90049af66354&actionBarEnabled=true"
)

ui.page_header(
    "Power BI",
    "Tableau de bord commercial alimenté par les données SQL Server.",
    eyebrow="Reporting",
    index="(04)",
)

st.markdown(
    f'<div class="mi-embed"><iframe title="Rapport Power BI" src="{REPORT_URL}" allowfullscreen="true"></iframe></div>',
    unsafe_allow_html=True,
)

st.caption(
    "Utilisez les filtres directement dans le rapport. Si le rapport ne s'affiche pas, "
    "vérifiez que votre compte Microsoft a accès au tenant 993f3397-d964-4599-8045-90049af66354."
)
st.link_button("Ouvrir dans Power BI", REPORT_URL, icon=":material/open_in_new:")

ui.footer()
