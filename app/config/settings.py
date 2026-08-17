from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

APP_INFO = {
    "name": "PDF SafeTools",
    "version": "0.1.0",
    "developer": "Yahya",
    "github_profile": "https://github.com/yahya06",
    "repository": "https://github.com/yahya06/pdf-safetools",
    "institution": "RSUD Bantarangin Ponorogo",
    "location": "Ponorogo, Jawa Timur, Indonesia",
}

APP_DATA_DIR = Path.home() / "AppData" / "Local" / "PDFSafeTools"
LOG_DIR = APP_DATA_DIR / "logs"
TEMP_DIR = APP_DATA_DIR / "temp"


def ensure_temp_dir() -> Path:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    return TEMP_DIR


@contextmanager
def temporary_directory() -> Iterator[Path]:
    with TemporaryDirectory(prefix="job-", dir=ensure_temp_dir()) as directory:
        yield Path(directory)


def cleanup_temp_dir() -> None:
    if TEMP_DIR.exists():
        for path in TEMP_DIR.iterdir():
            if path.is_dir():
                import shutil

                shutil.rmtree(path)
            else:
                path.unlink()
