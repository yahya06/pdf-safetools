from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.services.compress_service import compress_pdf
from app.services.sanitize_service import sanitize_pdf
from app.services.scan_service import scan_pdf


class BatchPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        scan_button = QPushButton("Batch scan folder")
        sanitize_button = QPushButton("Batch sanitize folder")
        compress_button = QPushButton("Batch compress folder")
        scan_button.clicked.connect(self.batch_scan)
        sanitize_button.clicked.connect(self.batch_sanitize)
        compress_button.clicked.connect(self.batch_compress)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Batch Processing")
        title.setObjectName("page-title")
        layout.addWidget(title)
        layout.addWidget(scan_button)
        layout.addWidget(sanitize_button)
        layout.addWidget(compress_button)
        layout.addWidget(self.result)

    def batch_scan(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select folder")
        if not folder:
            return
        pdf_files = list(Path(folder).glob("*.pdf"))
        lines = [f"Scanning {len(pdf_files)} PDFs...", ""]
        for pdf_file in pdf_files:
            try:
                result = scan_pdf(pdf_file)
                lines.append(f"{pdf_file.name}: {result.risk_level}")
            except Exception as error:
                lines.append(f"{pdf_file.name}: ERROR — {error}")
        self.result.setText("\n".join(lines))

    def batch_sanitize(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select folder")
        if not folder:
            return
        output_folder = Path(folder) / "sanitized"
        output_folder.mkdir(exist_ok=True)
        pdf_files = list(Path(folder).glob("*.pdf"))
        lines = [f"Sanitizing {len(pdf_files)} PDFs to {output_folder}...", ""]
        for pdf_file in pdf_files:
            output = output_folder / f"{pdf_file.stem}_clean.pdf"
            try:
                result = sanitize_pdf(pdf_file, output, preset="JKN Safe Mode")
                removed_count = sum(result.removed.values())
                lines.append(f"{pdf_file.name}: {result.scan.risk_level} (removed {removed_count})")
            except Exception as error:
                lines.append(f"{pdf_file.name}: ERROR — {error}")
        self.result.setText("\n".join(lines))

    def batch_compress(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select folder")
        if not folder:
            return
        output_folder = Path(folder) / "compressed"
        output_folder.mkdir(exist_ok=True)
        pdf_files = list(Path(folder).glob("*.pdf"))
        lines = [f"Compressing {len(pdf_files)} PDFs to {output_folder}...", ""]
        for pdf_file in pdf_files:
            output = output_folder / f"{pdf_file.stem}_compressed.pdf"
            try:
                result = compress_pdf(pdf_file, output, "Medium")
                lines.append(f"{pdf_file.name}: {result.reduction_percent:.1f}% reduction")
            except Exception as error:
                lines.append(f"{pdf_file.name}: ERROR — {error}")
        self.result.setText("\n".join(lines))
