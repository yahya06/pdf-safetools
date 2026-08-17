from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from app.services.pdf_service import split_pdf


class SplitPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        button = QPushButton("Select PDF and split all pages")
        button.setProperty("primary", True)
        button.clicked.connect(self.split)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Split PDF")
        title.setObjectName("page-title")
        description = QLabel("Pisahkan setiap halaman PDF menjadi berkas terpisah.")
        description.setObjectName("page-desc")
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(button)
        layout.addStretch()

    def split(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(self, "Select PDF", filter="PDF files (*.pdf)")
        if not file_name:
            return
        directory = QFileDialog.getExistingDirectory(self, "Select output folder")
        if not directory:
            return
        try:
            outputs = split_pdf(Path(file_name), Path(directory))
        except (FileExistsError, OSError, ValueError) as error:
            QMessageBox.warning(self, "Split failed", str(error))
        else:
            QMessageBox.information(self, "Split complete", f"Created {len(outputs)} PDF files.")
