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


def test_metadata_cleaning_is_opt_in(tmp_path: Path) -> None:
    source = tmp_path / "source.pdf"
    default_output = tmp_path / "default.pdf"
    clean_output = tmp_path / "clean.pdf"
    with fitz.open() as document:
        document.new_page()
        document.set_metadata({"author": "Synthetic Author", "title": "Synthetic Title"})
        document.save(source)
    sanitize_pdf(source, default_output, preset="Custom", rules=set())
    sanitize_pdf(source, clean_output, preset="Custom", rules={"metadata"})
    with pikepdf.Pdf.open(default_output) as pdf:
        assert str(pdf.docinfo["/Author"]) == "Synthetic Author"
    with pikepdf.Pdf.open(clean_output) as pdf:
        assert "/Author" not in pdf.docinfo
        assert "/Title" not in pdf.docinfo


def test_jkn_safe_mode_cleans_metadata(tmp_path: Path) -> None:
    source = tmp_path / "source.pdf"
    output = tmp_path / "output.pdf"
    with fitz.open() as document:
        document.new_page()
        document.set_metadata({"author": "Synthetic Author"})
        document.save(source)
    sanitize_pdf(source, output, preset="JKN Safe Mode")
    with pikepdf.Pdf.open(output) as pdf:
        assert "/Author" not in pdf.docinfo
