import utils_data


def test_demo_mode_uses_fictional_meetings(monkeypatch):
    monkeypatch.setenv("DEMO_MODE", "1")
    meetings = utils_data.load_meetings()
    assert utils_data.data_file() == utils_data.DEMO_FILE
    assert len(meetings) >= 5
    assert all(m["title"] and m["transcript"] for m in meetings)


def test_real_data_by_default(monkeypatch):
    monkeypatch.delenv("DEMO_MODE", raising=False)
    assert utils_data.data_file() == utils_data.REAL_FILE
