import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from app.services.pdf_service import _ensure_new_output, validate_pdf

PRESETS = {
    "Low": "/screen",
    "Medium": "/ebook",
    "High": "/printer",
}


class GhostscriptNotFoundError(RuntimeError):
    pass


class CompressionError(RuntimeError):
    pass


@dataclass(frozen=True)
class CompressionResult:
    output: Path
    original_size: int
    output_size: int

    @property
    def reduction_percent(self) -> float:
        if self.original_size == 0:
            return 0.0
        return (1 - self.output_size / self.original_size) * 100


def find_ghostscript() -> str:
    executable = next(
        (shutil.which(name) for name in ("gswin64c", "gswin32c", "gs") if shutil.which(name)),
        None,
    )
    if executable is None:
        raise GhostscriptNotFoundError("Ghostscript is not installed or not available on PATH.")
    return executable


def build_command(executable: str, source: Path, output: Path, preset: str) -> list[str]:
    try:
        quality = PRESETS[preset]
    except KeyError as error:
        raise ValueError(f"Unknown compression preset: {preset}") from error
    return [
        executable,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={quality}",
        "-dNOPAUSE",
        "-dBATCH",
        "-dSAFER",
        f"-sOutputFile={output}",
        str(source),
    ]


def compress_pdf(source: Path, output: Path, preset: str) -> CompressionResult:
    validate_pdf(source)
    _ensure_new_output(output)
    executable = find_ghostscript()
    try:
        subprocess.run(
            build_command(executable, source, output, preset), check=True, capture_output=True
        )
    except subprocess.CalledProcessError as error:
        if output.exists():
            output.unlink()
        raise CompressionError("Ghostscript could not compress this PDF.") from error
    if not output.is_file():
        raise CompressionError("Ghostscript did not create an output PDF.")
    return CompressionResult(output, source.stat().st_size, output.stat().st_size)
