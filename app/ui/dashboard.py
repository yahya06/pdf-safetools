from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("PDF SafeTools")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(title)
        layout.addWidget(QLabel("Local PDF utility and security tool"))
        layout.addStretch()
