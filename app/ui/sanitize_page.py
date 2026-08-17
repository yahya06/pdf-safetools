from pathlib import Path

from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.services.sanitize_service import sanitize_pdf


class SanitizePage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.preset = QComboBox()
        self.preset.addItems(["Standard", "JKN Safe Mode"])
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        button = QPushButton("Select PDF and sanitize")
        button.setProperty("primary", True)
        button.clicked.connect(self.sanitize)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Sanitize PDF")
        title.setObjectName("page-title")
        layout.addWidget(title)
        layout.addWidget(QLabel("Preset"))
        layout.addWidget(self.preset)
        layout.addWidget(button)
        layout.addWidget(self.result)

    def sanitize(self) -> None:
        source_name, _ = QFileDialog.getOpenFileName(
            self, "Select PDF", filter="PDF files (*.pdf)"
        )
        if not source_name:
            return
        source = Path(source_name)
        output, _ = QFileDialog.getSaveFileName(
            self,
            "Save sanitized PDF",
            str(source.with_stem(f"{source.stem}_clean")),
            "PDF files (*.pdf)",
        )
        if not output:
            return
        try:
            preset_text = self.preset.currentText()
            res = sanitize_pdf(source, Path(output), preset=preset_text)  # type: ignore[arg-type]
        except (FileExistsError, OSError, ValueError) as error:
            QMessageBox.warning(self, "Sanitize failed", str(error))
            return
        lines = [
            f"Output: {res.output}",
            f"Original SHA-256: {res.original_sha256}",
            f"Output SHA-256: {res.output_sha256}",
            f"Safe: {res.is_safe}",
            "",
        ]
        if res.removed:
            lines.append("Removed:")
            for rule, count in res.removed.items():
                lines.append(f"  {rule}: {count}")
            lines.append("")
        lines.append("Re-scan results:")
        lines.append(f"  Risk level: {res.scan.risk_level}")
        lines.append(f"  Status: {res.scan.status}")
        if res.scan.findings:
            lines.append("  Remaining findings:")
            for finding in res.scan.findings:
                lines.append(
                    f"    {finding.type}: {finding.severity} "
                    f"({finding.count}) — {finding.description}"
                )
        self.result.setText("\n".join(lines))
