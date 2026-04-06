import os
import json

DATA_FILE = "meetings.json"

def load_meetings():
    if not os.path.exists(DATA_FILE):
        return []
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
