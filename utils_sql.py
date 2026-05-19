"""
utils_sql.py — Connexion et insertions SQL Server pour Meeting Intelligence
Windows Authentication · ODBC Driver 17 for SQL Server
"""
import pyodbc
import streamlit as st
from datetime import date


# ─── Détection automatique du driver ODBC ────────────────────────────────────

def _get_best_driver() -> str:
    """Retourne le meilleur driver SQL Server disponible sur la machine."""
    available = pyodbc.drivers()
    for preferred in ["ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server", "SQL Server"]:
        if preferred in available:
            return preferred
    raise EnvironmentError(
        f"Aucun driver SQL Server trouvé. Drivers disponibles : {available}"
    )


# ─── Connexion ────────────────────────────────────────────────────────────────

def get_sql_connection(server: str = "localhost", database: str = "MeetingIntelligence"):
    """
    Retourne une connexion pyodbc en Windows Authentication.
    Essaie ODBC Driver 18 puis 17 automatiquement.
    """
    driver = _get_best_driver()
    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"  # évite l'erreur TLS avec Driver 18
    )
    return pyodbc.connect(conn_str, timeout=10)


def check_connection(server: str = "localhost", database: str = "MeetingIntelligence") -> dict:
    """
    Teste la connexion et retourne un dict {ok, driver, message}.
    Utilisé par le bouton de diagnostic dans l'interface.
    """
    try:
        driver = _get_best_driver()
        conn = get_sql_connection(server, database)
        cursor = conn.cursor()
        cursor.execute("SELECT DB_NAME(), @@VERSION")
        db_name, version = cursor.fetchone()
        conn.close()
        return {
            "ok": True,
            "driver": driver,
            "database": db_name,
            "message": f"Connecté à '{db_name}' via «{driver}»",
            "version": version.split("\n")[0]
        }
    except Exception as e:
        return {"ok": False, "driver": "N/A", "message": str(e)}


# ─── Contrôle doublon ─────────────────────────────────────────────────────────

def meeting_already_inserted(source_meeting_id: str, server: str = "localhost", database: str = "MeetingIntelligence") -> bool:
    """
    Vérifie si ce meeting (identifié par son source_meeting_id JSON)
    a déjà été inséré dans SQL Server.
    """
    try:
        conn = get_sql_connection(server, database)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM meetings WHERE source_meeting_id = ?",
            (source_meeting_id,)
        )
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except Exception:
        return False


# ─── Insertion complète ───────────────────────────────────────────────────────

def insert_meeting_full(
    structured: dict,
    source_meeting_id: str,
    raw_segments: list = None,
    server: str = "localhost",
    database: str = "MeetingIntelligence"
) -> dict:
    """
    Insère toutes les données structurées dans SQL Server.

    Args:
        structured : dict produit par utils_ai_structurer (client, meeting, topics,
                     decisions, actions, report)
        source_meeting_id : identifiant issu du JSON local (meeting_id du meetings.json)
        raw_segments      : liste de segments bruts [{start, end, text}]
        server / database : paramètres de connexion

    Returns:
        dict avec les compteurs par table et le meeting_id SQL généré
    """
    conn = get_sql_connection(server, database)
    cursor = conn.cursor()
    stats = {}

    try:
        # ── 1. Client ──────────────────────────────────────────────────────────
        client = structured.get("client", {})
        client_name = client.get("client_name", "Inconnu")
        client_email = client.get("client_email", "")

        # Réutilise le client si déjà existant (par nom)
        cursor.execute(
            "SELECT client_id FROM clients WHERE client_name = ?",
            (client_name,)
        )
        row = cursor.fetchone()
        if row:
            client_id = row[0]
        else:
            cursor.execute(
                "INSERT INTO clients (client_name, client_email) OUTPUT INSERTED.client_id VALUES (?, ?)",
                (client_name, client_email)
            )
            client_id = cursor.fetchone()[0]
        stats["clients"] = 1

        # ── 2. Meeting ─────────────────────────────────────────────────────────
        meeting = structured.get("meeting", {})
        cursor.execute(
            """
            INSERT INTO meetings
                (title, date, duration, sentiment_score, client_id, source_meeting_id)
            OUTPUT INSERTED.meeting_id
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                meeting.get("title", "Sans titre"),
                meeting.get("date", date.today().isoformat()),
                int(meeting.get("duration", 0)),
                float(meeting.get("sentiment_score", 0)),
                client_id,
                source_meeting_id
            )
        )
        meeting_id = cursor.fetchone()[0]
        stats["meetings"] = 1

        # ── 3. Segments ────────────────────────────────────────────────────────
        segments = raw_segments or []
        if segments:
            for seg in segments:
                cursor.execute(
                    "INSERT INTO segments (meeting_id, start_time, end_time, text) VALUES (?, ?, ?, ?)",
                    (
                        meeting_id,
                        float(seg.get("start", 0)),
                        float(seg.get("end", 0)),
                        seg.get("text", "")
                    )
                )
            stats["segments"] = len(segments)

        # ── 4. Topics ──────────────────────────────────────────────────────────
        topics = structured.get("topics", [])
        for t in topics:
            name = t if isinstance(t, str) else t.get("topic_name", str(t))
            cursor.execute(
                "INSERT INTO topics (meeting_id, topic_name) VALUES (?, ?)",
                (meeting_id, name)
            )
        stats["topics"] = len(topics)

        # ── 5. Decisions ───────────────────────────────────────────────────────
        decisions = structured.get("decisions", [])
        for d in decisions:
            text = d if isinstance(d, str) else d.get("decision_text", str(d))
            cursor.execute(
                "INSERT INTO decisions (meeting_id, decision_text) VALUES (?, ?)",
                (meeting_id, text)
            )
        stats["decisions"] = len(decisions)

        # ── 6. Actions ─────────────────────────────────────────────────────────
        actions = structured.get("actions", [])
        for a in actions:
            if isinstance(a, str):
                text, assigned, status = a, "Non assigné", "À faire"
            else:
                text = a.get("action_text", str(a))
                assigned = a.get("assigned_to", "Non assigné")
                status = a.get("status", "À faire")
            cursor.execute(
                "INSERT INTO actions (meeting_id, action_text, assigned_to, status) VALUES (?, ?, ?, ?)",
                (meeting_id, text, assigned, status)
            )
        stats["actions"] = len(actions)

        # ── 7. Report ──────────────────────────────────────────────────────────
        report = structured.get("report", {})
        cursor.execute(
            "INSERT INTO reports (meeting_id, summary, pain_points, recommendations) VALUES (?, ?, ?, ?)",
            (
                meeting_id,
                report.get("summary", ""),
                report.get("pain_points", ""),
                report.get("recommendations", "")
            )
        )
        stats["reports"] = 1

        conn.commit()
        stats["meeting_id_sql"] = meeting_id
        stats["success"] = True
        return stats

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
