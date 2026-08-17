from pathlib import Path

import fitz

from app.services.pdf_service import _ensure_new_output, validate_pdf


def pdf_to_images(path: Path, output_dir: Path) -> list[Path]:
    validate_pdf(path)
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    with fitz.open(path) as document:
        for index, page in enumerate(document, start=1):
            output = output_dir / f"{path.stem}_{index:03d}.png"
            _ensure_new_output(output)
            page.get_pixmap().save(output)
            outputs.append(output)
    return outputs


def images_to_pdf(images: list[Path], output: Path) -> None:
    if not images:
        raise ValueError("Select at least one image.")
    _ensure_new_output(output)
    with fitz.open() as document:
        for image in images:
            if not image.is_file():
                raise FileNotFoundError(image)
            with fitz.open(image) as source:
                pdf_bytes = source.convert_to_pdf()
                with fitz.open("pdf", pdf_bytes) as source_pdf:
                    document.insert_pdf(source_pdf)
        document.save(output)
