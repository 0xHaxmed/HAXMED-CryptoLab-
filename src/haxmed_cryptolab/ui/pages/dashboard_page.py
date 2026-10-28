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
    APP_VERSION,
    ICON_PNG_PATH,
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
        layout.setSpacing(16)

        # 1. Branding Header Card
        header_card = QFrame()
        header_card.setObjectName("card")
        header_layout = QHBoxLayout(header_card)
        header_layout.setContentsMargins(18, 14, 18, 14)
        header_layout.setSpacing(16)

        if ICON_PNG_PATH.exists():
            lbl_shield = QLabel()
            pix = QPixmap(str(ICON_PNG_PATH))
            if not pix.isNull():
                lbl_shield.setPixmap(pix.scaledToHeight(52, Qt.SmoothTransformation))
                header_layout.addWidget(lbl_shield)

        text_vbox = QVBoxLayout()
        text_vbox.setSpacing(3)

        self.lbl_app = QLabel(
            f"<b>{APP_NAME}</b> <span style='color:#E02235; font-size:14px; font-weight:bold;'>v{APP_VERSION}</span>"
        )
        self.lbl_app.setTextFormat(Qt.RichText)
        self.lbl_app.setObjectName("section_title")

        self.lbl_slogan = QLabel(f"{i18n.tr('app_subtitle')} — {i18n.tr('brand_tagline')}")
        self.lbl_slogan.setObjectName("section_desc")

        self.lbl_features = QLabel(
            "<span style='color:#94A3B8; font-size:11px; font-weight:600; letter-spacing:0.5px;'>"
            "ENCRYPT • DECRYPT • HASH • RECOVER • ANALYZE"
            "</span>"
        )
        self.lbl_features.setTextFormat(Qt.RichText)

        text_vbox.addWidget(self.lbl_app)
        text_vbox.addWidget(self.lbl_slogan)
        text_vbox.addWidget(self.lbl_features)

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

        self.card_os, self.lbl_os_t, self.lbl_os_v, self.lbl_os_s = self._create_stat_card_widget(
            i18n.tr("dash_os_label"), os_name, platform.machine()
        )
        self.card_py, self.lbl_py_t, self.lbl_py_v, self.lbl_py_s = self._create_stat_card_widget(
            i18n.tr("dash_python_ver"), py_ver, "PySide6 / Qt 6"
        )
        self.card_eng, self.lbl_eng_t, self.lbl_eng_v, self.lbl_eng_s = (
            self._create_stat_card_widget(
                i18n.tr("dash_crypto_status"),
                i18n.tr("dash_engine_online"),
                i18n.tr("dash_engine_details"),
            )
        )
        self.card_hist, self.lbl_hist_t, self.lbl_hist_v, self.lbl_hist_s = (
            self._create_stat_card_widget(
                i18n.tr("dash_history_status"),
                history_status,
                f"{op_count} {i18n.tr('dash_recorded_suffix')}",
            )
        )

        metrics_grid.addWidget(self.card_os, 0, 0)
        metrics_grid.addWidget(self.card_py, 0, 1)
        metrics_grid.addWidget(self.card_eng, 0, 2)
        metrics_grid.addWidget(self.card_hist, 0, 3)
        layout.addLayout(metrics_grid)

        # 3. UNIVERSAL CRYPTO INSPECTOR & AUTO-DETECTOR
        self.detect_group = QGroupBox(f"🔍 {i18n.tr('dash_autodetect_title')}")
        d_lay = QVBoxLayout(self.detect_group)
        d_lay.setSpacing(10)

        self.lbl_detect_desc = QLabel(i18n.tr("dash_autodetect_desc"))
        self.lbl_detect_desc.setStyleSheet("color: #9AA0B2; font-size: 12px;")
        d_lay.addWidget(self.lbl_detect_desc)

        self.txt_inspect_in = QPlainTextEdit()
        self.txt_inspect_in.setPlaceholderText(i18n.tr("dash_inspect_placeholder"))
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

        layout.addWidget(self.detect_group)

        # 4. Quick Navigation Workflows
        self.quick_group = QGroupBox(i18n.tr("dash_quick_actions"))
        quick_layout = QHBoxLayout(self.quick_group)
        quick_layout.setSpacing(12)

        self.btn_enc = QPushButton(f"🔒  {i18n.tr('nav_encryption')}")
        self.btn_enc.setObjectName("primary_btn")
        self.btn_enc.clicked.connect(lambda: self.navigate_requested.emit("encryption"))

        self.btn_hash = QPushButton(f"#️⃣  {i18n.tr('nav_hash')}")
        self.btn_hash.clicked.connect(lambda: self.navigate_requested.emit("hash"))

        self.btn_rec = QPushButton(f"🧪  {i18n.tr('nav_recovery')}")
        self.btn_rec.clicked.connect(lambda: self.navigate_requested.emit("recovery"))

        self.btn_ana = QPushButton(f"📊  {i18n.tr('nav_analyzer')}")
        self.btn_ana.clicked.connect(lambda: self.navigate_requested.emit("analyzer"))

        quick_layout.addWidget(self.btn_enc)
        quick_layout.addWidget(self.btn_hash)
        quick_layout.addWidget(self.btn_rec)
        quick_layout.addWidget(self.btn_ana)
        layout.addWidget(self.quick_group)

        # 5. Educational Cryptographic Highlights
        edu_card = QFrame()
        edu_card.setObjectName("card")
        edu_layout = QVBoxLayout(edu_card)
        self.edu_title = QLabel(f"💡 {i18n.tr('dash_edu_notes')}")
        self.edu_title.setStyleSheet("color: #E02235; font-weight: 700; font-size: 14px;")

        self.edu_content = QLabel()
        self.edu_content.setWordWrap(True)
        self.edu_content.setTextFormat(Qt.RichText)
        self.edu_content.setStyleSheet("color: #C2C6D2; line-height: 160%; padding-top: 4px;")
        self._update_edu_text()

        edu_layout.addWidget(self.edu_title)
        edu_layout.addWidget(self.edu_content)
        layout.addWidget(edu_card)

        # 6. Active Task Status Monitor
        self.task_group = QGroupBox(i18n.tr("dash_active_tasks"))
        task_layout = QVBoxLayout(self.task_group)
        self.lbl_active_tasks = QLabel(f"🟢 {i18n.tr('dash_no_tasks')}")
        self.lbl_active_tasks.setStyleSheet("color: #9AA0B2; font-style: italic;")
        task_layout.addWidget(self.lbl_active_tasks)
        layout.addWidget(self.task_group)

        layout.addStretch()
        scroll.setWidget(container)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _create_stat_card_widget(self, title: str, value: str, subtitle: str):
        card = QFrame()
        card.setObjectName("card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(4)

        lbl_t = QLabel(title)
        lbl_t.setStyleSheet("color: #9AA0B2; font-size: 11px; font-weight: 600;")
        lbl_v = QLabel(value)
        lbl_v.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: bold;")
        lbl_s = QLabel(subtitle)
        lbl_s.setStyleSheet("color: #E02235; font-size: 11px;")

        lay.addWidget(lbl_t)
        lay.addWidget(lbl_v)
        lay.addWidget(lbl_s)
        return card, lbl_t, lbl_v, lbl_s

    def _update_edu_text(self):
        self.edu_content.setText(
            f"<b>{i18n.tr('dash_edu_1_title')}:</b> {i18n.tr('dash_edu_1')}<br/><br/>"
            f"<b>{i18n.tr('dash_edu_2_title')}:</b> {i18n.tr('dash_edu_2')}<br/><br/>"
            f"<b>{i18n.tr('dash_edu_3_title')}:</b> {i18n.tr('dash_edu_3')}"
        )

    def retranslate_ui(self):
        """Update all text on the dashboard upon language switch."""
        self.lbl_slogan.setText(f"{i18n.tr('app_subtitle')} — {i18n.tr('brand_tagline')}")

        self.lbl_os_t.setText(i18n.tr("dash_os_label"))
        self.lbl_py_t.setText(i18n.tr("dash_python_ver"))
        self.lbl_eng_t.setText(i18n.tr("dash_crypto_status"))
        self.lbl_eng_v.setText(i18n.tr("dash_engine_online"))
        self.lbl_eng_s.setText(i18n.tr("dash_engine_details"))

        self.lbl_hist_t.setText(i18n.tr("dash_history_status"))
        hist_status = (
            i18n.tr("dash_enabled")
            if self.history_service.config_mgr.config.enable_history
            else i18n.tr("dash_disabled")
        )
        self.lbl_hist_v.setText(hist_status)
        op_count = str(self.history_service.count_records())
        self.lbl_hist_s.setText(f"{op_count} {i18n.tr('dash_recorded_suffix')}")

        self.detect_group.setTitle(f"🔍 {i18n.tr('dash_autodetect_title')}")
        self.lbl_detect_desc.setText(i18n.tr("dash_autodetect_desc"))
        self.txt_inspect_in.setPlaceholderText(i18n.tr("dash_inspect_placeholder"))
        self.btn_auto_detect.setText(i18n.tr("btn_auto_detect"))

        self.quick_group.setTitle(i18n.tr("dash_quick_actions"))
        self.btn_enc.setText(f"🔒  {i18n.tr('nav_encryption')}")
        self.btn_hash.setText(f"#️⃣  {i18n.tr('nav_hash')}")
        self.btn_rec.setText(f"🧪  {i18n.tr('nav_recovery')}")
        self.btn_ana.setText(f"📊  {i18n.tr('nav_analyzer')}")

        self.edu_title.setText(f"💡 {i18n.tr('dash_edu_notes')}")
        self._update_edu_text()

        self.task_group.setTitle(i18n.tr("dash_active_tasks"))
        self.lbl_active_tasks.setText(f"🟢 {i18n.tr('dash_no_tasks')}")

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
        self.lbl_hist_v.setText(hist_status)
        self.lbl_hist_s.setText(f"{op_count} {i18n.tr('dash_recorded_suffix')}")
