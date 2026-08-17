from pathlib import Path

import fitz
import pikepdf

from app.services.sanitize_service import sanitize_pdf
from app.services.scan_service import scan_pdf


def _write_pdf(path: Path) -> None:
    with fitz.open() as document:
        document.new_page()
        document.save(path)


def _add_actions(path: Path) -> None:
    with pikepdf.Pdf.open(path) as pdf:
        root_action = pikepdf.Dictionary(S=pikepdf.Name("/JavaScript"), JS="ignored")
        pdf.Root.OpenAction = root_action
        pdf.Root.AA = pikepdf.Dictionary(O=pikepdf.Dictionary(S=pikepdf.Name("/Launch")))
        pdf.Root.Names = pikepdf.Dictionary(
            JavaScript=pikepdf.Dictionary(Names=[]), EmbeddedFiles=pikepdf.Dictionary(Names=[])
        )
        annotations = []
        for action_type in ("/URI", "/GoToR", "/GoToE", "/SubmitForm", "/ImportData"):
            annotations.append(
                pikepdf.Dictionary(
                    Type=pikepdf.Name("/Annot"),
                    Subtype=pikepdf.Name("/Link"),
                    Rect=[0, 0, 10, 10],
                    A=pikepdf.Dictionary(S=pikepdf.Name(action_type)),
                )
            )
        for subtype in ("/RichMedia", "/Movie", "/Sound", "/3D"):
            annotations.append(
                pikepdf.Dictionary(
                    Type=pikepdf.Name("/Annot"), Subtype=pikepdf.Name(subtype), Rect=[0, 0, 10, 10]
                )
            )
        pdf.pages[0].Annots = pdf.make_indirect(annotations)
        pdf.save(path.with_stem(f"{path.stem}_actions"))
    path.unlink()
    path.with_stem(f"{path.stem}_actions").replace(path)


def test_scan_detects_static_actions_and_configures_severity(tmp_path: Path) -> None:
    source = tmp_path / "actions.pdf"
    _write_pdf(source)
    _add_actions(source)
    result = scan_pdf(source, {"external_uri": "LOW"})
    types = {finding.type for finding in result.findings}
    assert {"javascript", "open_action", "additional_actions", "external_uri", "launch"} <= types
    assert {"goto_remote", "goto_embedded", "embedded_file", "submit_form", "import_data"} <= types
    assert {"rich_media", "movie", "sound", "3d", "external_annotation"} <= types
    assert next(item for item in result.findings if item.type == "external_uri").severity == "LOW"
    assert all(item.action == "REMOVE" for item in result.findings)


def test_jkn_sanitize_preserves_original_and_rescan_has_no_findings(tmp_path: Path) -> None:
    source = tmp_path / "source.pdf"
    output = tmp_path / "sanitized.pdf"
    _write_pdf(source)
    _add_actions(source)
    original = source.read_bytes()
    result = sanitize_pdf(source, output)
    assert source.read_bytes() == original
    assert result.original_sha256 != result.output_sha256
    assert result.is_safe
    assert result.scan.status == "No configured findings detected"
    assert not scan_pdf(output).findings


def test_custom_rules_only_remove_selected_action(tmp_path: Path) -> None:
    source = tmp_path / "custom.pdf"
    output = tmp_path / "custom_output.pdf"
    _write_pdf(source)
    _add_actions(source)
    sanitize_pdf(source, output, "Custom", {"external_annotation"})
    types = {finding.type for finding in scan_pdf(output).findings}
    assert "external_uri" not in types
    assert "javascript" in types
