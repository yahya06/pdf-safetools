from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.pdf_service import merge_pdfs


class MergePage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.files = QListWidget()
        add_button = QPushButton("Add PDFs")
        remove_button = QPushButton("Remove selected")
        merge_button = QPushButton("Merge")
        merge_button.setProperty("primary", True)
        add_button.clicked.connect(self.add_files)
        remove_button.clicked.connect(self.files.takeItem)
        merge_button.clicked.connect(self.merge)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Merge PDFs")
        title.setObjectName("page-title")
        layout.addWidget(title)
        layout.addWidget(self.files)
        actions = QHBoxLayout()
        actions.addWidget(add_button)
        actions.addWidget(remove_button)
        actions.addWidget(merge_button)
        layout.addLayout(actions)

    def add_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDFs", filter="PDF files (*.pdf)")
        self.files.addItems(files)

    def merge(self) -> None:
        output, _ = QFileDialog.getSaveFileName(
            self, "Save merged PDF", "merged.pdf", "PDF files (*.pdf)"
        )
        if not output:
            return
        try:
            merge_pdfs(
                [Path(self.files.item(index).text()) for index in range(self.files.count())],
                Path(output),
            )
        except (FileExistsError, OSError, ValueError) as error:
            QMessageBox.warning(self, "Merge failed", str(error))
        else:
            QMessageBox.information(self, "Merge complete", f"Saved to {output}")
