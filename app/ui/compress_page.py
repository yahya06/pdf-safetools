from pathlib import Path

from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.compress_service import (
    PRESETS,
    CompressionError,
    GhostscriptNotFoundError,
    compress_pdf,
)


class CompressPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.preset = QComboBox()
        self.preset.addItems(list(PRESETS))
        self.result = QLabel("Select a PDF to compress.")
        button = QPushButton("Select PDF and compress")
        button.setProperty("primary", True)
        button.clicked.connect(self.compress)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Compress PDF")
        title.setObjectName("page-title")
        layout.addWidget(title)
        layout.addWidget(QLabel("Quality preset"))
        layout.addWidget(self.preset)
        layout.addWidget(button)
        layout.addWidget(self.result)
        layout.addStretch()

    def compress(self) -> None:
        source_name, _ = QFileDialog.getOpenFileName(self, "Select PDF", filter="PDF files (*.pdf)")
        if not source_name:
            return
        source = Path(source_name)
        output, _ = QFileDialog.getSaveFileName(
            self,
            "Save compressed PDF",
            str(source.with_stem(f"{source.stem}_compressed")),
            "PDF files (*.pdf)",
        )
        if not output:
            return
        try:
            result = compress_pdf(source, Path(output), self.preset.currentText())
        except (
            CompressionError,
            GhostscriptNotFoundError,
            FileExistsError,
            OSError,
            ValueError,
        ) as error:
            QMessageBox.warning(self, "Compression failed", str(error))
        else:
            self.result.setText(
                f"Original: {result.original_size:,} bytes\n"
                f"Output: {result.output_size:,} bytes\n"
                f"Reduction: {result.reduction_percent:.1f}%"
            )
