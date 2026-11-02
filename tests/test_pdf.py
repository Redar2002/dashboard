import os

import utils_pdf


def test_create_pdf_returns_pdf_bytes(monkeypatch):
    monkeypatch.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data = utils_pdf.create_pdf("# Titre\n\n- **Point** important\n- Accents : éàç €", title="TEST")
    assert bytes(data[:4]) == b"%PDF"
