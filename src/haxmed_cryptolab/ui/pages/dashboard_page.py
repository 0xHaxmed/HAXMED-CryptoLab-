"""Module A — Dashboard Landing Page."""

import platform
import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from haxmed_cryptolab.core.constants import APP_NAME, APP_SLOGAN, APP_VERSION
from haxmed_cryptolab.services.crypto_service import CryptoService
from haxmed_cryptolab.services.history_service import HistoryService
from haxmed_cryptolab.ui.i18n import i18n


class DashboardPage(QWidget):
    """Professional landing page with branding, diagnostics, and quick shortcuts."""

    navigate_requested = Signal(str)  # target page key

    def __init__(
        self,
        crypto_service: CryptoService,
        history_service: HistoryService,
        parent=None,
    ):
        super().__init__(parent)
        self.crypto_service = crypto_service
        self.history_service = history_service

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(18)

        # 1. Branding Header
        header_card = QFrame()
        header_card.setObjectName("card")
        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(16, 14, 16, 14)

        lbl_app = QLabel(
            f"{APP_NAME} <span style='color:#E02235; font-size:14px;'>v{APP_VERSION}</span>"
        )
        lbl_app.setTextFormat(Qt.RichText)
        lbl_app.setObjectName("section_title")

        lbl_slogan = QLabel(f"{APP_SLOGAN} — {i18n.tr('brand_tagline')}")
        lbl_slogan.setObjectName("section_desc")

        header_layout.addWidget(lbl_app)
        header_layout.addWidget(lbl_slogan)
        layout.addWidget(header_card)

        # 2. System Diagnostics Metrics
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(12)

        os_name = f"{platform.system()} {platform.release()}"
        py_ver = sys.version.split()[0]
        history_status = (
            i18n.tr("dash_enabled")
            if self.history_service.config_mgr.config.enable_history
            else i18n.tr("dash_disabled")
        )
        op_count = str(self.history_service.count_records())

        self.card_os = self._create_stat_card(i18n.tr("dash_os_label"), os_name, platform.machine())
        self.card_py = self._create_stat_card(
            i18n.tr("dash_python_ver"), py_ver, "C胞/PySide6 6.12"
        )
        self.card_engine = self._create_stat_card(
            "Engine", "Online", "AES, RSA, SHA, Bcrypt, Argon2"
        )
        self.card_history = self._create_stat_card(
            i18n.tr("dash_history_status"), history_status, f"{op_count} recorded"
        )

        metrics_grid.addWidget(self.card_os, 0, 0)
        metrics_grid.addWidget(self.card_py, 0, 1)
        metrics_grid.addWidget(self.card_engine, 0, 2)
        metrics_grid.addWidget(self.card_history, 0, 3)
        layout.addLayout(metrics_grid)

        # 3. Quick Navigation Workflows
        quick_group = QGroupBox(i18n.tr("dash_quick_actions"))
        quick_layout = QHBoxLayout(quick_group)
        quick_layout.setSpacing(12)

        btn_enc = QPushButton(f"🔒 {i18n.tr('nav_encryption')}")
        btn_enc.setObjectName("primary_btn")
        btn_enc.clicked.connect(lambda: self.navigate_requested.emit("encryption"))

        btn_hash = QPushButton(f"#️⃣ {i18n.tr('nav_hash')}")
        btn_hash.clicked.connect(lambda: self.navigate_requested.emit("hash"))

        btn_rec = QPushButton(f"🧪 {i18n.tr('nav_recovery')}")
        btn_rec.clicked.connect(lambda: self.navigate_requested.emit("recovery"))

        btn_ana = QPushButton(f"📊 {i18n.tr('nav_analyzer')}")
        btn_ana.clicked.connect(lambda: self.navigate_requested.emit("analyzer"))

        quick_layout.addWidget(btn_enc)
        quick_layout.addWidget(btn_hash)
        quick_layout.addWidget(btn_rec)
        quick_layout.addWidget(btn_ana)
        layout.addWidget(quick_group)

        # 4. Educational Cryptographic Highlights
        edu_card = QFrame()
        edu_card.setObjectName("card")
        edu_layout = QVBoxLayout(edu_card)
        edu_title = QLabel(f"💡 {i18n.tr('dash_edu_notes')}")
        edu_title.setStyleSheet("color: #E02235; font-weight: 700; font-size: 14px;")

        edu_content = QLabel(
            "<b>1. Authenticated Encryption:</b> AES-GCM guarantees both secrecy (confidentiality) and tampering detection (authenticity). Never reuse a Nonce with the same key.<br/>"
            "<b>2. Asymmetric Limits:</b> RSA-OAEP encrypts messages smaller than key size minus padding (max 190 bytes for RSA-2048). Use hybrid schemes for files.<br/>"
            "<b>3. Hashing vs Password Storage:</b> Standard SHA-256 is too fast for passwords. Always employ memory-hard salted algorithms like Argon2id or Bcrypt.<br/>"
            "<b>4. Classical Insecurity:</b> Classical substitution and transposition ciphers preserve letter patterns and are broken in fractions of a second."
        )
        edu_content.setWordWrap(True)
        edu_content.setTextFormat(Qt.RichText)
        edu_content.setStyleSheet("color: #C2C6D2; line-height: 150%; padding-top: 4px;")

        edu_layout.addWidget(edu_title)
        edu_layout.addWidget(edu_content)
        layout.addWidget(edu_card)

        # 5. Active Task Status Monitor
        task_group = QGroupBox(i18n.tr("dash_active_tasks"))
        task_layout = QVBoxLayout(task_group)
        self.lbl_active_tasks = QLabel(f"🟢 {i18n.tr('dash_no_tasks')}")
        self.lbl_active_tasks.setStyleSheet("color: #8C90A0; font-style: italic;")
        task_layout.addWidget(self.lbl_active_tasks)
        layout.addWidget(task_group)

        layout.addStretch()
        scroll.setWidget(container)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _create_stat_card(self, title: str, value: str, subtitle: str) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(2)

        lbl_t = QLabel(title)
        lbl_t.setStyleSheet("color: #8C90A0; font-size: 11px; font-weight: 600;")
        lbl_v = QLabel(value)
        lbl_v.setStyleSheet(
            "color: #FFFFFF; font-size: 16px; font-weight: bold; font-family: monospace;"
        )
        lbl_s = QLabel(subtitle)
        lbl_s.setStyleSheet("color: #E02235; font-size: 10px;")

        lay.addWidget(lbl_t)
        lay.addWidget(lbl_v)
        lay.addWidget(lbl_s)
        return card

    def refresh_stats(self):
        """Update dynamic counters on page display."""
        op_count = str(self.history_service.count_records())
        hist_status = (
            i18n.tr("dash_enabled")
            if self.history_service.config_mgr.config.enable_history
            else i18n.tr("dash_disabled")
        )
        # update card texts
        card_labels = self.card_history.findChildren(QLabel)
        if len(card_labels) >= 3:
            card_labels[1].setText(hist_status)
            card_labels[2].setText(f"{op_count} recorded")
