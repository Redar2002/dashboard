import os
import json

import streamlit as st

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meetings.json")

def load_meetings():
    if not os.path.exists(DATA_FILE):
        return []
    # Le fichier n'est relu que s'il a changé (date de modification dans la clé de cache)
    return _read_meetings(os.path.getmtime(DATA_FILE))


@st.cache_data(show_spinner=False)
def _read_meetings(mtime: float):
    with open(DATA_FILE, "r", encoding="utf8") as f:
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
    with open(DATA_FILE, "w", encoding="utf8") as f:
        json.dump(meetings, f, indent=2, ensure_ascii=False)
