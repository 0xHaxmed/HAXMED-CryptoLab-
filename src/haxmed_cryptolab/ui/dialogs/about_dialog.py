"""About HAXMED CryptoLab modal dialog."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from haxmed_cryptolab.core.constants import LOGO_BANNER_PATH, LOGO_SHIELD_PATH
from haxmed_cryptolab.ui.i18n import i18n


class AboutDialog(QDialog):
    """About dialog presenting application metadata, brand, and license."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(i18n.tr("about_dialog_title"))
        self.setFixedSize(520, 460)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 20, 28, 20)
        layout.setSpacing(14)

        # Brand Hero Banner
        banner_path = LOGO_BANNER_PATH if LOGO_BANNER_PATH.exists() else LOGO_SHIELD_PATH
        if banner_path.exists():
            lbl_banner = QLabel()
            lbl_banner.setAlignment(Qt.AlignCenter)
            pix = QPixmap(str(banner_path))
            if not pix.isNull():
                lbl_banner.setPixmap(pix.scaledToWidth(280, Qt.SmoothTransformation))
                layout.addWidget(lbl_banner)

        lbl_content = QLabel(i18n.tr("about_text"))
        lbl_content.setWordWrap(True)
        lbl_content.setTextFormat(Qt.RichText)
        lbl_content.setAlignment(Qt.AlignCenter)
        lbl_content.setStyleSheet("line-height: 140%; font-size: 13px;")

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_close = QPushButton(i18n.tr("btn_close"))
        btn_close.setFixedWidth(100)
        btn_close.clicked.connect(self.accept)
        btn_row.addWidget(btn_close)
        btn_row.addStretch()

        layout.addWidget(lbl_content)
        layout.addStretch()
        layout.addLayout(btn_row)

