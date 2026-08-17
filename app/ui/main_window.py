from PySide6.QtWidgets import QHBoxLayout, QListWidget, QMainWindow, QStackedWidget, QWidget

from app.ui.about_page import AboutPage
from app.ui.dashboard import DashboardPage
from app.ui.settings_page import SettingsPage


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PDF SafeTools")
        self.resize(960, 640)

        self.navigation = QListWidget()
        self.navigation.addItems(["Dashboard", "Settings", "About"])
        self.navigation.setFixedWidth(180)

        self.pages = QStackedWidget()
        self.pages.addWidget(DashboardPage())
        self.pages.addWidget(SettingsPage())
        self.pages.addWidget(AboutPage())
        self.navigation.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.navigation.setCurrentRow(0)

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(self.navigation)
        layout.addWidget(self.pages)
        self.setCentralWidget(container)
