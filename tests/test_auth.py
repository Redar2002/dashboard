import auth


def test_no_default_admin(monkeypatch):
    monkeypatch.delenv("ADMIN_EMAIL", raising=False)
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)
    monkeypatch.setattr(auth, "get_user_by_email", lambda *a, **k: None)
    assert auth.login_user("admin@inspirigence.ma", "admin123")["ok"] is False


def test_env_admin(monkeypatch):
    monkeypatch.setenv("ADMIN_EMAIL", "Admin@Test.ma")
    monkeypatch.setenv("ADMIN_PASSWORD", "S3cret!")
    monkeypatch.setattr(auth, "get_user_by_email", lambda *a, **k: None)
    ok = auth.login_user("admin@test.ma ", "S3cret!")
    assert ok["ok"] is True and ok["user"]["role"] == "admin"
    assert auth.login_user("admin@test.ma", "mauvais")["ok"] is False
