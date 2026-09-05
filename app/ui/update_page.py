import json
import urllib.error
import urllib.request

from PySide6.QtCore import QObject, Qt, QThread, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.config.settings import APP_INFO

_REPO = APP_INFO["repository"]
_API_URL = (
    _REPO.replace("https://github.com/", "https://api.github.com/repos/") + "/releases/latest"
)


def _parse_version(tag: str) -> tuple[int, ...]:
    return tuple(int(x) for x in tag.lstrip("v").split("."))


class _CheckSignals(QObject):
    finished = Signal(str, str, str)
    error = Signal(str)


class _CheckWorker(QObject):
    def __init__(self, signals: _CheckSignals) -> None:
        super().__init__()
        self.signals = signals

    def run(self) -> None:
        try:
            req = urllib.request.Request(
                _API_URL, headers={"Accept": "application/vnd.github+json"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
            tag = data.get("tag_name", "")
            url = data.get("html_url", "")
            body = data.get("body", "")
            self.signals.finished.emit(tag, url, body)
        except (urllib.error.URLError, OSError, json.JSONDecodeError, ValueError) as exc:
            self.signals.error.emit(str(exc))


class UpdatePage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._thread: QThread | None = None
        self._worker: _CheckWorker | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Update")
        title.setObjectName("page-title")
        layout.addWidget(title)

        self.version_label = QLabel(f"Current version: v{APP_INFO['version']}")
        self.version_label.setStyleSheet("font-size: 14px; margin-bottom: 8px;")
        layout.addWidget(self.version_label)

        self.check_button = QPushButton("Check for Updates")
        self.check_button.setProperty("primary", True)
        self.check_button.clicked.connect(self._check)
        layout.addWidget(self.check_button)

        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        self.status_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(self.status_label)

        self.release_notes = QLabel("")
        self.release_notes.setWordWrap(True)
        self.release_notes.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.release_notes)

        btn_row = QHBoxLayout()
        self.download_button = QPushButton("Download Update")
        self.download_button.setProperty("primary", True)
        self.download_button.setVisible(False)
        self.download_button.clicked.connect(self._open_release)
        btn_row.addWidget(self.download_button)

        self.repo_button = QPushButton("Open GitHub Repository")
        self.repo_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(_REPO)))
        btn_row.addWidget(self.repo_button)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        layout.addStretch()

        self._release_url = ""

    def _check(self) -> None:
        self.check_button.setEnabled(False)
        self.status_label.setText("Checking for updates...")
        self.download_button.setVisible(False)
        self.release_notes.setText("")

        signals = _CheckSignals()
        signals.finished.connect(self._on_result)
        signals.error.connect(self._on_error)

        worker = _CheckWorker(signals)
        thread = QThread()
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        thread.start()
        self._thread = thread
        self._worker = worker

    def _on_result(self, tag: str, url: str, body: str) -> None:
        self._cleanup_thread()
        self.check_button.setEnabled(True)
        if not tag:
            self.status_label.setText("No releases found on GitHub.")
            return

        self._release_url = url
        try:
            remote = _parse_version(tag)
            local = _parse_version(APP_INFO["version"])
            is_new = remote > local
        except ValueError:
            is_new = tag.lstrip("v") != APP_INFO["version"]

        if is_new:
            self.status_label.setText(f"<b>New version available: {tag}</b>")
            self.download_button.setVisible(True)
        else:
            self.status_label.setText("You are up to date.")

        if body:
            self.release_notes.setText(body[:500])

    def _on_error(self, message: str) -> None:
        self._cleanup_thread()
        self.check_button.setEnabled(True)
        self.status_label.setText(f"Unable to check for updates: {message}")

    def _open_release(self) -> None:
        if self._release_url:
            QDesktopServices.openUrl(QUrl(self._release_url))

    def _cleanup_thread(self) -> None:
        if self._thread is not None:
            self._thread.quit()
            self._thread.wait(3000)
            self._thread = None
            self._worker = None
