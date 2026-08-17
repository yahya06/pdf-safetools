from pathlib import Path

import fitz
import pytest

from app.services.pdf_service import (
    PdfValidationError,
    get_pdf_info,
    merge_pdfs,
    split_pdf,
    transform_pages,
    validate_pdf,
)
from app.services.render_service import images_to_pdf, pdf_to_images


def _write_pdf(path: Path, page_count: int = 1) -> Path:
    with fitz.open() as document:
        for _ in range(page_count):
            document.new_page()
        document.save(path)
    return path


def test_validate_pdf_rejects_non_pdf(tmp_path: Path) -> None:
    path = tmp_path / "note.txt"
    path.write_text("not a pdf")
    with pytest.raises(PdfValidationError):
        validate_pdf(path)


def test_merge_split_and_delete(tmp_path: Path) -> None:
    first = _write_pdf(tmp_path / "first.pdf", 1)
    second = _write_pdf(tmp_path / "second.pdf", 2)
    merged = tmp_path / "merged.pdf"
    merge_pdfs([first, second], merged)
    assert get_pdf_info(merged).page_count == 3
    pages = split_pdf(merged, tmp_path / "pages")
    assert len(pages) == 3
    trimmed = tmp_path / "trimmed.pdf"
    transform_pages(merged, trimmed, [0, 2], {})
    assert get_pdf_info(trimmed).page_count == 2


def test_pdf_image_roundtrip(tmp_path: Path) -> None:
    source = _write_pdf(tmp_path / "source.pdf", 2)
    images = pdf_to_images(source, tmp_path / "images")
    output = tmp_path / "from_images.pdf"
    images_to_pdf(images, output)
    assert get_pdf_info(output).page_count == 2
