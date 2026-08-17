from pathlib import Path
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QProgressBar,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from PySide6.QtGui import QColor

from app.services.compress_service import compress_pdf
from app.services.sanitize_service import sanitize_pdf
from app.services.scan_service import scan_pdf

RISK_COLORS: dict[str, str] = {
    "SAFE": "#168C8C",
    "LOW": "#A0A000",
    "MEDIUM": "#D97706",
    "HIGH": "#DC2626",
    "CRITICAL": "#991B1B",
}


def _human_size(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}" if unit != "B" else f"{size} B"
        size /= 1024  # type: ignore[assignment]
    return f"{size:.1f} TB"


class BatchWorker(QObject):
    progress = Signal(int, object, object)
    finished = Signal()

    def __init__(
        self, files: list[Path], operation: str, output_folder: Path | None = None
    ) -> None:
        super().__init__()
        self.files = files
        self.operation = operation
        self.output_folder = output_folder

    @Slot()
    def run(self) -> None:
        for index, pdf_file in enumerate(self.files):
            try:
                result: Any
                if self.operation == "scan":
                    result = scan_pdf(pdf_file)
                elif self.operation == "sanitize":
                    assert self.output_folder is not None
                    result = sanitize_pdf(
                        pdf_file,
                        self.output_folder / f"{pdf_file.stem}_clean.pdf",
                        preset="JKN Safe Mode",
                    )
                else:
                    assert self.output_folder is not None
                    result = compress_pdf(
                        pdf_file, self.output_folder / f"{pdf_file.stem}_compressed.pdf", "Medium"
                    )
                self.progress.emit(index, result, None)
            except Exception as error:  # noqa: BLE001
                self.progress.emit(index, None, error)
        self.finished.emit()


class BatchPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.result = QTreeWidget()
        self.result.setHeaderLabels(["Label", "Value"])
        self.result.setRootIsDecorated(True)
        self.result.setItemsExpandable(True)
        self.result.setAlternatingRowColors(False)
        self.result.setUniformRowHeights(True)
        self.result.setColumnWidth(0, 320)
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self._thread: QThread | None = None
        self._worker: BatchWorker | None = None
        scan_button = QPushButton("Batch scan folder")
        sanitize_button = QPushButton("Batch sanitize folder")
        compress_button = QPushButton("Batch compress folder")
        scan_button.clicked.connect(self._batch_scan)
        sanitize_button.clicked.connect(self._batch_sanitize)
        compress_button.clicked.connect(self._batch_compress)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Batch Processing")
        title.setObjectName("page-title")
        layout.addWidget(title)
        layout.addWidget(QLabel("Select a folder — all PDF files inside are processed."))
        layout.addWidget(scan_button)
        layout.addWidget(sanitize_button)
        layout.addWidget(compress_button)
        layout.addWidget(self.progress)
        layout.addWidget(self.result)

    # ── public entry points ──────────────────────────────────────────

    def _batch_scan(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select folder")
        if not folder:
            return
        pdf_files = sorted(Path(folder).glob("*.pdf"))
        self._start_batch(pdf_files, "scan", Path(folder), None)

    def _batch_sanitize(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select folder")
        if not folder:
            return
        output_folder = Path(folder) / "sanitized"
        output_folder.mkdir(exist_ok=True)
        pdf_files = sorted(Path(folder).glob("*.pdf"))
        self._start_batch(pdf_files, "sanitize", Path(folder), output_folder)

    def _batch_compress(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select folder")
        if not folder:
            return
        output_folder = Path(folder) / "compressed"
        output_folder.mkdir(exist_ok=True)
        pdf_files = sorted(Path(folder).glob("*.pdf"))
        self._start_batch(pdf_files, "compress", Path(folder), output_folder)

    def _start_batch(
        self, files: list[Path], operation: str, folder: Path, output: Path | None
    ) -> None:
        self.result.clear()
        self._root = self._summary_root(
            operation.title(), len(files), str(folder), str(output) if output else None
        )
        self._items = [QTreeWidgetItem(self._root, [path.name, ""]) for path in files]
        self.progress.setRange(0, len(files))
        self.progress.setValue(0)
        self.progress.setVisible(True)
        self._thread = QThread(self)
        self._worker = BatchWorker(files, operation, output)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._batch_progress)
        self._worker.finished.connect(self._batch_finished)
        self._worker.finished.connect(self._thread.quit)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    @Slot(int, object, object)
    def _batch_progress(self, index: int, result: Any, error: Any) -> None:
        item = self._items[index]
        if error is not None:
            self._error_item(item, error if isinstance(error, Exception) else Exception(str(error)))
        elif self._root.text(0).startswith("Scan"):
            scan = result
            self._scan_detail_item(item, scan.risk_level, scan.status, scan.sha256, scan.findings)
        elif self._root.text(0).startswith("Sanitize"):
            sanitized = result
            self._sanitize_detail_item(
                item,
                sanitized.scan.risk_level,
                sanitized.scan.status,
                sanitized.scan.sha256,
                sanitized.scan.findings,
                str(sanitized.output),
                sanitized.original_sha256,
                sanitized.output_sha256,
                sanitized.removed,
                sum(sanitized.removed.values()),
            )
        else:
            compressed = result
            self._compress_detail_item(
                item,
                str(compressed.output),
                compressed.original_size,
                compressed.output_size,
                compressed.reduction_percent,
            )
        self.progress.setValue(index + 1)

    @Slot()
    def _batch_finished(self) -> None:
        self._finalize_summary(self._root, len(self._items))
        self.progress.setVisible(False)
        self._worker = None
        self._thread = None

    # ── tree builders ────────────────────────────────────────────────

    def _summary_root(
        self, op: str, count: int, folder: str, output: str | None
    ) -> QTreeWidgetItem:
        label = f"{op} — {count} PDF" + ("s" if count != 1 else "")
        root = QTreeWidgetItem(self.result, [label, ""])
        font = root.font(0)
        font.setBold(True)
        font.setPointSize(font.pointSize() + 1)
        root.setFont(0, font)
        QTreeWidgetItem(root, ["Source folder", folder])
        if output:
            QTreeWidgetItem(root, ["Output folder", output])
        return root

    def _finalize_summary(self, root: QTreeWidgetItem, total: int) -> None:
        error_count = root.childCount() - self._info_child_count(root)
        ok_count = total - error_count
        status = f"Done — {ok_count} ok, {error_count} failed" if total else "No PDF files found"
        status_item = QTreeWidgetItem(root, ["Status", status])
        font = status_item.font(0)
        font.setBold(True)
        status_item.setFont(0, font)
        self.result.expandItem(root)
        if root.childCount() <= 4:
            self.result.expandAll()

    def _info_child_count(self, root: QTreeWidgetItem) -> int:
        count = 0
        for i in range(root.childCount()):
            child = root.child(i)
            if child.childCount() == 0 and child.text(0) in {
                "Source folder",
                "Output folder",
                "Status",
            }:
                count += 1
        return count + 1  # +1 for Status row itself

    def _scan_detail_item(
        self,
        parent: QTreeWidgetItem,
        risk_level: str,
        status: str,
        sha256: str,
        findings: list[Any],
    ) -> None:
        parent.setText(1, risk_level)
        parent.setForeground(1, _qcolor(RISK_COLORS.get(risk_level, "#1B2A38")))
        QTreeWidgetItem(parent, ["Status", status])
        QTreeWidgetItem(parent, ["SHA-256", sha256])
        if findings:
            f_root = QTreeWidgetItem(parent, ["Findings", f"{len(findings)} type(s)"])
            for f in findings:
                QTreeWidgetItem(
                    f_root,
                    [f.type, f"{f.severity} · count={f.count}"],
                )
                QTreeWidgetItem(f_root, ["  description", f.description])

    def _sanitize_detail_item(
        self,
        parent: QTreeWidgetItem,
        risk_level: str,
        status: str,
        sha256: str,
        findings: list[Any],
        output: str,
        original_sha: str,
        output_sha: str,
        removed: dict[str, int],
        removed_total: int,
    ) -> None:
        parent.setText(1, f"removed {removed_total}")
        parent.setForeground(1, _qcolor(RISK_COLORS.get(risk_level, "#1B2A38")))
        QTreeWidgetItem(parent, ["Output", output])
        QTreeWidgetItem(parent, ["Source SHA-256", original_sha])
        QTreeWidgetItem(parent, ["Output SHA-256", output_sha])
        QTreeWidgetItem(parent, ["Re-scan risk", risk_level])
        QTreeWidgetItem(parent, ["Re-scan status", status])
        if removed:
            r_root = QTreeWidgetItem(parent, ["Removed items", f"{removed_total} total"])
            for rule, cnt in removed.items():
                QTreeWidgetItem(r_root, [rule, str(cnt)])
        if findings:
            f_root = QTreeWidgetItem(parent, ["Remaining findings", f"{len(findings)} type(s)"])
            for f in findings:
                QTreeWidgetItem(f_root, [f.type, f"{f.severity} · count={f.count}"])

    def _compress_detail_item(
        self,
        parent: QTreeWidgetItem,
        output: str,
        original_size: int,
        output_size: int,
        reduction: float,
    ) -> None:
        parent.setText(1, f"{reduction:.1f}% smaller")
        color = "#168C8C" if reduction > 0 else "#A0A000"
        parent.setForeground(1, _qcolor(color))
        QTreeWidgetItem(parent, ["Output", output])
        QTreeWidgetItem(parent, ["Original size", _human_size(original_size)])
        QTreeWidgetItem(parent, ["Compressed size", _human_size(output_size)])
        QTreeWidgetItem(parent, ["Reduction", f"{reduction:.1f}%"])

    def _error_item(self, parent: QTreeWidgetItem, error: Exception) -> None:
        parent.setText(1, "ERROR")
        parent.setForeground(1, _qcolor("#DC2626"))
        font = parent.font(0)
        font.setBold(True)
        parent.setFont(0, font)
        QTreeWidgetItem(parent, ["Error", str(error)])


def _qcolor(hex_code: str) -> "QColor":
    from PySide6.QtGui import QColor

    return QColor(hex_code)
