from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from app.services.render_service import images_to_pdf, pdf_to_images


class ConvertPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        pdf_button = QPushButton("PDF to images")
        pdf_button.setProperty("primary", True)
        images_button = QPushButton("Images to PDF")
        pdf_button.clicked.connect(self.convert_pdf)
        images_button.clicked.connect(self.convert_images)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Convert PDF and images")
        title.setObjectName("page-title")
        layout.addWidget(title)
        layout.addWidget(pdf_button)
        layout.addWidget(images_button)
        layout.addStretch()

    def convert_pdf(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(self, "Select PDF", filter="PDF files (*.pdf)")
        if not file_name:
            return
        directory = QFileDialog.getExistingDirectory(self, "Select output folder")
        if not directory:
            return
        try:
            outputs = pdf_to_images(Path(file_name), Path(directory))
        except (FileExistsError, OSError, ValueError) as error:
            QMessageBox.warning(self, "Conversion failed", str(error))
        else:
            QMessageBox.information(self, "Conversion complete", f"Created {len(outputs)} images.")

    def convert_images(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select images", filter="Image files (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        if not files:
            return
        output, _ = QFileDialog.getSaveFileName(self, "Save PDF", "images.pdf", "PDF files (*.pdf)")
        if not output:
            return
        try:
            images_to_pdf([Path(file_name) for file_name in files], Path(output))
        except (FileExistsError, OSError, ValueError) as error:
            QMessageBox.warning(self, "Conversion failed", str(error))
        else:
            QMessageBox.information(self, "Conversion complete", f"Saved to {output}")
