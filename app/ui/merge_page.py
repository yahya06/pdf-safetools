import tempfile
from pathlib import Path

import fitz
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QImage, QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListView,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.pdf_service import get_pdf_info, merge_pdfs, transform_pages
from app.ui.file_drop import PdfDropLabel


class MergePage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.files = QListWidget()
        self.drop_label = PdfDropLabel()
        self.drop_label.files_dropped.connect(self.add_paths)
        self.previews = QListWidget()
        self.previews.setViewMode(QListView.ViewMode.IconMode)
        self.previews.setIconSize(QPixmap(120, 160).size())
        self.previews.setResizeMode(QListView.ResizeMode.Adjust)
        self.previews.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        self.previews.setWordWrap(True)
        add_button = QPushButton("Add PDFs")
        up_button = QPushButton("↑")
        down_button = QPushButton("↓")
        remove_button = QPushButton("✕")
        rotate_button = QPushButton("↻")
        clear_button = QPushButton("Clear All")
        merge_button = QPushButton("Merge")
        rotate_button.setToolTip("Rotate selected PDF 90° clockwise")
        up_button.setToolTip("Move selected PDF up")
        down_button.setToolTip("Move selected PDF down")
        remove_button.setToolTip("Remove selected PDF")
        clear_button.setToolTip("Remove all PDFs")
        merge_button.setProperty("primary", True)
        add_button.clicked.connect(self.add_files)
        up_button.clicked.connect(self.move_up)
        down_button.clicked.connect(self.move_down)
        remove_button.clicked.connect(self.remove_selected)
        rotate_button.clicked.connect(self.rotate_selected)
        clear_button.clicked.connect(self.clear_all)
        merge_button.clicked.connect(self.merge)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Merge PDFs")
        title.setObjectName("page-title")
        layout.addWidget(title)
        layout.addWidget(QLabel("PDF order"))
        layout.addWidget(self.drop_label)
        layout.addWidget(self.files)
        actions = QHBoxLayout()
        actions.addWidget(add_button)
        actions.addWidget(up_button)
        actions.addWidget(down_button)
        actions.addWidget(rotate_button)
        actions.addWidget(remove_button)
        actions.addWidget(clear_button)
        actions.addWidget(merge_button)
        layout.addLayout(actions)
        layout.addWidget(QLabel("Merge preview"))
        layout.addWidget(self.previews)

    def add_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDFs", filter="PDF files (*.pdf)")
        self.add_paths([Path(file_name) for file_name in files])

    def add_paths(self, paths: list[Path]) -> None:
        for path in paths:
            try:
                preview = self._preview(path)
            except (fitz.FileDataError, OSError, ValueError) as error:
                QMessageBox.warning(self, "Preview failed", str(error))
                continue
            item = QListWidgetItem(path.name)
            item.setData(Qt.ItemDataRole.UserRole, path)
            item.setData(Qt.ItemDataRole.UserRole + 1, preview)
            item.setData(Qt.ItemDataRole.UserRole + 2, 0)  # Rotation degrees
            item.setToolTip(str(path))
            self.files.addItem(item)
        self.update_previews()

    def move_up(self) -> None:
        row = self.files.currentRow()
        if row <= 0:
            return
        self.files.insertItem(row - 1, self.files.takeItem(row))
        self.files.setCurrentRow(row - 1)
        self.update_previews()

    def move_down(self) -> None:
        row = self.files.currentRow()
        if row < 0 or row >= self.files.count() - 1:
            return
        self.files.insertItem(row + 1, self.files.takeItem(row))
        self.files.setCurrentRow(row + 1)
        self.update_previews()

    def remove_selected(self) -> None:
        row = self.files.currentRow()
        if row >= 0:
            self.files.takeItem(row)
            self.update_previews()

    def rotate_selected(self) -> None:
        row = self.files.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No PDF selected", "Select a PDF first.")
            return
        item = self.files.item(row)
        current_rotation = item.data(Qt.ItemDataRole.UserRole + 2) or 0
        new_rotation = (current_rotation + 90) % 360
        item.setData(Qt.ItemDataRole.UserRole + 2, new_rotation)
        self.update_previews()

    def clear_all(self) -> None:
        self.files.clear()
        self.previews.clear()

    def update_previews(self) -> None:
        self.previews.clear()
        for index in range(self.files.count()):
            source = self.files.item(index)
            preview = source.data(Qt.ItemDataRole.UserRole + 1)
            rotation = source.data(Qt.ItemDataRole.UserRole + 2) or 0

            # Apply rotation to preview QPixmap
            if rotation:
                from PySide6.QtGui import QTransform

                transform = QTransform().rotate(rotation)
                preview = preview.transformed(transform)

            item = QListWidgetItem(QIcon(preview), f"{index + 1}. {source.text()}")
            item.setToolTip(source.toolTip())
            self.previews.addItem(item)

    def merge(self) -> None:
        output_name, _ = QFileDialog.getSaveFileName(
            self, "Save merged PDF", "merged.pdf", "PDF files (*.pdf)"
        )
        if not output_name:
            return
        output = Path(output_name)
        if output.exists():
            stem, suffix = output.stem, output.suffix
            counter = 1
            while output.exists():
                output = output.with_name(f"{stem}({counter}){suffix}")
                counter += 1
        try:
            with tempfile.TemporaryDirectory() as directory:
                inputs: list[Path] = []
                for index in range(self.files.count()):
                    item = self.files.item(index)
                    source = item.data(Qt.ItemDataRole.UserRole)
                    rotation = item.data(Qt.ItemDataRole.UserRole + 2) or 0
                    if rotation:
                        rotated = Path(directory) / f"rotated_{index}.pdf"
                        page_count = get_pdf_info(source).page_count
                        transform_pages(
                            source,
                            rotated,
                            list(range(page_count)),
                            {page: rotation for page in range(page_count)},
                        )
                        inputs.append(rotated)
                    else:
                        inputs.append(source)
                merge_pdfs(inputs, output)
        except (FileExistsError, OSError, ValueError) as error:
            QMessageBox.warning(self, "Merge failed", str(error))
        else:
            QMessageBox.information(self, "Merge complete", f"Saved to {output}")

    @staticmethod
    def _preview(path: Path) -> QPixmap:
        with fitz.open(path) as document:
            page = document[0]
            pixmap = page.get_pixmap(matrix=fitz.Matrix(0.25, 0.25), alpha=False)
        image = QImage(
            pixmap.samples,
            pixmap.width,
            pixmap.height,
            pixmap.stride,
            QImage.Format.Format_RGB888,
        ).copy()
        return QPixmap.fromImage(image).scaled(
            120,
            160,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
