import json
import re

def clean_text_content(text):
    if not text:
        return ""
    
    # 1. Fix specific "stuttering" patterns (short words repeated)
    # e.g. "de la de la de la" -> "de la"
    # Matches a word/phrase repeated 2+ times with spaces
    # \b(.+?)\b(\s+\1\b)+ -> replace with \1
    # We run this in a loop to catch nested/multiple occurrences
    
    prev_text = None
    while prev_text != text:
        prev_text = text
        # Remove immediate word/phrase repetitions (min 3 chars to avoid false positives like "a a")
        # Allow apostrophes in words for French (e.g. "d'un", "l'appel")
        text = re.sub(r'\b([a-zA-Z\u00C0-\u00FF][a-zA-Z\u00C0-\u00FF \'\s]{2,}?)\s+(?:\1\s+)+\1\b', r'\1', text, flags=re.IGNORECASE)
        # Also catch simple single word repetitions like "de de de" or "d'un d'un"
        text = re.sub(r'\b([a-zA-Z\u00C0-\u00FF\']+)\s+(?:\1\s+)+\1\b', r'\1', text, flags=re.IGNORECASE)

    # 2. Split into sentences/clauses to find duplicate sentences
    # Split by punctuation
    parts = re.split(r'([.!?]+)', text)
    
    cleaned_parts = []
    if len(parts) > 1:
        # Re-assemble with delimiters
        sentences = []
        current_sent = ""
        for p in parts:
            current_sent += p
            if re.match(r'[.!?]+', p):
                sentences.append(current_sent.strip())
                current_sent = ""
        if current_sent:
            sentences.append(current_sent.strip())
            
        # Deduplicate consecutive sentences
        if sentences:
            cleaned_parts.append(sentences[0])
            for i in range(1, len(sentences)):
                prev_s = sentences[i-1]
                curr_s = sentences[i]
                
                # Calculate similarity or containment
                # Simple check: identical or contained
                clean_prev = re.sub(r'\W+', '', prev_s).lower()
                clean_curr = re.sub(r'\W+', '', curr_s).lower()
                
                if not clean_curr:
                    continue
                    
                if clean_prev == clean_curr:
                    continue
                
                # Check if current is a substring of previous (hallucination often repeats parts)
                if len(clean_curr) > 10 and clean_curr in clean_prev:
                    continue
                    
                cleaned_parts.append(curr_s)
        
        text = " ".join(cleaned_parts)

    return text

def remove_repetitive_segments(segments):
    cleaned_segments = []
    
    valid_segments = [s for s in segments if s.get('text', '').strip()]
    if not valid_segments:
        return []

    # First, clean content INSIDE each segment
    for seg in valid_segments:
        original_text = seg.get('text', '')
        cleaned_text = clean_text_content(original_text)
        seg['text'] = cleaned_text
        cleaned_segments.append(seg)
    
    # Second, deduplicate ACROSS segments (same as before)
    final_segments = []
    if cleaned_segments:
        final_segments.append(cleaned_segments[0])
        for i in range(1, len(cleaned_segments)):
            current = cleaned_segments[i]
            prev = final_segments[-1]
            
            curr_text = re.sub(r'\s+', ' ', current.get('text', '')).strip()
            prev_text = re.sub(r'\s+', ' ', prev.get('text', '')).strip()
            
            if not curr_text:
                continue

            if curr_text == prev_text:
                continue
                
            if len(curr_text) < 20 and curr_text in prev_text:
                 continue
            
            final_segments.append(current)
            
    return final_segments

def regenerate_transcript(segments):
    return "\n".join([s.get('text', '').strip() for s in segments if s.get('text', '').strip()])

def main():
    input_file = r'd:\meeting_improvement\meetings_cleaned_corrected.json'
    output_file = r'd:\meeting_improvement\meetings_cleaned_v2.json'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        return

    for meeting in data:
        original_segments = meeting.get('segments', [])
        # We process 'original_segments' but we should assume we might modify them in place if we aren't careful,
        # but here we create new lists.
        
        print(f"Processing Meeting {meeting.get('meeting_id')}...")
        cleaned = remove_repetitive_segments(original_segments)
        
        # Calculate stats
        orig_len = sum(len(s.get('text', '')) for s in original_segments)
        new_len = sum(len(s.get('text', '')) for s in cleaned)
        
        print(f"  Segments: {len(original_segments)} -> {len(cleaned)}")
        print(f"  Characters: {orig_len} -> {new_len}")
        
        meeting['segments'] = cleaned
        meeting['transcript'] = regenerate_transcript(cleaned)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved cleaned data to {output_file}")

if __name__ == "__main__":
    main()
