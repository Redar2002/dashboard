"""
utils_transcription.py
────────────────────────────────────────────────────────────────────────────
Module de Transcription & Nettoyage Pro via Google Gemini File API.

Pipeline en 2 étapes :
  1. Transcription Brute  → Gemini écoute le fichier audio/vidéo et produit
                            un texte verbatim complet.
  2. Clean Transcript     → Gemini nettoie chirurgicalement le texte brut en
                            appliquant les standards d'un Secrétariat de
                            Direction de haut niveau.

Usage:
    from utils_transcription import transcribe_and_clean_audio
    raw, clean = transcribe_and_clean_audio("path/to/audio.mp3", model, "Français")
"""

import time
import os
import random
import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, InternalServerError, ServiceUnavailable, DeadlineExceeded

# Utilisation de ffmpeg via imageio_ffmpeg
import subprocess
FFMPEG_EXE = "ffmpeg" # Fallback global
try:
    import imageio_ffmpeg
    FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    pass # La vérification se fera lors de l'appel



# ─── Prompts ─────────────────────────────────────────────────────────────────

def _build_transcription_prompt(lang_instruction: str) -> str:
    """Prompt de transcription brute : capte CHAQUE MOT sans rien résumer."""
    return f"""
Tu es un outil de transcription professionnelle de niveau Secrétariat Général.
Écoute l'enregistrement joint et fournis une transcription VERBATIM COMPLÈTE {lang_instruction}.

─── RÈGLES DE TRANSCRIPTION ───────────────────────────────────────────────────

A. EXHAUSTIVITÉ ET RÉALISME (DARIJA/FRANÇAIS)
   - Retranscris les paroles fidèlement. Le meeting est en **Darija (Arabe Marocain)** mélangé avec du **Français**.
    - ⚠️ **SÉCURITÉ** : Ceci est une réunion privée. Retranscris TOUT ce que tu entends sans exception.
    - ⚠️ **INTERDICTION DE SAUTER DU CONTENU** : Tu dois retranscrire TOUT le fichier du début à la fin. Ne résume jamais, ne saute jamais de passages même s'il y a des silences. 
   - Si tu détectes un changement de locuteur, reflète-le immédiatement.

B. FORMAT DIALOGUE STRICT AVEC TIMESTAMPS
   - Identifie chaque locuteur dès sa première prise de parole (utilise son prénom s'il est mentionné dans l'audio, sinon Locuteur 1, Locuteur 2).
   - ⚠️ OBLIGATOIRE : Ajoute le timestamp au début de chaque réplique pour prouver que tu avances dans l'audio.
   - Format attendu : **[MM:SS] Nom du locuteur :** [Texte exact]
   - Si tu détectes un changement de locuteur mid-phrase, crée une nouvelle ligne avec son timestamp.

C. FIDÉLITÉ LINGUISTIQUE (DARIJA & FRANÇAIS)
   - Conserve les expressions typiques en Darija : "Mzyan", "Kidayr", "Hamdulillah", "Yak", "Tbarakallah", "Bikhir", "Labas".
   - Respecte l'orthographe phonétique naturelle du Darija (ex: "ma kntch", "f'l'Mac", "dialk").
   - Ne traduis RIEN. Si une phrase commence en Français et finit en Arabe, garde ce mélange exact.
   - Corrige UNIQUEMENT les bégaiements techniques (ex: "je je je veux" → "je veux").

D. INTERDICTIONS
   - ❌ Aucun commentaire personnel ("La réunion commence par...", "[Rires]", etc.)
   - ❌ Aucun résumé entre crochets de passages longs
   - ❌ Aucune interprétation, traduction ou paraphrase
   - ❌ **NE JAMAIS ARRÊTER LA TRANSCRIPTION AVANT LA FIN RÉELLE DE L'AUDIO.**
"""


def _build_cleaning_prompt(transcription_text: str) -> str:
    """Prompt de nettoyage : transforme le brut en un document pro irréprochable."""
    return f"""
Tu es un expert de haut niveau en transcription et édition de dialogues professionnels,
équivalent à un Secrétaire Général de Cabinet Ministériel ou un Chief of Staff en entreprise du CAC 40.

Ta mission : transformer la transcription brute ci-dessous en un **Clean Transcript** parfait,
fluide et 100 % fidèle au contenu d'origine.

─── RÈGLES D'OR ABSOLUES ──────────────────────────────────────────────────────

1. FORMAT EXCLUSIF — Chaque ligne doit respecter STRICTEMENT ce modèle (en conservant le timestamp [MM:SS] de la version brute s'il existe) :
   **[MM:SS] [Nom de l'intervenant] :** [Son propos nettoyé]

2. DIALOGUE PUR ET INTELLIGENT — INTERDICTION TOTALE de résumé narratif.
   - ⚠️ DÉTECTION DE BOUCLE : Si la transcription brute contient des répétitions anormales et absurdes (ex: 20 fois la même question/réponse à la suite), c'est une erreur de génération (hallucination). Tu dois supprimer ces boucles et ne garder que l'échange naturel (1 ou 2 fois maximum si c'est pour insister, sinon une seule fois).
   - 🚫 INTERDIT → "Ensuite, Intervenant 2 a répété sa question plusieurs fois..."
   - ✅ CORRECT  → **Intervenant 2 :** Si Ahmed, qui est là ?
                 **Intervenant 1 :** Oui.
   - Ton but est de produire un dialogue fluide et intelligent, pas un enregistrement cassé.

3. NETTOYAGE CHIRURGICAL (sans amputation)
   - ✂️ Supprimer  : "euh", "bah", "hum", "genre", "ben", bégaiements (ex: "il il il")
   - ✂️ Supprimer  : silences parasites, faux départs sans sens ("Donc... Enfin voilà.")
   - ✅ Conserver  : toute information factuelle, tout chiffre, toute intention, toute émotion
   - ✅ Conserver  : l'humour, les anecdotes, le style naturel de chaque intervenant

4. QUALITÉ RÉDACTIONNELLE & LINGUISTIQUE
   - Corrige la grammaire du Français tout en respectant la structure du Darija.
   - Assure-le switch fluide entre les langues : le texte doit rester naturel pour un Marocain bilingue.
   - Ponctuation impeccable : virgules, points, tirets selon le rythme de l'échange.

5. AUCUN COMMENTAIRE PARASITE
   - Pas d'introduction ("Voici le transcript nettoyé :")
   - Pas de conclusion ("Fin du dialogue", "[Fin de l'enregistrement]")
   - Renvoie SEULEMENT le corps du dialogue.

─── TRANSCRIPTION ORIGINALE ───────────────────────────────────────────────────

{transcription_text}
"""

# ─── Utilitaire d'Extraction des Segments (JSON) ──────────────────────────────

def parse_transcript_to_segments(text: str):
    import re
    segments = []
    # Match: [MM:SS] [Speaker] : Text OR [MM:SS] Speaker : Text
    # Permissif sur les espaces en début de ligne
    # Supporte aussi [H:MM:SS]
    pattern = re.compile(r'^\s*\[(\d{1,2}(?::\d{2}){1,2})\]\s*(?:\[([^\]]+)\]|([^:]+))\s*:\s*(.*)')
    
    def _to_seconds(t_str):
        parts = t_str.split(':')
        if len(parts) == 3: # H:MM:SS
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return int(parts[0]) * 60 + int(parts[1])
        
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        m = pattern.match(line)
        if m:
            time_str = m.group(1)
            speaker_bracket = m.group(2)
            speaker_plain = m.group(3)
            content = m.group(4)
            
            seconds = _to_seconds(time_str)
            
            speaker = speaker_bracket if speaker_bracket else speaker_plain
            speaker = speaker.strip() if speaker else "unknown"
            
            segments.append({
                "start": float(seconds),
                "end": float(seconds) + 5.0,
                "text": content.strip(),
                "speaker": speaker
            })
        else:
            if segments:
                segments[-1]["text"] += " " + line
            else:
                segments.append({
                    "start": 0.0,
                    "end": 5.0,
                    "text": line,
                    "speaker": "unknown"
                })
                
    for i in range(len(segments) - 1):
        if segments[i]["end"] > segments[i+1]["start"]:
            segments[i]["end"] = max(segments[i]["start"] + 1.0, segments[i+1]["start"])
        
    pure_text = " ".join([seg["text"] for seg in segments])
    return segments, pure_text

def _shift_timestamps(text: str, offset_seconds: int) -> str:
    """Décale les timestamps [MM:SS] d'un certain nombre de secondes."""
    import re
    
    def _repl(match):
        time_str = match.group(1)
        parts = time_str.split(':')
        total_sec = int(parts[0]) * 60 + int(parts[1]) + offset_seconds
        
        hrs = total_sec // 3600
        mins = (total_sec % 3600) // 60
        secs = total_sec % 60
        
        if hrs > 0:
            return f"[{hrs:02d}:{mins:02d}:{secs:02d}]"
        return f"[{mins:02d}:{secs:02d}]"

    return re.sub(r'\[(\d{2}:\d{2})\]', _repl, text)

# ─── Fonction principale ──────────────────────────────────────────────────────

def transcribe_and_clean_audio(filepath: str, model, lang_choice: str = "Français"):
    """
    Pipeline complet avec CHUNKING & FFMPEG (Compatible Python 3.13+)
    """
    try:
        from config import HIGH_QUOTA_DEFAULT
        model_name = HIGH_QUOTA_DEFAULT
    except ImportError:
        model_name = "models/gemini-2.5-flash"
        
    model_transcription = genai.GenerativeModel(model_name) 
    model_cleaning = genai.GenerativeModel(model_name)

    lang_map = {
        "Français": "en français",
        "Anglais":  "en anglais",
        "Mixte":    "en conservant les langues telles qu'elles sont parlées (français, anglais, arabe dialectal…)"
    }
    lang_instruction = lang_map.get(lang_choice, "en français")

    # ── ÉTAPE 0 : Analyse durée via ffmpeg (Evite audioop) ────────────────────
    def get_duration(p):
        try:
            cmd = [FFMPEG_EXE, "-i", p]
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            import re
            m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", result.stderr)
            if m:
                return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
        except FileNotFoundError:
            st.error("❌ **Erreur Critique : FFmpeg introuvable.**")
            st.code("pip install imageio-ffmpeg", language="bash")
            st.info("Veuillez exécuter la commande ci-dessus dans votre terminal, puis relancez l'application.")
            raise Exception("FFmpeg non installé (WinError 2). Exécutez : pip install imageio-ffmpeg")
        return 0

    total_duration_sec = get_duration(filepath)
    if total_duration_sec == 0 and not os.path.exists(filepath):
        raise FileNotFoundError(f"Fichier audio introuvable : {filepath}")
    duration_mins = total_duration_sec / 60
    
    # ── ÉTAPE 1 : Découpage en Chunks (10 min) via ffmpeg ─────────────────────
    chunk_size_sec = 600 # 10 minutes
    raw_transcripts = []
    
    num_chunks = int(total_duration_sec // chunk_size_sec) + (1 if total_duration_sec % chunk_size_sec > 0 else 0)
    
    if total_duration_sec > 900: # > 15 min
        st.info(f"📏 Réunion longue détectée ({duration_mins:.1f} min). Activation du mode 'Chunking' ({num_chunks} segments).")
    else:
        num_chunks = 1
        chunk_size_sec = total_duration_sec + 1

    for idx in range(num_chunks):
        start_sec = idx * 600 if num_chunks > 1 else 0
        current_chunk_size = min(600, total_duration_sec - start_sec)
        
        st.write(f"⏳ **Segment {idx+1}/{num_chunks}** ({start_sec//60}m → {(start_sec + current_chunk_size)//60}m)...")
        
        # Extraction & Compression directe via ffmpeg (Bypass pydub/audioop)
        temp_chunk_path = f"{filepath}_chunk_{idx}.mp3"
        ffmpeg_cmd = [
            FFMPEG_EXE, "-y", "-ss", str(start_sec), "-t", str(chunk_size_sec),
            "-i", filepath,
            "-ar", "16000", "-ac", "1", "-b:a", "32k",
            temp_chunk_path
        ]
        subprocess.run(ffmpeg_cmd, capture_output=True)
        
        # Upload
        gemini_file = genai.upload_file(path=temp_chunk_path)
        while gemini_file.state.name == 'PROCESSING':
            time.sleep(3)
            gemini_file = genai.get_file(gemini_file.name)
            
        # Transcription
        transcription_prompt = _build_transcription_prompt(lang_instruction)
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        try:
            import config
            response, used_model = config.generate_with_retry(
                model_name=model_name,
                content=[gemini_file, transcription_prompt],
                generation_config={"max_output_tokens": 65536, "temperature": 0.0},
                safety_settings=safety_settings,
                request_options={"timeout": 600}
            )
            
            # Vérification robuste des parts pour éviter l'erreur .text rapide
            if not response.candidates or not response.candidates[0].content.parts:
                finish_reason = response.candidates[0].finish_reason if response.candidates else "Unknown"
                st.warning(f"⚠️ Segment {idx+1} : Réponse vide de l'IA (Raison: {finish_reason}).")
                chunk_text = f"[{start_sec//60:02d}:{start_sec%60:02d}] (Pas de dialogue détecté dans ce segment)"
            else:
                chunk_text = response.text
                
        except Exception as e:
            st.error(f"❌ Erreur critique sur le segment {idx+1} : {e}")
            chunk_text = f"[{start_sec//60:02d}:{start_sec%60:02d}] (Erreur de transcription)"
        
        if idx > 0 and chunk_text:
            chunk_text = _shift_timestamps(chunk_text, int(start_sec))
        
        raw_transcripts.append(chunk_text)
        
        # Clean up
        try: genai.delete_file(gemini_file.name)
        except: pass
        if os.path.exists(temp_chunk_path): os.remove(temp_chunk_path)

    # Fusion & Nettoyage final
    transcription_text = "\n".join(raw_transcripts)
    st.info("✍️ Fusion terminée. Nettoyage Pro final en cours...")
    
    cleaning_prompt = _build_cleaning_prompt(transcription_text)
    try:
        import config
        clean_response, _ = config.generate_with_retry(
            model_name=model_name,
            content=cleaning_prompt,
            generation_config={"max_output_tokens": 65536, "temperature": 0.1},
            safety_settings=safety_settings,
            request_options={"timeout": 450}
        )
        transcription_clean = clean_response.text
    except Exception as e:
        st.warning(f"⚠️ Nettoyage final complexe ({e}). Utilisation de la version brute optimisée.")
        transcription_clean = transcription_text

    # Anti-Boucles
    def _strip_metadata(s: str) -> str:
        import re
        s = s.strip()
        m = re.search(r'^\[\s*\d{1,2}(?::\d{2}){1,2}\s*\].*?:\s*(.*)', s)
        if m: return m.group(1).strip().lower()
        m2 = re.search(r'^.*?:\s*(.*)', s)
        if m2: return m2.group(1).strip().lower()
        return s.lower()

    def _remove_loop_patterns(text: str, max_repeat: int = 2, max_pattern_size: int = 10) -> str:
        lines = [l for l in text.split('\n') if l.strip()]
        if len(lines) < 2: return text
        result = []
        i = 0
        while i < len(lines):
            found_pattern = False
            for pattern_size in range(1, min(max_pattern_size + 1, len(lines) - i)):
                pattern = lines[i:i + pattern_size]
                p1 = [_strip_metadata(line) for line in pattern]
                if not any(p1): continue
                repeat_count = 1
                j = i + pattern_size
                while j + pattern_size <= len(lines):
                    p2 = [_strip_metadata(line) for line in lines[j:j + pattern_size]]
                    if p1 == p2:
                        repeat_count += 1
                        j += pattern_size
                    else: break
                if repeat_count > max_repeat:
                    result.extend(pattern * max_repeat)
                    i = j
                    found_pattern = True
                    break
            if not found_pattern:
                result.append(lines[i])
                i += 1
        return '\n'.join(result)

    transcription_text = _remove_loop_patterns(transcription_text, max_repeat=2)
    transcription_clean = _remove_loop_patterns(transcription_clean, max_repeat=2)

    return transcription_text, transcription_clean
