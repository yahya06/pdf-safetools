from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.services.pdf_service import get_pdf_info, transform_pages


class OrganizePage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.path: Path | None = None
        self.info = QLabel("Select a PDF to organize.")
        self.page = QSpinBox()
        self.page.setMinimum(1)
        self.page.setEnabled(False)
        choose_button = QPushButton("Select PDF")
        choose_button.setProperty("primary", True)
        rotate_button = QPushButton("Rotate selected page 90°")
        delete_button = QPushButton("Delete selected page")
        choose_button.clicked.connect(self.select_pdf)
        rotate_button.clicked.connect(lambda: self.save_transform(rotate=True))
        delete_button.clicked.connect(lambda: self.save_transform(rotate=False))
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Organize PDF")
        title.setObjectName("page-title")
        layout.addWidget(title)
        layout.addWidget(choose_button)
        layout.addWidget(self.info)
        controls = QHBoxLayout()
        controls.addWidget(QLabel("Page"))
        controls.addWidget(self.page)
        layout.addLayout(controls)
        layout.addWidget(rotate_button)
        layout.addWidget(delete_button)
        layout.addStretch()

    def select_pdf(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(self, "Select PDF", filter="PDF files (*.pdf)")
        if not file_name:
            return
        try:
            info = get_pdf_info(Path(file_name))
        except (OSError, ValueError) as error:
            QMessageBox.warning(self, "Unable to open PDF", str(error))
            return
        self.path = info.path
        self.page.setMaximum(info.page_count)
        self.page.setValue(1)
        self.page.setEnabled(True)
        self.info.setText(f"{info.path.name}: {info.page_count} pages")

    def save_transform(self, *, rotate: bool) -> None:
        if self.path is None:
            QMessageBox.warning(self, "No PDF selected", "Select a PDF first.")
            return
        output, _ = QFileDialog.getSaveFileName(self, "Save PDF", filter="PDF files (*.pdf)")
        if not output:
            return
        page_index = self.page.value() - 1
        try:
            count = get_pdf_info(self.path).page_count
            page_order = list(range(count))
            rotations = {page_index: 90} if rotate else {}
            if not rotate:
                page_order.remove(page_index)
                if not page_order:
                    raise ValueError("A PDF must retain at least one page.")
            transform_pages(self.path, Path(output), page_order, rotations)
        except (FileExistsError, OSError, ValueError) as error:
            QMessageBox.warning(self, "Unable to save PDF", str(error))
        else:
            QMessageBox.information(self, "PDF saved", f"Saved to {output}")
