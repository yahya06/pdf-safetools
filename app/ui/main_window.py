from PySide6.QtWidgets import QHBoxLayout, QListWidget, QMainWindow, QStackedWidget, QWidget

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
from app.ui.settings_page import SettingsPage
from app.ui.split_page import SplitPage


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PDF SafeTools")
        self.resize(1080, 720)

        self.navigation = QListWidget()
        self.navigation.setObjectName("sidebar")
        self.navigation.addItems(
            [
                "Dashboard",
                "Merge",
                "Split",
                "Organize",
                "Compress",
                "Convert",
                "PDF Information",
                "Scan PDF",
                "Sanitize PDF",
                "Batch",
                "Settings",
                "About",
            ]
        )
        self.navigation.setFixedWidth(200)

        self.pages = QStackedWidget()
        for page in (
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
            SettingsPage(),
            AboutPage(),
        ):
            self.pages.addWidget(page)
        self.navigation.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.navigation.setCurrentRow(0)

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.navigation)
        layout.addWidget(self.pages)
        self.setCentralWidget(container)
