from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("PDF SafeTools")
        title.setObjectName("page-title")
        title.setStyleSheet("font-size: 28px;")

        desc = QLabel("Local PDF utility and security tool")
        desc.setObjectName("page-desc")

        banner = QFrame()
        banner.setObjectName("local-banner")
        banner_layout = QVBoxLayout(banner)
        banner_layout.setContentsMargins(15, 15, 15, 15)
        banner_layout.setSpacing(5)

        banner_title = QLabel("Pemrosesan lokal aktif")
        banner_title.setObjectName("local-banner-title")

        banner_desc = QLabel(
            "Semua dokumen PDF diproses sepenuhnya di komputer Anda.\n"
            "Tidak ada dokumen yang diunggah ke internet, server, atau cloud pihak ketiga."
        )
        banner_desc.setObjectName("local-banner-desc")
        banner_desc.setWordWrap(True)

        banner_layout.addWidget(banner_title)
        banner_layout.addWidget(banner_desc)

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addWidget(banner)
        layout.addStretch()
