"""Sidebar navigation component for HAXMED CryptoLab."""

from typing import Dict

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from haxmed_cryptolab.core.constants import (
    APP_NAME,
    APP_VERSION,
    LOGO_HORIZONTAL_PATH,
)
from haxmed_cryptolab.ui.dialogs.about_dialog import AboutDialog
from haxmed_cryptolab.ui.i18n import i18n


class NavigationSidebar(QFrame):
    """Sidebar navigation bar with HAXMED branding and tab buttons."""

    page_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(6)

        # 1. Brand Header
        brand_frame = QFrame()
        brand_frame.setObjectName("brand_header")
        brand_lay = QVBoxLayout(brand_frame)
        brand_lay.setContentsMargins(4, 4, 4, 12)
        brand_lay.setSpacing(4)

        if LOGO_HORIZONTAL_PATH.exists():
            self.lbl_logo = QLabel()
            self.lbl_logo.setAlignment(Qt.AlignCenter)
            pix = QPixmap(str(LOGO_HORIZONTAL_PATH))
            if not pix.isNull():
                self.lbl_logo.setPixmap(pix.scaledToWidth(170, Qt.SmoothTransformation))
                brand_lay.addWidget(self.lbl_logo)
            else:
                self.lbl_brand = QLabel(f"🛡️ {APP_NAME}")
                self.lbl_brand.setObjectName("brand_title")
                brand_lay.addWidget(self.lbl_brand)
        else:
            self.lbl_brand = QLabel(f"🛡️ {APP_NAME}")
            self.lbl_brand.setObjectName("brand_title")
            brand_lay.addWidget(self.lbl_brand)

        self.lbl_tagline = QLabel(f"v{APP_VERSION} — Security Lab")
        self.lbl_tagline.setObjectName("brand_tagline")
        self.lbl_tagline.setAlignment(Qt.AlignCenter)
        brand_lay.addWidget(self.lbl_tagline)

        layout.addWidget(brand_frame)

        # 2. Navigation Buttons
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)
        self.nav_buttons: Dict[str, QPushButton] = {}

        items = [
            ("dashboard", "🏠", "nav_dashboard"),
            ("encryption", "🔒", "nav_encryption"),
            ("hash", "#️⃣", "nav_hash"),
            ("recovery", "🧪", "nav_recovery"),
            ("analyzer", "📊", "nav_analyzer"),
            ("history", "📜", "nav_history"),
            ("settings", "⚙️", "nav_settings"),
        ]

        for key, icon, i18n_key in items:
            btn = QPushButton(f"{icon}  {i18n.tr(i18n_key)}")
            btn.setProperty("class", "nav_btn")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, k=key: self._on_btn_clicked(k))
            self.btn_group.addButton(btn)
            self.nav_buttons[key] = btn
            layout.addWidget(btn)

        layout.addStretch()

        # 3. About Button at bottom
        self.btn_about = QPushButton(f"ℹ️  {i18n.tr('nav_about')}")
        self.btn_about.setProperty("class", "nav_btn")
        self.btn_about.clicked.connect(self._show_about)
        layout.addWidget(self.btn_about)

        # Select Dashboard by default
        if "dashboard" in self.nav_buttons:
            self.nav_buttons["dashboard"].setChecked(True)

    def _on_btn_clicked(self, page_key: str):
        self.page_changed.emit(page_key)

    def select_page(self, page_key: str):
        if page_key in self.nav_buttons:
            self.nav_buttons[page_key].setChecked(True)
            self.page_changed.emit(page_key)

    def _show_about(self):
        dlg = AboutDialog(self)
        dlg.exec()

    def update_texts(self):
        """Update button labels upon language change."""
        items = [
            ("dashboard", "🏠", "nav_dashboard"),
            ("encryption", "🔒", "nav_encryption"),
            ("hash", "#️⃣", "nav_hash"),
            ("recovery", "🧪", "nav_recovery"),
            ("analyzer", "📊", "nav_analyzer"),
            ("history", "📜", "nav_history"),
            ("settings", "⚙️", "nav_settings"),
        ]
        for key, icon, i18n_key in items:
            if key in self.nav_buttons:
                self.nav_buttons[key].setText(f"{icon}  {i18n.tr(i18n_key)}")
        self.btn_about.setText(f"ℹ️  {i18n.tr('nav_about')}")
