import json

import utils_data
from services import analyse


class _Response:
    def __init__(self, text):
        self.text = text


class _FakeModel:
    def __init__(self, text):
        self._text = text
        self.prompts = []

    def generate_content(self, prompt, **kwargs):
        self.prompts.append(prompt)
        return _Response(self._text)


MEETINGS = [{"title": "Démo CRM", "segments": [{"start": 65, "end": 70, "text": "Le budget est de 10 000 €"}]}]


def test_semantic_search_parses_json(monkeypatch):
    monkeypatch.setattr(utils_data, "load_meetings", lambda: MEETINGS)
    payload = {"results": [{"meeting_title": "Démo CRM", "timestamp": "01:05", "text": "budget", "relevance": 90}],
               "summary": "Le budget est de 10 000 €."}
    model = _FakeModel("```json\n" + json.dumps(payload) + "\n```")
    assert analyse.semantic_search("Quel budget ?", [0], model) == payload
    assert "[Démo CRM - 1:05]" in model.prompts[0]


def test_semantic_search_invalid_json(monkeypatch):
    monkeypatch.setattr(utils_data, "load_meetings", lambda: MEETINGS)
    result = analyse.semantic_search("?", [0], _FakeModel("pas du json"))
    assert result["results"] == []
