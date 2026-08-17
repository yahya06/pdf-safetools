from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QLabel


class PdfDropLabel(QLabel):
    files_dropped = Signal(list)

    def __init__(self, text: str = "Drop PDF files here") -> None:
        super().__init__(text)
        self.setAcceptDrops(True)
        self.setMinimumHeight(36)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        paths = [Path(url.toLocalFile()) for url in event.mimeData().urls() if url.isLocalFile()]
        files = [path for path in paths if path.suffix.lower() == ".pdf"]
        if files:
            self.files_dropped.emit(files)
            event.acceptProposedAction()
