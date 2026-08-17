from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from app.services.pdf_service import get_pdf_info


class PdfInfoPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.details = QLabel("Select a PDF to inspect its metadata.")
        button = QPushButton("Select PDF")
        button.setProperty("primary", True)
        button.clicked.connect(self.inspect)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("PDF Information")
        title.setObjectName("page-title")
        layout.addWidget(title)
        layout.addWidget(button)
        layout.addWidget(self.details)
        layout.addStretch()

    def inspect(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(self, "Select PDF", filter="PDF files (*.pdf)")
        if not file_name:
            return
        try:
            info = get_pdf_info(Path(file_name))
        except (OSError, ValueError) as error:
            QMessageBox.warning(self, "Unable to inspect PDF", str(error))
        else:
            self.details.setText(
                f"Pages: {info.page_count}\n"
                f"Encrypted: {info.encrypted}\n"
                f"Title: {info.title or '-'}\n"
                f"Author: {info.author or '-'}"
            )
