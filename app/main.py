import sys

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow
from app.utils.logging_utils import configure_logging


def main() -> int:
    configure_logging()
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
