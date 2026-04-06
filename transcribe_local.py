"""
transcribe_local.py
────────────────────────────────────────────────────────────────────────────
Script autonome de Transcription & Nettoyage de réunions via Google Gemini.
Exécutable en ligne de commande, sans Streamlit.

Pipeline :
  1. (Optionnel) Compression audio si > 10 Mo
  2. Upload vers Gemini File API
  3. Transcription brute (gemini-2.5-flash)
  4. Nettoyage Pro (gemini-2.5-flash)
  5. Sauvegarde  : <nom>_raw.txt  et  <nom>_clean.txt

Usage :
    python transcribe_local.py "meeting.mp3"
    python transcribe_local.py "meeting.mp4" --lang Anglais --output-dir ./output
    python transcribe_local.py "meeting.mp3" --no-clean
    python transcribe_local.py "meeting.mp3" --no-compress

Prérequis :
    pip install google-generativeai python-dotenv pydub imageio-ffmpeg
"""

import argparse
import os
import sys
import time
import random
from pathlib import Path
from dotenv import load_dotenv

# ─── Chargement de la clé API ────────────────────────────────────────────────
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

try:
    import google.generativeai as genai
    from google.api_core.exceptions import (
        ResourceExhausted, InternalServerError, ServiceUnavailable, DeadlineExceeded
    )
except ImportError:
    print("❌ Package manquant. Installez : pip install google-generativeai")
    sys.exit(1)

# ─── Prompts ─────────────────────────────────────────────────────────────────

def _build_transcription_prompt(lang_instruction: str) -> str:
    return f"""
Tu es un outil de transcription professionnelle de niveau Secrétariat Général.
Écoute l'enregistrement joint et fournis une transcription VERBATIM COMPLÈTE {lang_instruction}.

─── RÈGLES DE TRANSCRIPTION ───────────────────────────────────────────────────

A. EXHAUSTIVITÉ ET RÉALISME (DARIJA/FRANÇAIS)
   - Retranscris les paroles fidèlement. Le meeting est en **Darija (Arabe Marocain)** mélangé avec du **Français**.
   - Ne bloque pas sur les silences ou les répétitions. Continue toujours à retranscrire la suite logique de l'audio jusqu'à la fin.
   - Si tu détectes un changement de locuteur, reflète-le immédiatement.

B. FORMAT DIALOGUE STRICT AVEC TIMESTAMPS
   - Identifie chaque locuteur dès sa première prise de parole (utilise son prénom s'il est mentionné dans l'audio, sinon Locuteur 1, Locuteur 2).
   - ⚠️ OBLIGATOIRE : Ajoute le timestamp au début de chaque réplique pour prouver que tu avances dans l'audio.
   - Format attendu : **[MM:SS] Nom du locuteur :** [Texte exact]
   - Si tu détectes un changement de locuteur mid-phrase, crée une nouvelle ligne avec son timestamp.

C. FIDÉLITÉ LINGUISTIQUE (DARIJA & FRANÇAIS)
   - Conserve les expressions typiques en Darija : "Mzyan", "Kidayr", "Hamdulillah", "Yak", "Tbarakallah".
   - Respecte l'orthographe phonétique naturelle du Darija (ex: "ma kntch", "f'l'Mac", "dialk").
   - Ne traduis RIEN. Garde le mélange exact des langues.
   - Corrige UNIQUEMENT les bégaiements techniques (ex: "je je je veux" → "je veux").

D. INTERDICTIONS
   - ❌ Aucun commentaire personnel ("La réunion commence par...", "[Rires]", etc.)
   - ❌ Aucun résumé entre crochets de passages longs
   - ❌ Aucune interprétation, traduction ou paraphrase
"""


def _build_cleaning_prompt(transcription_text: str) -> str:
    return f"""
Tu es un expert de haut niveau en transcription et édition de dialogues professionnels,
équivalent à un Secrétaire Général de Cabinet Ministériel ou un Chief of Staff en entreprise du CAC 40.

Ta mission : transformer la transcription brute ci-dessous en un **Clean Transcript** parfait,
fluide et 100 % fidèle au contenu d'origine.

─── RÈGLES D'OR ABSOLUES ──────────────────────────────────────────────────────

1. FORMAT EXCLUSIF — Chaque ligne doit respecter STRICTEMENT ce modèle (en conservant le timestamp [MM:SS] de la version brute s'il existe) :
   **[MM:SS] Nom de l'intervenant :** [Son propos nettoyé]

2. DIALOGUE PUR ET INTELLIGENT — INTERDICTION TOTALE de résumé narratif.
   - ⚠️ DÉTECTION DE BOUCLE : Si la transcription brute contient des répétitions anormales,
     supprime-les et ne garde que l'échange naturel (1 ou 2 fois maximum).
   - Ton but est de produire un dialogue fluide et intelligent.

3. NETTOYAGE CHIRURGICAL (sans amputation)
   - ✂️ Supprimer  : "euh", "bah", "hum", "genre", "ben", bégaiements (ex: "il il il")
   - ✂️ Supprimer  : silences parasites, faux départs sans sens
   - ✅ Conserver  : toute information factuelle, tout chiffre, toute intention, toute émotion
   - ✅ Conserver  : l'humour, les anecdotes, le style naturel de chaque intervenant

4. QUALITÉ RÉDACTIONNELLE & LINGUISTIQUE
   - Corrige la grammaire du Français tout en respectant la structure du Darija.
   - Ponctuation impeccable : virgules, points, tirets selon le rythme de l'échange.

5. AUCUN COMMENTAIRE PARASITE
   - Pas d'introduction ("Voici le transcript nettoyé :")
   - Pas de conclusion ("Fin du dialogue", "[Fin de l'enregistrement]")
   - Renvoie SEULEMENT le corps du dialogue.

─── TRANSCRIPTION ORIGINALE ───────────────────────────────────────────────────

{transcription_text}
"""


# ─── Utilitaire Anti-Boucles ──────────────────────────────────────────────────

def _remove_loop_patterns(text: str, max_repeat: int = 3, max_pattern_size: int = 10) -> str:
    """
    Détecte et supprime les patterns répétitifs (boucles) dans un texte.
    Gère les répétitions simples (A,A,A) ET les patterns alternants (A,B,A,B,A,B)
    ou N-grams jusqu'à max_pattern_size lignes.

    Args:
        text             : Texte à nettoyer.
        max_repeat       : Nombre max de répétitions tolérées.
        max_pattern_size : Taille max du pattern à détecter (en lignes).
    """
    lines = text.split('\n')
    if len(lines) < 4:
        return text

    result = []
    i = 0
    while i < len(lines):
        found_pattern = False
        for pattern_size in range(1, min(max_pattern_size + 1, len(lines) - i)):
            pattern = lines[i:i + pattern_size]
            repeat_count = 1
            j = i + pattern_size
            while j + pattern_size <= len(lines):
                if [l.strip() for l in lines[j:j + pattern_size]] == [l.strip() for l in pattern]:
                    repeat_count += 1
                    j += pattern_size
                else:
                    break
            if repeat_count > max_repeat:
                result.extend(pattern * max_repeat)
                i = j
                found_pattern = True
                break
        if not found_pattern:
            result.append(lines[i])
            i += 1

    return '\n'.join(result)


# ─── Appel Gemini avec Retry ──────────────────────────────────────────────────

def _generate_with_retry(model, prompt, generation_config, request_timeout=600,
                          max_retries=3, label=""):
    """Appelle model.generate_content() avec retry exponentiel sur les erreurs API."""
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config=generation_config,
                request_options={"timeout": request_timeout}
            )
            return response.text
        except (ResourceExhausted, InternalServerError, ServiceUnavailable, DeadlineExceeded) as e:
            if attempt < max_retries - 1:
                is_quota = isinstance(e, ResourceExhausted)
                base_delay = 60 if is_quota else 20
                wait = base_delay * (attempt + 1) + (random.random() * 10)
                error_type = "Quota 429" if is_quota else "Erreur Serveur"
                print(f"  ⏳ [{label}] {error_type} — nouvelle tentative dans {int(wait)}s... ({e})")
                time.sleep(wait)
            else:
                raise


# ─── Pipeline Principal ───────────────────────────────────────────────────────

def transcribe_and_clean(filepath: str, lang_choice: str = "Français",
                          no_clean: bool = False, no_compress: bool = False) -> tuple:
    """
    Pipeline complet : Upload → Transcription brute → Nettoyage Pro.

    Returns:
        (transcription_raw, transcription_clean)
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ GEMINI_API_KEY introuvable. Vérifiez votre fichier .env")

    genai.configure(api_key=api_key)

    model_name = "models/gemini-2.5-flash"
    model = genai.GenerativeModel(model_name)

    lang_map = {
        "Français": "en français",
        "Anglais":  "en anglais",
        "Mixte":    "en conservant les langues telles qu'elles sont parlées (français, anglais, arabe dialectal…)"
    }
    lang_instruction = lang_map.get(lang_choice, "en français")

    # ── ÉTAPE 0 : Compression si > 10 Mo ─────────────────────────────────────
    file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
    file_to_upload = filepath
    compressed_filepath = None

    if not no_compress and file_size_mb > 10:
        print(f"🗜️  Fichier > 10 Mo ({file_size_mb:.1f} Mo). Compression audio en cours...")
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(filepath)
            audio = audio.set_channels(1).set_frame_rate(8000)
            compressed_filepath = filepath + "_compressed.mp3"
            audio.export(compressed_filepath, format="mp3", bitrate="8k")
            new_size_mb = os.path.getsize(compressed_filepath) / (1024 * 1024)
            print(f"✅ Compression terminée : {file_size_mb:.1f} Mo → {new_size_mb:.1f} Mo")
            file_to_upload = compressed_filepath
            file_size_mb = new_size_mb
        except Exception as e:
            print(f"⚠️  Échec compression ({e}). Envoi du fichier original.")

    # ── ÉTAPE 1 : Upload vers Gemini File API ──────────────────────────────────
    print(f"📤 Envoi vers Gemini ({file_size_mb:.1f} Mo)...")
    if file_size_mb > 100:
        print("⚠️  Fichier volumineux — l'upload peut prendre plusieurs minutes.")

    gemini_file = None
    for attempt in range(3):
        try:
            gemini_file = genai.upload_file(path=file_to_upload)
            break
        except Exception as e:
            if attempt < 2:
                wait_time = 10 * (attempt + 1)
                print(f"  ⏳ Échec upload (tentative {attempt+1}/3) — attente {wait_time}s... ({e})")
                time.sleep(wait_time)
            else:
                raise Exception(f"❌ Échec définitif de l'upload : {e}")

    print(f"✅ Fichier reçu par Gemini (URI : {gemini_file.uri})")

    try:
        # Attente du traitement côté Google
        max_wait = 120
        waited = 0
        while gemini_file.state.name == 'PROCESSING':
            if waited >= max_wait:
                raise Exception("⏱️  Timeout : Gemini met trop de temps à traiter le fichier (>2 min).")
            print("  ⏳ Gemini traite le fichier média...", end="\r")
            time.sleep(5)
            waited += 5
            gemini_file = genai.get_file(gemini_file.name)

        if gemini_file.state.name == 'FAILED':
            raise Exception("❌ Le traitement du fichier par Gemini a échoué (état FAILED).")

        print("\n🎙️  Fichier prêt ! Transcription brute en cours...")

        # ── ÉTAPE 2 : Transcription brute ─────────────────────────────────────
        transcription_text = _generate_with_retry(
            model=model,
            prompt=[gemini_file, _build_transcription_prompt(lang_instruction)],
            generation_config={
                "max_output_tokens": 65536,
                "temperature": 0.4,
            },
            request_timeout=600,
            label="Transcription"
        )
        transcription_text = _remove_loop_patterns(transcription_text)

        print("✍️  Transcription brute terminée !")

        # ── ÉTAPE 3 : Nettoyage Pro ───────────────────────────────────────────
        transcription_clean = transcription_text  # fallback si --no-clean

        if not no_clean:
            print("🧹 Nettoyage Pro en cours...")
            try:
                transcription_clean = _generate_with_retry(
                    model=model,
                    prompt=_build_cleaning_prompt(transcription_text),
                    generation_config={
                        "max_output_tokens": 32768,
                        "temperature": 0.2,
                    },
                    request_timeout=300,
                    label="Nettoyage"
                )
                transcription_clean = _remove_loop_patterns(transcription_clean)
                print("✅ Nettoyage Pro terminé !")
            except Exception as e:
                print(f"⚠️  Nettoyage échoué ({e}). Version brute conservée.")
                transcription_clean = transcription_text

        if not transcription_clean:
            transcription_clean = transcription_text

        print("🎉 Pipeline terminé avec succès !")
        return transcription_text, transcription_clean

    finally:
        # Suppression systématique du fichier chez Google
        if gemini_file:
            try:
                genai.delete_file(gemini_file.name)
            except Exception:
                pass

        # Suppression du fichier compressé local
        if compressed_filepath and os.path.exists(compressed_filepath):
            try:
                os.remove(compressed_filepath)
            except Exception:
                pass


# ─── Sauvegarde des résultats ─────────────────────────────────────────────────

def save_results(audio_path: str, raw: str, clean: str, output_dir: str = None) -> tuple:
    """Sauvegarde raw et clean dans des fichiers .txt. Retourne (raw_path, clean_path)."""
    audio_path = Path(audio_path)
    stem = audio_path.stem

    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = audio_path.parent

    raw_path   = out_dir / f"{stem}_raw.txt"
    clean_path = out_dir / f"{stem}_clean.txt"

    raw_path.write_text(raw, encoding="utf-8")
    clean_path.write_text(clean, encoding="utf-8")

    return str(raw_path), str(clean_path)


# ─── Entrée CLI ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Transcription & Nettoyage de réunions via Google Gemini (sans Streamlit)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
  python transcribe_local.py meeting.mp3
  python transcribe_local.py meeting.mp4 --lang Anglais
  python transcribe_local.py meeting.mp3 --output-dir ./resultats
  python transcribe_local.py meeting.mp3 --no-clean
  python transcribe_local.py meeting.mp3 --no-compress
        """
    )
    parser.add_argument(
        "audio_file",
        help="Chemin vers le fichier audio/vidéo à transcrire"
    )
    parser.add_argument(
        "--lang",
        choices=["Français", "Anglais", "Mixte"],
        default="Français",
        help="Langue principale du meeting (défaut : Français)"
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Dossier de sauvegarde des .txt (défaut : même dossier que l'audio)"
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Sauter l'étape de nettoyage Pro (sauvegarder uniquement la transcription brute)"
    )
    parser.add_argument(
        "--no-compress",
        action="store_true",
        help="Ne pas compresser le fichier même s'il dépasse 10 Mo"
    )

    args = parser.parse_args()

    # Vérification du fichier
    if not os.path.exists(args.audio_file):
        print(f"❌ Fichier introuvable : {args.audio_file}")
        sys.exit(1)

    print("=" * 60)
    print("🎙️  TRANSCRIPTION & NETTOYAGE — Gemini 2.5 Flash")
    print("=" * 60)
    print(f"📁 Fichier  : {args.audio_file}")
    print(f"🌍 Langue   : {args.lang}")
    print(f"🧹 Nettoyage: {'Désactivé' if args.no_clean else 'Activé'}")
    print("=" * 60)

    try:
        raw, clean = transcribe_and_clean(
            filepath=args.audio_file,
            lang_choice=args.lang,
            no_clean=args.no_clean,
            no_compress=args.no_compress
        )

        raw_path, clean_path = save_results(
            audio_path=args.audio_file,
            raw=raw,
            clean=clean,
            output_dir=args.output_dir
        )

        print()
        print("=" * 60)
        print("📄 Fichiers sauvegardés :")
        print(f"   🔹 Brut   : {raw_path}")
        if not args.no_clean:
            print(f"   ✨ Propre  : {clean_path}")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
