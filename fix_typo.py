import json
import logging

def main():
    file_path = "d:/meeting_improvement/meetings.json"
    meeting_id = "20260203_104028"
    
    with open(file_path, "r", encoding="utf8") as f:
        meetings = json.load(f)
    
    found = False
    for meeting in meetings:
        if meeting.get("meeting_id") == meeting_id:
            # Fix transcript
            if "Como" in meeting.get("transcript", ""):
                meeting["transcript"] = meeting["transcript"].replace("Como", "Kommo")
                found = True
                print("Fixed transcript.")
            
            # Fix segments
            count = 0
            for segment in meeting.get("segments", []):
                if "Como" in segment.get("text", ""):
                    segment["text"] = segment["text"].replace("Como", "Kommo")
                    count += 1
            if count > 0:
                print(f"Fixed {count} segments.")
                found = True
                
    if found:
        with open(file_path, "w", encoding="utf8") as f:
            json.dump(meetings, f, indent=2, ensure_ascii=False)
        print("Successfully updated meetings.json")
    else:
        print("No occurrences of 'Como' found to fix.")

if __name__ == "__main__":
    main()
