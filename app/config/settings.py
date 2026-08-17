from pathlib import Path

APP_INFO = {
    "name": "PDF SafeTools",
    "version": "0.1.0",
    "developer": "Yahya",
    "github_profile": "https://github.com/yahya06",
    "repository": None,
    "institution": "RSUD Bantarangin Ponorogo",
    "location": "Ponorogo, Jawa Timur, Indonesia",
}

APP_DATA_DIR = Path.home() / "AppData" / "Local" / "PDFSafeTools"
LOG_DIR = APP_DATA_DIR / "logs"
TEMP_DIR = APP_DATA_DIR / "temp"
