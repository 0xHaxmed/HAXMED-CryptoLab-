"""Module A — Dashboard Landing Page with Universal Crypto Inspector."""

import platform
import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from haxmed_cryptolab.core.constants import (
    APP_NAME,
    APP_SLOGAN,
    APP_VERSION,
    LOGO_SHIELD_PATH,
)
from haxmed_cryptolab.engines.analysis.detector import SmartDetector
from haxmed_cryptolab.models import DetectionReport
from haxmed_cryptolab.services.analysis_service import AnalysisService
from haxmed_cryptolab.services.crypto_service import CryptoService
from haxmed_cryptolab.services.history_service import HistoryService
from haxmed_cryptolab.ui.i18n import i18n


class DashboardPage(QWidget):
    """Professional landing page with branding, diagnostics, and universal auto-detector."""

    navigate_requested = Signal(str)  # target page key

    def __init__(
        self,
        crypto_service: CryptoService,
        history_service: HistoryService,
        analysis_service: AnalysisService,
        parent=None,
    ):
        super().__init__(parent)
        self.crypto_service = crypto_service
        self.history_service = history_service
        self.analysis_service = analysis_service
        self._last_report: DetectionReport = None

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
        header_layout = QHBoxLayout(header_card)
        header_layout.setContentsMargins(18, 14, 18, 14)
        header_layout.setSpacing(18)

        if LOGO_SHIELD_PATH.exists():
            lbl_shield = QLabel()
            pix = QPixmap(str(LOGO_SHIELD_PATH))
            if not pix.isNull():
                lbl_shield.setPixmap(pix.scaledToHeight(68, Qt.SmoothTransformation))
                header_layout.addWidget(lbl_shield)

        text_vbox = QVBoxLayout()
        text_vbox.setSpacing(4)

        lbl_app = QLabel(
            f"{APP_NAME} <span style='color:#E02235; font-size:14px; font-weight:bold;'>v{APP_VERSION}</span>"
        )
        lbl_app.setTextFormat(Qt.RichText)
        lbl_app.setObjectName("section_title")

        lbl_slogan = QLabel(f"{APP_SLOGAN} — {i18n.tr('brand_tagline')}")
        lbl_slogan.setObjectName("section_desc")

        lbl_features = QLabel(
            "<span style='color:#94A3B8; font-size:11px; font-weight:bold; letter-spacing:1px;'>"
            "ENCRYPT • DECRYPT • HASH • RECOVER • ANALYZE"
            "</span>"
        )
        lbl_features.setTextFormat(Qt.RichText)

        text_vbox.addWidget(lbl_app)
        text_vbox.addWidget(lbl_slogan)
        text_vbox.addWidget(lbl_features)

        header_layout.addLayout(text_vbox)
        header_layout.addStretch()
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

        # 3. UNIVERSAL CRYPTO INSPECTOR & AUTO-DETECTOR
        detect_group = QGroupBox(f"🔍 {i18n.tr('dash_autodetect_title')}")
        d_lay = QVBoxLayout(detect_group)
        d_lay.setSpacing(10)

        lbl_desc = QLabel(i18n.tr("dash_autodetect_desc"))
        lbl_desc.setStyleSheet("color: #8C90A0; font-size: 12px;")
        d_lay.addWidget(lbl_desc)

        self.txt_inspect_in = QPlainTextEdit()
        self.txt_inspect_in.setPlaceholderText(
            "Paste any ciphertext, hash digest ($2b$, SHA-256, MD5...), AES container JSON, or RSA key here..."
        )
        self.txt_inspect_in.setMaximumHeight(85)
        d_lay.addWidget(self.txt_inspect_in)

        # Action Buttons
        d_btn_row = QHBoxLayout()
        self.btn_auto_detect = QPushButton(i18n.tr("btn_auto_detect"))
        self.btn_auto_detect.setObjectName("primary_btn")
        self.btn_auto_detect.clicked.connect(self._run_auto_detect)
        d_btn_row.addWidget(self.btn_auto_detect)

        self.btn_action_target = QPushButton("Open in Suggested Studio")
        self.btn_action_target.setVisible(False)
        self.btn_action_target.clicked.connect(self._navigate_suggested_action)
        d_btn_row.addWidget(self.btn_action_target)

        d_btn_row.addStretch()
        d_lay.addLayout(d_btn_row)

        # Result Banner
        self.frame_detect_res = QFrame()
        self.frame_detect_res.setObjectName("card")
        self.frame_detect_res.setVisible(False)
        r_lay = QVBoxLayout(self.frame_detect_res)
        self.lbl_detect_title = QLabel("DETECTION RESULT")
        self.lbl_detect_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #E02235;")
        self.lbl_detect_body = QLabel("")
        self.lbl_detect_body.setStyleSheet("line-height: 140%; color: #E2E4E9;")
        self.lbl_detect_body.setWordWrap(True)
        r_lay.addWidget(self.lbl_detect_title)
        r_lay.addWidget(self.lbl_detect_body)
        d_lay.addWidget(self.frame_detect_res)

        layout.addWidget(detect_group)

        # 4. Quick Navigation Workflows
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

        # 5. Educational Cryptographic Highlights
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

        # 6. Active Task Status Monitor
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

    def _run_auto_detect(self):
        text = self.txt_inspect_in.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "Auto-Detector", "Please enter or paste text to analyze.")
            return

        report = SmartDetector.analyze(text)
        self._last_report = report
        self.frame_detect_res.setVisible(True)

        conf_color = (
            "#28A745"
            if report.confidence == "HIGH"
            else ("#FFC107" if report.confidence == "MEDIUM" else "#E02235")
        )
        self.lbl_detect_title.setText(
            f"🎯 {report.suggested_algorithm} <span style='font-size:12px; color:{conf_color};'>[{report.confidence} CONFIDENCE]</span>"
        )
        self.lbl_detect_title.setTextFormat(Qt.RichText)

        body_text = f"<b>Summary:</b> {report.summary}<br/><b>Details:</b> {report.details}"
        self.lbl_detect_body.setText(body_text)

        if report.suggested_action == "DECRYPT_AES":
            self.btn_action_target.setText("🔓 " + i18n.tr("btn_open_decryptor") + " (AES-GCM)")
            self.btn_action_target.setVisible(True)
        elif report.suggested_action == "DECRYPT_CAESAR":
            self.btn_action_target.setText("🔓 " + i18n.tr("btn_open_decryptor") + " (Caesar)")
            self.btn_action_target.setVisible(True)
        elif report.suggested_action == "DECRYPT_RSA":
            self.btn_action_target.setText("🔓 " + i18n.tr("btn_open_decryptor") + " (RSA)")
            self.btn_action_target.setVisible(True)
        elif report.suggested_action == "HASH_WORKBENCH":
            self.btn_action_target.setText("#️⃣ " + i18n.tr("btn_open_hash"))
            self.btn_action_target.setVisible(True)
        elif report.suggested_action == "RECOVERY_LAB":
            self.btn_action_target.setText("🧪 " + i18n.tr("btn_open_recovery"))
            self.btn_action_target.setVisible(True)
        elif report.suggested_action == "CIPHER_ANALYZER":
            self.btn_action_target.setText("📊 Open in Cipher Analyzer")
            self.btn_action_target.setVisible(True)
        else:
            self.btn_action_target.setVisible(False)

    def _navigate_suggested_action(self):
        if not self._last_report:
            return
        action = self._last_report.suggested_action
        if action in ("DECRYPT_AES", "DECRYPT_CAESAR", "DECRYPT_RSA", "ENCRYPT_STUDIO"):
            self.navigate_requested.emit("encryption")
        elif action == "HASH_WORKBENCH":
            self.navigate_requested.emit("hash")
        elif action == "RECOVERY_LAB":
            self.navigate_requested.emit("recovery")
        elif action == "CIPHER_ANALYZER":
            self.navigate_requested.emit("analyzer")

    def refresh_stats(self):
        """Update dynamic counters on page display."""
        op_count = str(self.history_service.count_records())
        hist_status = (
            i18n.tr("dash_enabled")
            if self.history_service.config_mgr.config.enable_history
            else i18n.tr("dash_disabled")
        )
        card_labels = self.card_history.findChildren(QLabel)
        if len(card_labels) >= 3:
            card_labels[1].setText(hist_status)
            card_labels[2].setText(f"{op_count} recorded")
