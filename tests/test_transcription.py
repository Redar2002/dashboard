from utils_transcription import _shift_timestamps, parse_transcript_to_segments


def test_parse_segments_with_speakers():
    text = "[00:05] Ahmed : Bonjour\n[00:12] [Mouad] : Salut\nsuite du message"
    segments, pure = parse_transcript_to_segments(text)
    assert [s["speaker"] for s in segments] == ["Ahmed", "Mouad"]
    assert segments[0]["start"] == 5.0
    assert segments[1]["text"] == "Salut suite du message"
    assert pure == "Bonjour Salut suite du message"


def test_parse_segments_hours_and_overlap():
    segments, _ = parse_transcript_to_segments("[1:00:00] A : un\n[1:00:02] B : deux")
    assert segments[0]["start"] == 3600.0
    # La fin du premier segment ne dépasse pas le début du suivant
    assert segments[0]["end"] == 3602.0


def test_parse_text_without_timestamp():
    segments, pure = parse_transcript_to_segments("texte libre")
    assert segments[0]["speaker"] == "unknown"
    assert pure == "texte libre"


def test_shift_timestamps():
    assert _shift_timestamps("[00:30] A : x", 600) == "[10:30] A : x"
    assert _shift_timestamps("[59:30] A : x", 60) == "[01:00:30] A : x"
