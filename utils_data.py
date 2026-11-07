import os
import json

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

_ROOT = os.path.dirname(os.path.abspath(__file__))
REAL_FILE = os.path.join(_ROOT, "meetings.json")
DEMO_FILE = os.path.join(_ROOT, "demo", "meetings_demo.json")


def is_demo() -> bool:
    """Mode démo (DEMO_MODE=1 dans .env) : réunions fictives, infos personnelles masquées."""
    return os.getenv("DEMO_MODE", "").strip().lower() in ("1", "true", "oui", "yes")


def data_file() -> str:
    return DEMO_FILE if is_demo() else REAL_FILE


def load_meetings():
    path = data_file()
    if not os.path.exists(path):
        return []
    # Le fichier n'est relu que s'il a changé (date de modification dans la clé de cache)
    return _read_meetings(path, os.path.getmtime(path))


@st.cache_data(show_spinner=False)
def _read_meetings(path: str, mtime: float):
    with open(path, "r", encoding="utf8") as f:
        data = json.load(f)
        
        # Ensure list format
        if isinstance(data, dict):
            data = [data]
            
        # Backfill transcript if missing
        for meeting in data:
            if "transcript" not in meeting and "segments" in meeting:
                meeting["transcript"] = "\n".join([s.get("text", "") for s in meeting["segments"]])
                
        return data

def save_meetings(meetings):
    with open(data_file(), "w", encoding="utf8") as f:
        json.dump(meetings, f, indent=2, ensure_ascii=False)
