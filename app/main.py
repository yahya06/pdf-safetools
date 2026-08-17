import sys

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow
from app.utils.logging_utils import configure_logging


def main() -> int:
    configure_logging()
    application = QApplication(sys.argv)

    application.setStyleSheet("""
        QMainWindow {
            background-color: #F2F6F9;
        }
        QWidget {
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
            color: #1B2A38;
        }
        QListWidget#sidebar {
            background-color: #22394A;
            border: none;
            outline: 0;
            padding-top: 10px;
        }
        QListWidget#sidebar::item {
            color: #D8E2E8;
            padding: 10px 15px;
            border-radius: 4px;
            margin: 2px 8px;
        }
        QListWidget#sidebar::item:hover {
            background-color: #2E4E64;
            color: #FFFFFF;
        }
        QListWidget#sidebar::item:selected {
            background-color: #168C8C;
            color: #FFFFFF;
            font-weight: bold;
        }
        QLineEdit, QSpinBox, QComboBox {
            background-color: #FFFFFF;
            border: 1px solid #D8E2E8;
            border-radius: 4px;
            padding: 6px 10px;
            selection-background-color: #168C8C;
        }
        QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
            border: 1px solid #168C8C;
        }
        QListWidget {
            background-color: #FFFFFF;
            border: 1px solid #D8E2E8;
            border-radius: 4px;
            padding: 5px;
        }
        QPushButton {
            background-color: #FFFFFF;
            border: 1px solid #D8E2E8;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #F2F6F9;
            border-color: #B2C3CF;
        }
        QPushButton:pressed {
            background-color: #E2EBF0;
        }
        QPushButton[primary="true"] {
            background-color: #168C8C;
            color: #FFFFFF;
            border: none;
            font-weight: bold;
        }
        QPushButton[primary="true"]:hover {
            background-color: #1B9E9E;
        }
        QPushButton[primary="true"]:pressed {
            background-color: #116B6B;
        }
        QLabel#page-title {
            font-size: 20px;
            font-weight: bold;
            color: #1B2A38;
            margin-bottom: 5px;
        }
        QLabel#page-desc {
            font-size: 13px;
            color: #61717E;
            margin-bottom: 15px;
        }
        QFrame#local-banner {
            background-color: #E6F4F4;
            border: 1px solid #BFE3E3;
            border-radius: 6px;
            padding: 12px;
        }
        QLabel#local-banner-title {
            font-weight: bold;
            color: #168C8C;
            font-size: 14px;
        }
        QLabel#local-banner-desc {
            color: #2E4E64;
            font-size: 12px;
        }
    """)

    window = MainWindow()
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
