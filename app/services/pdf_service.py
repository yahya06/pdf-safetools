from dataclasses import dataclass
from pathlib import Path

import pikepdf


class PdfValidationError(ValueError):
    pass


@dataclass(frozen=True)
class PdfInfo:
    path: Path
    page_count: int
    encrypted: bool
    title: str | None
    author: str | None


def validate_pdf(path: Path) -> None:
    if path.suffix.lower() != ".pdf":
        raise PdfValidationError("File must use the .pdf extension.")
    try:
        if path.read_bytes()[:5] != b"%PDF-":
            raise PdfValidationError("File does not have a PDF signature.")
        with pikepdf.Pdf.open(path):
            pass
    except pikepdf.PdfError as error:
        raise PdfValidationError("File is not a valid PDF.") from error


def get_pdf_info(path: Path) -> PdfInfo:
    validate_pdf(path)
    with pikepdf.Pdf.open(path) as pdf:
        metadata = pdf.docinfo
        return PdfInfo(
            path=path,
            page_count=len(pdf.pages),
            encrypted=pdf.is_encrypted,
            title=str(metadata.get("/Title")) if metadata.get("/Title") else None,
            author=str(metadata.get("/Author")) if metadata.get("/Author") else None,
        )


def merge_pdfs(inputs: list[Path], output: Path) -> None:
    if len(inputs) < 2:
        raise ValueError("Select at least two PDFs to merge.")
    for path in inputs:
        validate_pdf(path)
    _ensure_new_output(output)
    with pikepdf.Pdf.new() as merged:
        for path in inputs:
            with pikepdf.Pdf.open(path) as source:
                merged.pages.extend(source.pages)
        merged.save(output)


def split_pdf(path: Path, output_dir: Path) -> list[Path]:
    validate_pdf(path)
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    with pikepdf.Pdf.open(path) as source:
        for index, page in enumerate(source.pages, start=1):
            output = output_dir / f"{path.stem}_{index:03d}.pdf"
            _ensure_new_output(output)
            with pikepdf.Pdf.new() as document:
                document.pages.append(page)
                document.save(output)
            outputs.append(output)
    return outputs


def transform_pages(
    path: Path, output: Path, page_order: list[int], rotations: dict[int, int]
) -> None:
    validate_pdf(path)
    _ensure_new_output(output)
    with pikepdf.Pdf.open(path) as source, pikepdf.Pdf.new() as transformed:
        count = len(source.pages)
        if not page_order or len(set(page_order)) != len(page_order):
            raise ValueError("Page order must contain unique pages.")
        if any(index < 0 or index >= count for index in page_order):
            raise ValueError("Page order contains an invalid page index.")
        for index in page_order:
            page = source.pages[index]
            rotation = rotations.get(index, 0)
            if rotation not in {0, 90, 180, 270}:
                raise ValueError("Rotation must be 0, 90, 180, or 270 degrees.")
            if rotation:
                page.Rotate = (int(page.Rotate) if page.Rotate else 0) + rotation
            transformed.pages.append(page)
        transformed.save(output)


def _ensure_new_output(path: Path) -> None:
    if path.exists():
        raise FileExistsError(f"Output already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
