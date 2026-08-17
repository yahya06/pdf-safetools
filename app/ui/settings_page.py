from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SettingsPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Settings")
        title.setObjectName("page-title")
        layout.addWidget(title)
        layout.addWidget(QLabel("Configuration options will be available here."))
        layout.addStretch()
