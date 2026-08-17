from pathlib import Path

import fitz

from app.services.scan_service import scan_pdf


def test_scan_safe_pdf_uses_configured_safe_wording(tmp_path: Path) -> None:
    path = tmp_path / "safe.pdf"
    with fitz.open() as document:
        document.new_page()
        document.save(path)
    result = scan_pdf(path)
    assert result.risk_level == "SAFE"
    assert result.status == "No configured findings detected"
    assert not result.findings
