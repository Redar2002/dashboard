
import json
import os

filepath = r"d:\meeting_improvement\meetings.json"

if os.path.exists(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # On parcourt les réunions et on nettoie les répétitions dans le texte
    for meeting in data:
        if "segments" in meeting:
            for segment in meeting["segments"]:
                if "text" in segment:
                    lines = segment["text"].split('\n')
                    new_lines = []
                    last_line = ""
                    count = 0
                    for line in lines:
                        if line.strip() == last_line.strip() and line.strip() != "":
                            count += 1
                        else:
                            count = 1
                        if count <= 5: # On garde max 5 répétitions consécutives (marge de sécurité)
                            new_lines.append(line)
                            last_line = line
                    segment["text"] = '\n'.join(new_lines)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Nettoyage de meetings.json terminé.")
else:
    print("Fichier non trouvé.")
