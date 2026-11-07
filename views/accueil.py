from datetime import datetime

import streamlit as st
from google.api_core.exceptions import ResourceExhausted

import ui
import utils_ai_structurer
import utils_audio
import utils_data
import utils_pdf
import utils_sql
import utils_transcription
from services.analyse import (
    extract_objections,
    generate_followup_email,
    generate_global_report,
    generate_improvement_report,
    generate_pro_minutes,
)
from services.modele import get_model

MODEL, _model_error = get_model()
load_meetings = utils_data.load_meetings
save_meetings = utils_data.save_meetings


def _meeting_date(meeting):
    try:
        return datetime.strptime(meeting.get("meeting_id", ""), "%Y%m%d_%H%M%S")
    except ValueError:
        return None


meetings = load_meetings()

# ═══════════════════════════════════════════════════════════════════════════
# EN-TÊTE + INDICATEURS
# ═══════════════════════════════════════════════════════════════════════════

ui.banner(
    "Meeting Intelligence",
    "Transcrivez vos réunions commerciales, puis laissez l'IA générer rapports, comptes rendus et analyses.",
    badges=["Gemini AI", "Transcription automatique", "Analyse MEDDIC", "Power BI"],
)

dates = [d for d in (_meeting_date(m) for m in meetings) if d]
word_counts = [len(m.get("transcript", "").split()) for m in meetings]
words = sum(word_counts)
# Estimation à ~130 mots par minute de parole
minutes = round(words / 130)

k1, k2, k3, k4 = st.columns(4)
with k1:
    ui.kpi("Réunions", len(meetings), icon="mic", tone="violet")
with k2:
    ui.kpi("Mots transcrits", f"{words:,}".replace(",", " "), icon="text", tone="blue")
with k3:
    ui.kpi(
        "Temps de parole (estimé)",
        f"{minutes // 60} h {minutes % 60:02d}" if minutes >= 60 else f"{minutes} min",
        icon="clock",
        tone="green",
    )
with k4:
    ui.kpi("Dernière réunion", max(dates).strftime("%d/%m/%Y") if dates else "—", icon="calendar", tone="amber")

if meetings:
    st.write("")
    c_chart, c_list = st.columns([3, 2])
    with c_chart:
        with st.container(border=True):
            ui.section_header("Volume par réunion", "Nombre de mots transcrits")
            recent = meetings[:8]
            st.bar_chart(
                {
                    "Réunion": [m.get("title", "Sans titre").split(" — ")[0][:24] for m in recent],
                    "Mots": [len(m.get("transcript", "").split()) for m in recent],
                },
                x="Réunion",
                y="Mots",
                x_label="",
                y_label="",
                sort="-Mots",
                color="#6D28D9",
                horizontal=True,
                height=260,
            )
    with c_list:
        with st.container(border=True):
            ui.section_header("Réunions récentes", count=len(meetings))
            ui.meeting_list([
                (
                    m.get("title", "Sans titre"),
                    _meeting_date(m).strftime("%d/%m/%Y à %H:%M") if _meeting_date(m) else "Date inconnue",
                    f"{len(m.get('transcript', '').split()):,} mots".replace(",", " "),
                )
                for m in meetings[:5]
            ])

st.write("")

if MODEL is None:
    st.error(f"Modèle Gemini non configuré : {_model_error}", icon=":material/error:")

tab_new, tab_analyse, tab_audit = st.tabs(["Nouvelle réunion", "Analyse", "Audit global"])

# ═══════════════════════════════════════════════════════════════════════════
# NOUVELLE RÉUNION
# ═══════════════════════════════════════════════════════════════════════════

with tab_new:
    with st.container(border=True):
        ui.section_header(
            "Importer un enregistrement",
            "Audio ou vidéo : la transcription et le nettoyage sont faits automatiquement.",
        )
        uploaded_file = st.file_uploader(
            "Fichier (MP3, WAV, M4A, AAC, MP4, MOV, AVI)",
            type=['mp3', 'wav', 'm4a', 'aac', 'mp4', 'mov', 'avi']
        )

        col1, col2 = st.columns([3, 1])
        with col1:
            meeting_title = st.text_input("Titre de la réunion (facultatif)", placeholder="Ex. : Démo CRM — Client X")
        with col2:
            lang_choice = st.selectbox("Langue", ["Français", "Anglais", "Mixte"])

        start = st.button("Lancer la transcription", icon=":material/graphic_eq:", type="primary", width="stretch")

    if start:
        if not uploaded_file:
            st.error("Sélectionnez un fichier avant de lancer la transcription.")
        elif not MODEL:
            st.error("Modèle Gemini non configuré.")
        else:
            with st.spinner(f"Traitement de {uploaded_file.name}… (cela peut prendre plusieurs minutes)"):
                try:
                    import os
                    import tempfile

                    # Fichier temporaire système, supprimé même en cas d'erreur
                    suffix = os.path.splitext(uploaded_file.name)[1] or ".mp3"
                    with tempfile.NamedTemporaryFile(prefix="upload_", suffix=suffix, delete=False) as f:
                        f.write(uploaded_file.getbuffer())
                        tmp_filepath = f.name

                    try:
                        transcription_text, transcription_clean = utils_transcription.transcribe_and_clean_audio(
                            filepath=tmp_filepath,
                            model=MODEL,
                            lang_choice=lang_choice
                        )
                    finally:
                        if os.path.exists(tmp_filepath):
                            os.remove(tmp_filepath)

                    segments, pure_text = utils_transcription.parse_transcript_to_segments(transcription_text)
                    segments_clean, pure_text_clean = utils_transcription.parse_transcript_to_segments(transcription_clean)

                    st.session_state["pending_meeting"] = {
                        "title": meeting_title if meeting_title else uploaded_file.name,
                        "meeting_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
                        "filename": uploaded_file.name,
                        "segments": segments,
                        "transcript": pure_text,
                        "transcript_clean": pure_text_clean,
                        "segments_clean": segments_clean
                    }
                    st.session_state["transcription_finished"] = True

                except Exception as e:
                    st.error(f"Erreur lors de la transcription : {e}")

    # Zone de confirmation
    if "pending_meeting" in st.session_state:
        st.info(f"Transcription prête : **{st.session_state['pending_meeting']['title']}**", icon=":material/task_alt:")

        col_save, col_cancel = st.columns(2)
        with col_save:
            if st.button("Enregistrer la réunion", icon=":material/save:", type="primary", width="stretch"):
                meetings = load_meetings()
                meetings.insert(0, st.session_state["pending_meeting"])
                save_meetings(meetings)
                st.toast("Réunion enregistrée.", icon=":material/check_circle:")
                del st.session_state["pending_meeting"]
                st.session_state.pop("transcription_finished", None)
                st.rerun()
        with col_cancel:
            if st.button("Annuler", icon=":material/close:", width="stretch"):
                del st.session_state["pending_meeting"]
                st.session_state.pop("transcription_finished", None)
                st.rerun()

        with st.expander("Transcription nettoyée", expanded=True):
            st.text_area("Texte nettoyé", st.session_state["pending_meeting"]["transcript_clean"], height=400)

# ═══════════════════════════════════════════════════════════════════════════
# ANALYSE DES RÉUNIONS
# ═══════════════════════════════════════════════════════════════════════════

with tab_analyse:
    if not meetings:
        ui.empty_state("Aucune réunion enregistrée", "Importez un enregistrement dans l'onglet « Nouvelle réunion ».")
    else:
        with st.container(border=True):
            ui.section_header(
                "Réunions enregistrées",
                "Sélectionnez une ou plusieurs réunions à analyser.",
                count=len(meetings),
            )
            labels = [
                f"{i} - {m.get('title', m.get('filename', 'Sans titre'))}"
                for i, m in enumerate(meetings)
            ]
            selected = st.multiselect("Réunions", labels, placeholder="Choisir des réunions…")

            _btn_rapport_col, _btn_sql_col = st.columns(2)
            with _btn_rapport_col:
                _btn_rapport = st.button("Générer le rapport d'amélioration", icon=":material/insights:", type="primary", width="stretch")
            with _btn_sql_col:
                _btn_sql_direct = st.button("Structurer et envoyer vers SQL Server", icon=":material/database:", width="stretch", key="btn_sql_pipeline")

        # ── Génération du rapport ──────────────────────────────────────────
        if _btn_rapport:
            if len(selected) == 0:
                st.warning("Sélectionnez au moins une réunion.")
            elif not MODEL:
                st.error("Modèle Gemini non configuré.")
            else:
                selected_indices = [int(i.split(" - ")[0]) for i in selected]
                transcripts = [meetings[idx]["transcript"] for idx in selected_indices]

                with st.spinner("Analyse en cours…"):
                    try:
                        report_text, kpis, pdf_header = generate_improvement_report(transcripts, MODEL)
                        st.session_state.improvement_report = report_text
                        st.session_state.kpis = kpis
                        st.session_state.pdf_header = pdf_header
                        st.session_state.selected_indices = selected_indices
                    except ResourceExhausted:
                        st.error("Quota API épuisé. Patientez une minute puis réessayez.")
                    except Exception as e:
                        st.error(f"Erreur pendant l'analyse : {e}")

                for _k in ("pro_report", "pro_pdf_bytes", "pro_audio_bytes"):
                    st.session_state.pop(_k, None)

        # ── Structuration SQL ──────────────────────────────────────────────
        if _btn_sql_direct:
            if len(selected) == 0:
                st.warning("Sélectionnez au moins une réunion.")
            elif not MODEL:
                st.error("Modèle Gemini non configuré.")
            else:
                _sql_selected_indices = [int(i.split(" - ")[0]) for i in selected]

                _sql_check = utils_sql.check_connection()
                if not _sql_check["ok"]:
                    st.error(f"Impossible de joindre SQL Server : {_sql_check['message']}")
                    st.stop()

                with st.spinner("Étape 1/2 — Gemini structure les données de la transcription…"):
                    try:
                        _structured_all = []
                        for _idx in _sql_selected_indices:
                            _m = meetings[_idx]
                            _src_id = _m.get("meeting_id", str(_idx))
                            if utils_sql.meeting_already_inserted(_src_id):
                                st.warning(f"« {_m.get('title', '?')} » est déjà en base — ignorée.")
                                continue
                            _transcript = _m.get("transcript_clean", _m.get("transcript", ""))
                            _structured = utils_ai_structurer.structure_transcript_for_sql(
                                transcript=_transcript,
                                report_text=_transcript,
                                kpis=None,
                                model=MODEL,
                                meeting_title=_m.get("title", "Réunion")
                            )
                            _valid, _errs = utils_ai_structurer.validate_structured_data(_structured)
                            if not _valid:
                                st.warning(f"Données partiellement invalides pour « {_m.get('title', '?')} » : {_errs}")
                            _structured_all.append((_idx, _src_id, _m, _structured))

                        st.session_state.sql_structured_data = _structured_all
                    except Exception as _e:
                        st.error(f"Erreur lors de la structuration IA : {_e}")
                        st.stop()

                if st.session_state.get("sql_structured_data"):
                    with st.spinner("Étape 2/2 — Insertion dans SQL Server…"):
                        try:
                            _all_stats = []
                            for (_idx, _src_id, _m, _structured) in st.session_state.sql_structured_data:
                                _raw_segs = _m.get("segments_clean", _m.get("segments", []))
                                _stats = utils_sql.insert_meeting_full(
                                    structured=_structured,
                                    source_meeting_id=_src_id,
                                    raw_segments=_raw_segs
                                )
                                _all_stats.append((_m.get("title", "?"), _stats))
                            st.session_state.sql_insert_stats = _all_stats
                        except Exception as _e:
                            st.error(f"Erreur SQL lors de l'insertion : {_e}")
                            st.stop()

                st.rerun()

        if "sql_insert_stats" in st.session_state:
            for _title, _stats in st.session_state.sql_insert_stats:
                _total_rows = sum(v for k, v in _stats.items() if k not in ["meeting_id_sql", "success"])
                st.success(
                    f"**Synchronisé avec SQL Server — {_title}**  \n"
                    f"meeting_id SQL #{_stats.get('meeting_id_sql')} · {_stats.get('segments', 0)} segments · "
                    f"{_stats.get('topics', 0)} sujets · {_stats.get('decisions', 0)} décisions · "
                    f"{_stats.get('actions', 0)} actions · 1 rapport ({_total_rows} lignes insérées).  \n"
                    "Actualisez le dataset Power BI pour voir les nouvelles données.",
                    icon=":material/database:",
                )

        if st.session_state.get("sql_structured_data"):
            with st.expander("Données structurées par l'IA (JSON)"):
                for (_idx, _src_id, _m, _structured) in st.session_state.sql_structured_data:
                    st.caption(f"Réunion : {_m.get('title', '?')} — source_meeting_id : {_src_id}")
                    st.json(_structured)

        if "sql_insert_stats" in st.session_state or "sql_structured_data" in st.session_state:
            if st.button("Effacer les résultats SQL", icon=":material/delete:", key="btn_sql_reset"):
                for _k in ["sql_structured_data", "sql_insert_stats"]:
                    st.session_state.pop(_k, None)
                st.rerun()

        # ── Rapport ────────────────────────────────────────────────────────
        if st.session_state.get("improvement_report"):
            with st.container(border=True):
                ui.section_header("Rapport d'amélioration")
                kpis = st.session_state.get("kpis") or {}
                if kpis.get("global_score") is not None:
                    st.metric("Score global", f"{kpis.get('global_score')}/100")
                st.text_area("Rapport", st.session_state.improvement_report, height=450, label_visibility="collapsed")

                try:
                    pdf_text = st.session_state.improvement_report
                    if kpis:
                        pdf_text = f"SCORE GLOBAL: {kpis.get('global_score')}/100\n\n" + pdf_text
                    pdf_bytes = utils_pdf.create_pdf(pdf_text, title=st.session_state.get("pdf_header"))
                    st.download_button(
                        label="Télécharger le rapport (PDF)",
                        icon=":material/download:",
                        data=pdf_bytes,
                        file_name="rapport_amelioration.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Erreur PDF : {e}")

            # ── Compte rendu formel ────────────────────────────────────────
            with st.container(border=True):
                ui.section_header("Compte rendu formel", "Document de type « minutes » rédigé à partir de l'analyse.")

                if st.button("Générer le compte rendu", icon=":material/description:", width="stretch", key="btn_gen_pro_re_fixed", type="primary"):
                    with st.spinner("Rédaction en cours…"):
                        try:
                            selected_indices = st.session_state.get("selected_indices", [])
                            titles = [meetings[idx].get("title", "Sans titre") for idx in selected_indices]
                            pro_minutes = generate_pro_minutes(st.session_state.improvement_report, MODEL, titles=titles)
                            st.session_state.pro_report = pro_minutes
                            st.session_state.pro_pdf_header = "COMPTE RENDU DE RÉUNION"
                            st.session_state.pro_pdf_bytes = utils_pdf.create_pdf(pro_minutes, title=st.session_state.pro_pdf_header)
                        except Exception as e:
                            st.error(f"Erreur : {e}")

                if "pro_report" in st.session_state:
                    edited_report = st.text_area(
                        "Relisez et modifiez le texte, puis enregistrez pour mettre à jour le PDF.",
                        st.session_state.pro_report, height=400, key="pro_report_editor_main",
                    )

                    c1, c2, c3 = st.columns(3)
                    with c1:
                        if st.button("Enregistrer les modifications", icon=":material/save:", width="stretch", key="save_pro_edits_main"):
                            st.session_state.pro_report = edited_report
                            st.session_state.pro_pdf_bytes = utils_pdf.create_pdf(edited_report, title=st.session_state.pro_pdf_header)
                            st.toast("PDF mis à jour.", icon=":material/check_circle:")
                            st.rerun()
                    with c2:
                        if "pro_pdf_bytes" in st.session_state:
                            st.download_button(
                                label="Télécharger (PDF)",
                                icon=":material/download:",
                                data=st.session_state.pro_pdf_bytes,
                                file_name="compte_rendu_pro.pdf",
                                mime="application/pdf",
                                key="dl_pro_main",
                                width="stretch"
                            )
                    with c3:
                        if st.button("Version audio", icon=":material/volume_up:", key="gen_audio_pro_main", width="stretch"):
                            with st.spinner("Génération de l'audio…"):
                                audio_raw = utils_audio.text_to_speech(st.session_state.pro_report)
                                if audio_raw:
                                    st.session_state.pro_audio_bytes = audio_raw

                    if "pro_audio_bytes" in st.session_state:
                        st.audio(st.session_state.pro_audio_bytes, format="audio/mp3")

            # ── Email de suivi ─────────────────────────────────────────────
            with st.container(border=True):
                ui.section_header("Email de suivi", "Brouillon prêt à envoyer, basé sur l'analyse.")

                if st.button("Rédiger l'email", icon=":material/mail:", type="primary"):
                    with st.spinner("Rédaction de l'email…"):
                        try:
                            st.session_state.email_draft = generate_followup_email(
                                st.session_state.improvement_report,
                                st.session_state.kpis,
                                MODEL
                            )
                        except ResourceExhausted:
                            st.error("Quota API épuisé. Réessayez dans une minute.")
                        except Exception as e:
                            st.error(f"Erreur : {e}")

                if "email_draft" in st.session_state:
                    st.text_area("Brouillon", st.session_state.email_draft, height=250)
                    st.caption("Conseil : personnalisez la première phrase avant d'envoyer.")

            # ── Objections ─────────────────────────────────────────────────
            with st.container(border=True):
                ui.section_header("Objections et blocages", "Détection des freins du client et réponses suggérées.")

                if st.button("Analyser les objections", icon=":material/report:", type="primary"):
                    with st.spinner("Analyse des objections…"):
                        if "selected_indices" in st.session_state:
                            try:
                                full_transcript = ""
                                for idx in st.session_state.selected_indices:
                                    full_transcript += meetings[idx].get("transcript", "") + "\n\n"
                                st.session_state.objections = extract_objections(full_transcript, MODEL)
                            except ResourceExhausted:
                                st.error("Quota API épuisé. Réessayez dans une minute.")
                            except Exception as e:
                                st.error(f"Erreur : {e}")
                        else:
                            st.error("Transcriptions introuvables. Régénérez le rapport.")

                if st.session_state.get("objections"):
                    for obj in st.session_state.objections:
                        st.markdown(f"**{obj.get('type')}** · {obj.get('technique')}")
                        st.info(f"« {obj.get('objection')} »", icon=":material/format_quote:")
                        st.success(f"Réponse : {obj.get('reponse')}", icon=":material/reply:")
                elif "objections" in st.session_state:
                    st.success("Aucune objection majeure détectée.", icon=":material/check_circle:")

# ═══════════════════════════════════════════════════════════════════════════
# AUDIT GLOBAL
# ═══════════════════════════════════════════════════════════════════════════

with tab_audit:
    with st.container(border=True):
        ui.section_header(
            "Audit stratégique global",
            f"Synthèse consolidée de l'ensemble des réunions ({len(meetings)}).",
        )
        if st.button("Générer l'audit global", icon=":material/monitoring:", type="primary", disabled=not (MODEL and meetings)):
            with st.spinner(f"Analyse de {len(meetings)} réunions…"):
                transcripts_dict = {
                    m.get('title', f"Meeting_{idx}"): m.get('transcript', '')
                    for idx, m in enumerate(meetings)
                }
                global_audit_text, global_kpis = generate_global_report(transcripts_dict, MODEL)
                st.session_state.global_audit = global_audit_text
                st.session_state.global_kpis = global_kpis
                st.session_state.global_pdf_bytes = utils_pdf.create_pdf(
                    global_audit_text, title="AUDIT STRATEGIQUE GLOBAL"
                )

    if "global_audit" in st.session_state:
        topics = (st.session_state.get("global_kpis") or {}).get("common_topics", [])
        if topics:
            st.caption("Sujets principaux")
            ui.tags(topics[:5])

        st.markdown(st.session_state.global_audit)

        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "Télécharger l'audit (PDF)",
                st.session_state.global_pdf_bytes,
                "Audit_Global_Strategique.pdf",
                "application/pdf",
                icon=":material/download:",
                width="stretch"
            )
        with c2:
            if st.button("Effacer l'audit", icon=":material/delete:", width="stretch"):
                for _k in ("global_audit", "global_kpis", "global_pdf_bytes"):
                    st.session_state.pop(_k, None)
                st.rerun()
