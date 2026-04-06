import io
from gtts import gTTS

def text_to_speech(text, lang='fr'):
    """
    Converts text to speech and returns the audio bytes.
    
    Args:
        text (str): The text to convert.
        lang (str): Language code (default 'fr' for French).
        
    Returns:
        bytes: Audio data in MP3 format.
    """
    try:
        # Filter out markdown formatting like #, **, --- for better speech quality
        clean_text = text.replace("#", "").replace("*", "").replace("-", " ")
        tts = gTTS(text=clean_text, lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp.getvalue()
    except Exception as e:
        print(f"Error in Text-to-Speech conversion: {e}")
        return None
