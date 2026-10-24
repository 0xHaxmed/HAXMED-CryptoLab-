"""About HAXMED CryptoLab modal dialog."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from haxmed_cryptolab.ui.i18n import i18n


class AboutDialog(QDialog):
    """About dialog presenting application metadata, brand, and license."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(i18n.tr("about_dialog_title"))
        self.setFixedSize(480, 280)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        lbl_content = QLabel(i18n.tr("about_text"))
        lbl_content.setWordWrap(True)
        lbl_content.setTextFormat(Qt.RichText)
        lbl_content.setStyleSheet("line-height: 140%;")

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_close = QPushButton(i18n.tr("btn_close"))
        btn_close.clicked.connect(self.accept)
        btn_row.addWidget(btn_close)

        layout.addWidget(lbl_content)
        layout.addStretch()
        layout.addLayout(btn_row)
