from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from app.config.settings import APP_INFO


class AboutPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel(f"{APP_INFO['name']} v{APP_INFO['version']}")
        title.setObjectName("page-title")
        layout.addWidget(title)
        layout.addWidget(QLabel(f"Developed by {APP_INFO['developer']}"))
        layout.addWidget(QLabel(f"Project Origin: {APP_INFO['institution']}"))
        layout.addWidget(QLabel(APP_INFO["location"]))
        layout.addStretch()
