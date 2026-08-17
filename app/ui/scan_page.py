from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.services.scan_service import scan_pdf
from app.ui.file_drop import PdfDropLabel


class ScanPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.drop_label = PdfDropLabel()
        self.drop_label.files_dropped.connect(self.scan_paths)
        button = QPushButton("Select PDF and scan")
        button.setProperty("primary", True)
        button.clicked.connect(self.scan)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Scan PDF")
        title.setObjectName("page-title")
        layout.addWidget(title)
        layout.addWidget(QLabel("Static security analysis — does not execute actions"))
        layout.addWidget(self.drop_label)
        layout.addWidget(button)
        layout.addWidget(self.result)

    def scan(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(self, "Select PDF", filter="PDF files (*.pdf)")
        if not file_name:
            return
        try:
            scan_result = scan_pdf(Path(file_name))
        except (OSError, ValueError) as error:
            QMessageBox.warning(self, "Scan failed", str(error))
            return
        lines = [
            f"Risk level: {scan_result.risk_level}",
            f"Status: {scan_result.status}",
            f"SHA-256: {scan_result.sha256}",
            "",
        ]
        if scan_result.findings:
            lines.append("Findings:")
            for finding in scan_result.findings:
                lines.append(
                    f"  {finding.type}: {finding.severity} "
                    f"({finding.count}) — {finding.description}"
                )
        self.result.setText("\n".join(lines))

    def scan_paths(self, files: list[Path]) -> None:
        if not files:
            return
        file_name = str(files[0])
        try:
            scan_result = scan_pdf(Path(file_name))
        except (OSError, ValueError) as error:
            QMessageBox.warning(self, "Scan failed", str(error))
            return
        lines = [
            f"Risk level: {scan_result.risk_level}",
            f"Status: {scan_result.status}",
            f"SHA-256: {scan_result.sha256}",
            "",
        ]
        if scan_result.findings:
            lines.append("Findings:")
            for finding in scan_result.findings:
                lines.append(
                    f"  {finding.type}: {finding.severity} "
                    f"({finding.count}) — {finding.description}"
                )
        self.result.setText("\n".join(lines))
