from pathlib import Path

import fitz
import pytest

from app.services.compress_service import (
    CompressionResult,
    GhostscriptNotFoundError,
    build_command,
    compress_pdf,
)


def test_compression_result() -> None:
    result = CompressionResult(Path("test.pdf"), 1000, 400)
    assert result.reduction_percent == 60.0


def test_build_command() -> None:
    command = build_command("gs", Path("in.pdf"), Path("out.pdf"), "Medium")
    assert "-dPDFSETTINGS=/ebook" in command


def test_compress_pdf_handles_missing_ghostscript(tmp_path: Path) -> None:
    source = tmp_path / "source.pdf"
    with fitz.open() as document:
        document.new_page()
        document.save(source)
    with pytest.raises(GhostscriptNotFoundError):
        compress_pdf(source, tmp_path / "out.pdf", "Medium")
