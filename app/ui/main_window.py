from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.config.settings import APP_INFO
from app.ui.about_page import AboutPage
from app.ui.batch_page import BatchPage
from app.ui.compress_page import CompressPage
from app.ui.convert_page import ConvertPage
from app.ui.dashboard import DashboardPage
from app.ui.merge_page import MergePage
from app.ui.organize_page import OrganizePage
from app.ui.pdf_info_page import PdfInfoPage
from app.ui.sanitize_page import SanitizePage
from app.ui.scan_page import ScanPage
from app.ui.split_page import SplitPage
from app.ui.update_page import UpdatePage


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PDF SafeTools")
        self.resize(1080, 720)

        self.navigation = QListWidget()
        self.navigation.setObjectName("sidebar")
        self.navigation.setFixedWidth(200)

        self.pages = QStackedWidget()
        pages_list = [
            DashboardPage(),
            MergePage(),
            SplitPage(),
            OrganizePage(),
            CompressPage(),
            ConvertPage(),
            PdfInfoPage(),
            ScanPage(),
            SanitizePage(),
            BatchPage(),
            UpdatePage(),
            AboutPage(),
        ]
        for page in pages_list:
            self.pages.addWidget(page)

        menu_structure = [
            ("item", "Dashboard", 0),
            ("header", "PDF TOOLS", -1),
            ("item", "  Merge", 1),
            ("item", "  Split", 2),
            ("item", "  Organize", 3),
            ("item", "  Compress", 4),
            ("item", "  Convert", 5),
            ("item", "  PDF Information", 6),
            ("header", "SECURITY", -1),
            ("item", "  Scan PDF", 7),
            ("item", "  Sanitize PDF", 8),
            ("item", "  Batch", 9),
            ("header", "SYSTEM", -1),
            ("item", "  Update", 10),
            ("item", "  About", 11),
        ]

        for item_type, text, page_idx in menu_structure:
            item = QListWidgetItem(text)
            if item_type == "header":
                item.setFlags(Qt.ItemFlag.NoItemFlags)
                item.setData(Qt.ItemDataRole.UserRole, -1)
            else:
                item.setData(Qt.ItemDataRole.UserRole, page_idx)
            self.navigation.addItem(item)

        self.navigation.currentItemChanged.connect(self.on_item_changed)
        self.navigation.setCurrentRow(0)

        footer = QLabel()
        footer.setObjectName("footer")
        footer.setTextFormat(Qt.TextFormat.RichText)
        footer.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
        footer.setOpenExternalLinks(False)
        link_style = "color: #168C8C; text-decoration: none;"
        footer.setText(
            f"{APP_INFO['name']} v{APP_INFO['version']} · "
            f'<a href="{APP_INFO["repository"]}" style="{link_style}">Project by Yahya</a> '
            'with <span style="color:#D04A5A;">♥</span>'
        )
        footer.linkActivated.connect(lambda url: QDesktopServices.openUrl(QUrl(url)))
        footer.setStyleSheet(
            "color: #D8E2E8; font-size: 13px; font-weight: 500; padding: 12px 20px; "
            "background-color: #22394A;"
        )
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pages_with_footer = QWidget()
        pages_layout = QVBoxLayout(pages_with_footer)
        pages_layout.setContentsMargins(0, 0, 0, 0)
        pages_layout.setSpacing(0)
        pages_layout.addWidget(self.pages)
        pages_layout.addWidget(footer)

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.navigation)
        layout.addWidget(pages_with_footer)
        self.setCentralWidget(container)

    def on_item_changed(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        if not current:
            return
        page_idx = current.data(Qt.ItemDataRole.UserRole)
        if page_idx != -1:
            self.pages.setCurrentIndex(page_idx)
        elif previous:
            self.navigation.setCurrentItem(previous)
