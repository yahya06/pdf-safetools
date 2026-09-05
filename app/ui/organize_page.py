from pathlib import Path

import fitz
from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QIcon, QImage, QPixmap, QTransform
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

from app.services.pdf_service import get_pdf_info, transform_pages


class _ThumbnailSignals(QObject):
    ready = Signal(int, QPixmap)


class _ThumbnailWorker(QObject):
    def __init__(self, path: Path, page_count: int, signals: _ThumbnailSignals) -> None:
        super().__init__()
        self._path = path
        self._page_count = page_count
        self.signals = signals

    def run(self) -> None:
        with fitz.open(self._path) as doc:
            for i in range(self._page_count):
                page = doc[i]
                pix = page.get_pixmap(matrix=fitz.Matrix(0.25, 0.25), alpha=False)
                image = QImage(
                    pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888
                ).copy()
                thumb = QPixmap.fromImage(image).scaled(
                    120,
                    160,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self.signals.ready.emit(i, thumb)


class OrganizePage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.path: Path | None = None
        self._page_count = 0
        self._thread: object | None = None

        self.info = QLabel("Select a PDF to organize.")
        self.pages_list = QListWidget()
        self.pages_list.setViewMode(QListView.ViewMode.IconMode)
        self.pages_list.setIconSize(QPixmap(120, 160).size())
        self.pages_list.setResizeMode(QListView.ResizeMode.Adjust)
        self.pages_list.setWordWrap(True)
        self.pages_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        choose_button = QPushButton("Select PDF")
        choose_button.setProperty("primary", True)
        up_button = QPushButton("↑")
        down_button = QPushButton("↓")
        rotate_button = QPushButton("↻")
        delete_button = QPushButton("✕")
        save_button = QPushButton("Save")

        up_button.setToolTip("Move selected page up")
        down_button.setToolTip("Move selected page down")
        rotate_button.setToolTip("Rotate selected page 90° clockwise")
        delete_button.setToolTip("Delete selected page")
        save_button.setProperty("primary", True)

        choose_button.clicked.connect(self.select_pdf)
        up_button.clicked.connect(self.move_up)
        down_button.clicked.connect(self.move_down)
        rotate_button.clicked.connect(self.rotate_selected)
        delete_button.clicked.connect(self.delete_selected)
        save_button.clicked.connect(self.save)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Organize PDF")
        title.setObjectName("page-title")
        layout.addWidget(title)
        layout.addWidget(choose_button)
        layout.addWidget(self.info)
        layout.addWidget(self.pages_list, 1)

        actions = QHBoxLayout()
        actions.addWidget(up_button)
        actions.addWidget(down_button)
        actions.addWidget(rotate_button)
        actions.addWidget(delete_button)
        actions.addStretch()
        actions.addWidget(save_button)
        layout.addLayout(actions)

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
        self._page_count = info.page_count
        self.info.setText(f"{info.path.name}: {info.page_count} pages")
        self._load_thumbnails()

    def _load_thumbnails(self) -> None:
        self.pages_list.clear()
        if self.path is None:
            return

        for i in range(self._page_count):
            item = QListWidgetItem(f"Page {i + 1}")
            item.setData(Qt.ItemDataRole.UserRole, i)
            item.setData(Qt.ItemDataRole.UserRole + 1, QPixmap())
            item.setData(Qt.ItemDataRole.UserRole + 2, 0)
            self.pages_list.addItem(item)

        from PySide6.QtCore import QThread

        signals = _ThumbnailSignals()
        signals.ready.connect(self._on_thumbnail_ready)
        worker = _ThumbnailWorker(self.path, self._page_count, signals)
        thread = QThread()
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        signals.ready.connect(lambda _i, _p, t=thread: self._finish_thread_if_done(t))
        thread.start()
        self._thread = thread
        self._worker = worker

    def _finish_thread_if_done(self, thread: object) -> None:
        from PySide6.QtCore import QThread

        if not isinstance(thread, QThread):
            return
        loaded = sum(
            1
            for i in range(self.pages_list.count())
            if not self.pages_list.item(i).data(Qt.ItemDataRole.UserRole + 1).isNull()
        )
        if loaded >= self.pages_list.count():
            thread.quit()

    def _on_thumbnail_ready(self, page_index: int, pixmap: QPixmap) -> None:
        for i in range(self.pages_list.count()):
            item = self.pages_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == page_index:
                item.setData(Qt.ItemDataRole.UserRole + 1, pixmap)
                break
        self._refresh_icons()

    def _refresh_icons(self) -> None:
        for i in range(self.pages_list.count()):
            item = self.pages_list.item(i)
            pixmap = item.data(Qt.ItemDataRole.UserRole + 1)
            rotation = item.data(Qt.ItemDataRole.UserRole + 2) or 0
            if rotation and not pixmap.isNull():
                pixmap = pixmap.transformed(QTransform().rotate(rotation))
            item.setIcon(QIcon(pixmap))

    def move_up(self) -> None:
        row = self.pages_list.currentRow()
        if row <= 0:
            return
        self.pages_list.insertItem(row - 1, self.pages_list.takeItem(row))
        self.pages_list.setCurrentRow(row - 1)
        self._update_labels()

    def move_down(self) -> None:
        row = self.pages_list.currentRow()
        if row < 0 or row >= self.pages_list.count() - 1:
            return
        self.pages_list.insertItem(row + 1, self.pages_list.takeItem(row))
        self.pages_list.setCurrentRow(row + 1)
        self._update_labels()

    def _update_labels(self) -> None:
        for i in range(self.pages_list.count()):
            original = self.pages_list.item(i).data(Qt.ItemDataRole.UserRole)
            self.pages_list.item(i).setText(f"Page {original + 1}")

    def rotate_selected(self) -> None:
        row = self.pages_list.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No page selected", "Select a page first.")
            return
        item = self.pages_list.item(row)
        current = item.data(Qt.ItemDataRole.UserRole + 2) or 0
        item.setData(Qt.ItemDataRole.UserRole + 2, (current + 90) % 360)
        self._refresh_icons()

    def delete_selected(self) -> None:
        row = self.pages_list.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No page selected", "Select a page first.")
            return
        if self.pages_list.count() <= 1:
            QMessageBox.warning(self, "Cannot delete", "A PDF must retain at least one page.")
            return
        self.pages_list.takeItem(row)
        self._update_labels()

    def save(self) -> None:
        if self.path is None or self.pages_list.count() == 0:
            QMessageBox.warning(self, "No PDF loaded", "Select a PDF first.")
            return
        output, _ = QFileDialog.getSaveFileName(self, "Save PDF", filter="PDF files (*.pdf)")
        if not output:
            return
        page_order: list[int] = []
        rotations: dict[int, int] = {}
        for i in range(self.pages_list.count()):
            item = self.pages_list.item(i)
            original_index = item.data(Qt.ItemDataRole.UserRole)
            page_order.append(original_index)
            rot = item.data(Qt.ItemDataRole.UserRole + 2) or 0
            if rot:
                rotations[i] = rot
        try:
            transform_pages(self.path, Path(output), page_order, rotations)
        except (FileExistsError, OSError, ValueError) as error:
            QMessageBox.warning(self, "Unable to save PDF", str(error))
        else:
            QMessageBox.information(self, "PDF saved", f"Saved to {output}")
