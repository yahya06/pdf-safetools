from pathlib import Path

from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.compress_service import (
    PRESETS,
    CompressionError,
    CompressionResult,
    GhostscriptNotFoundError,
    compress_pdf,
)
from app.ui.file_drop import PdfDropLabel


class CompressWorker(QObject):
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, source: Path, output: Path, preset: str) -> None:
        super().__init__()
        self.source = source
        self.output = output
        self.preset = preset

    @Slot()
    def run(self) -> None:
        try:
            self.finished.emit(compress_pdf(self.source, self.output, self.preset))
        except (
            CompressionError,
            GhostscriptNotFoundError,
            FileExistsError,
            OSError,
            ValueError,
        ) as error:
            self.error.emit(str(error))


class CompressPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.preset = QComboBox()
        self.preset.addItems(list(PRESETS))
        self.result = QLabel("Select a PDF to compress.")
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()
        self.drop_label = PdfDropLabel()
        self.drop_label.files_dropped.connect(self.compress_path)
        button = QPushButton("Select PDF and compress")
        button.setProperty("primary", True)
        button.clicked.connect(self.compress)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Compress PDF")
        title.setObjectName("page-title")
        layout.addWidget(title)
        layout.addWidget(self.drop_label)
        layout.addWidget(QLabel("Quality preset"))
        layout.addWidget(self.preset)
        layout.addWidget(button)
        layout.addWidget(self.progress)
        layout.addWidget(self.result)
        layout.addStretch()
        self._thread: QThread | None = None
        self._worker: CompressWorker | None = None

    def compress(self) -> None:
        source_name, _ = QFileDialog.getOpenFileName(self, "Select PDF", filter="PDF files (*.pdf)")
        if source_name:
            self.compress_path([Path(source_name)])

    def compress_path(self, files: list[Path]) -> None:
        source = files[0]
        output, _ = QFileDialog.getSaveFileName(
            self,
            "Save compressed PDF",
            str(source.with_stem(f"{source.stem}_compressed")),
            "PDF files (*.pdf)",
        )
        if not output:
            return
        self.progress.show()
        self._thread = QThread(self)
        self._worker = CompressWorker(source, Path(output), self.preset.currentText())
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self.compression_finished)
        self._worker.error.connect(self.compression_failed)
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    @Slot(object)
    def compression_finished(self, result: CompressionResult) -> None:
        self.progress.hide()
        self.result.setText(
            f"Original: {result.original_size:,} bytes\n"
            f"Output: {result.output_size:,} bytes\n"
            f"Reduction: {result.reduction_percent:.1f}%"
        )

    @Slot(str)
    def compression_failed(self, message: str) -> None:
        self.progress.hide()
        QMessageBox.warning(self, "Compression failed", message)
