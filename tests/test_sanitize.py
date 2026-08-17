from pathlib import Path

import fitz
import pikepdf

from app.services.sanitize_service import sanitize_pdf
from app.services.scan_service import scan_pdf


def test_sanitize_removes_javascript_without_overwriting_source(tmp_path: Path) -> None:
    source = tmp_path / "source.pdf"
    prepared = tmp_path / "prepared.pdf"
    output = tmp_path / "output.pdf"
    with fitz.open() as document:
        document.new_page()
        document.save(source)
    with pikepdf.Pdf.open(source) as pdf:
        js_action = pikepdf.Dictionary(S=pikepdf.Name("/JavaScript"), JS="ignored")
        annotation = pikepdf.Dictionary(
            Type=pikepdf.Name("/Annot"),
            Subtype=pikepdf.Name("/Link"),
            Rect=[0, 0, 100, 100],
            A=js_action,
        )
        pdf.pages[0].Annots = pdf.make_indirect([annotation])
        pdf.save(prepared)
    source.unlink()
    prepared.replace(source)
    assert any(item.type == "javascript" for item in scan_pdf(source).findings)
    result = sanitize_pdf(source, output, "JKN Safe Mode")
    assert result.is_safe
    assert output.exists()
    assert not scan_pdf(output).findings
