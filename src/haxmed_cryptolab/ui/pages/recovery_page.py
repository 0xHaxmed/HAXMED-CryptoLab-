"""Module D — Authorized Hash Recovery Lab Page."""

import os

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from haxmed_cryptolab.engines.recovery.rules import RuleConfig
from haxmed_cryptolab.models import RecoveryCandidateMatch
from haxmed_cryptolab.services.recovery_service import RecoveryService
from haxmed_cryptolab.ui.i18n import i18n
from haxmed_cryptolab.ui.widgets.code_display import CodeDisplay
from haxmed_cryptolab.ui.widgets.disclaimer_banner import DisclaimerBanner
from haxmed_cryptolab.workers.recovery_worker import HashRecoveryWorker


class RecoveryPage(QWidget):
    """Authorized Hash Recovery Lab workspace."""

    def __init__(self, recovery_service: RecoveryService, parent=None):
        super().__init__(parent)
        self.recovery_service = recovery_service
        self._worker: HashRecoveryWorker = None
        self._last_match: RecoveryCandidateMatch = None
        self._last_rule_config: RuleConfig = None
        self._wordlist_count = 0
        self._wordlist_path = ""
        self._wordlist_encoding = "utf-8"

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 16, 20, 20)
        main_layout.setSpacing(12)

        self.lbl_title = QLabel(i18n.tr("rec_title"))
        self.lbl_title.setObjectName("section_title")
        main_layout.addWidget(self.lbl_title)

        # Ethical disclaimer banner
        self.banner = DisclaimerBanner(i18n.tr("rec_disclaimer"))
        main_layout.addWidget(self.banner)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        lay = QVBoxLayout(container)
        lay.setSpacing(12)

        # 1. Wordlist Selection & Target Card
        target_card = QFrame()
        target_card.setObjectName("card")
        t_lay = QGridLayout(target_card)
        t_lay.setContentsMargins(14, 12, 14, 12)
        t_lay.setSpacing(10)

        # Wordlist row
        self.lbl_wl_label = QLabel(i18n.tr("rec_wordlist_label"))
        t_lay.addWidget(self.lbl_wl_label, 0, 0)
        self.txt_wordlist_path = QLineEdit()
        self.txt_wordlist_path.setReadOnly(True)
        self.btn_browse_wl = QPushButton(i18n.tr("btn_browse"))
        self.btn_browse_wl.clicked.connect(self._browse_wordlist)
        self.lbl_wl_info = QLabel(i18n.tr("rec_no_wordlist"))
        self.lbl_wl_info.setStyleSheet("color: #E02235; font-size: 11px;")
        t_lay.addWidget(self.txt_wordlist_path, 0, 1)
        t_lay.addWidget(self.btn_browse_wl, 0, 2)
        t_lay.addWidget(self.lbl_wl_info, 0, 3)

        # Adapter / Algorithm
        self.lbl_adapter = QLabel(i18n.tr("rec_adapter_label"))
        t_lay.addWidget(self.lbl_adapter, 1, 0)
        self.combo_adapter = QComboBox()
        self.combo_adapter.addItems(
            [
                "Raw SHA-256 (Hex)",
                "Raw SHA-512 (Hex)",
                "Raw MD5 (Hex)",
                "Raw SHA-1 (Hex)",
                "Bcrypt ($2b$...)",
                "Argon2id ($argon2id$...)",
            ]
        )
        t_lay.addWidget(self.combo_adapter, 1, 1, 1, 3)

        # Target Hash
        self.lbl_target = QLabel(i18n.tr("rec_target_hash"))
        t_lay.addWidget(self.lbl_target, 2, 0)
        self.txt_target_hash = QLineEdit()
        self.txt_target_hash.setPlaceholderText(i18n.tr("rec_target_placeholder"))
        t_lay.addWidget(self.txt_target_hash, 2, 1, 1, 3)

        lay.addWidget(target_card)

        # 2. Transformation Rules Card
        self.rules_group = QGroupBox(i18n.tr("rec_rules_group"))
        r_lay = QGridLayout(self.rules_group)
        r_lay.setContentsMargins(14, 12, 14, 12)
        r_lay.setSpacing(10)

        self.chk_orig = QCheckBox(i18n.tr("rec_rule_orig"))
        self.chk_orig.setChecked(True)
        self.chk_lower = QCheckBox(i18n.tr("rec_rule_lower"))
        self.chk_upper = QCheckBox(i18n.tr("rec_rule_upper"))
        self.chk_cap = QCheckBox(i18n.tr("rec_rule_cap"))

        r_lay.addWidget(self.chk_orig, 0, 0)
        r_lay.addWidget(self.chk_lower, 0, 1)
        r_lay.addWidget(self.chk_upper, 0, 2)
        r_lay.addWidget(self.chk_cap, 0, 3)

        # Prefix / Suffix
        self.lbl_prefix = QLabel(i18n.tr("rec_rule_prefix"))
        r_lay.addWidget(self.lbl_prefix, 1, 0)
        self.txt_prefix = QLineEdit()
        self.txt_prefix.setPlaceholderText(i18n.tr("rec_prefix_placeholder"))
        r_lay.addWidget(self.txt_prefix, 1, 1)

        self.lbl_suffix = QLabel(i18n.tr("rec_rule_suffix"))
        r_lay.addWidget(self.lbl_suffix, 1, 2)
        self.txt_suffix = QLineEdit()
        self.txt_suffix.setPlaceholderText(i18n.tr("rec_suffix_placeholder"))
        r_lay.addWidget(self.txt_suffix, 1, 3)

        # Numeric Suffix Bounded Range
        self.lbl_num_range = QLabel(i18n.tr("rec_rule_num_end"))
        r_lay.addWidget(self.lbl_num_range, 2, 0)
        self.spin_num_range = QSpinBox()
        self.spin_num_range.setRange(0, 9999)
        self.spin_num_range.setValue(0)
        self.spin_num_range.setToolTip("0 = disabled. 99 = append numbers from 0 to 99")
        r_lay.addWidget(self.spin_num_range, 2, 1)

        lay.addWidget(self.rules_group)

        # 3. Execution Control & Progress Card
        prog_card = QFrame()
        prog_card.setObjectName("card")
        p_lay = QVBoxLayout(prog_card)
        p_lay.setContentsMargins(14, 12, 14, 12)
        p_lay.setSpacing(10)

        btn_bar = QHBoxLayout()
        self.btn_start = QPushButton(f"▶ {i18n.tr('btn_start')}")
        self.btn_start.setObjectName("primary_btn")
        self.btn_start.clicked.connect(self._start_recovery)

        self.btn_cancel = QPushButton(f"⏹ {i18n.tr('btn_cancel')}")
        self.btn_cancel.setObjectName("danger_btn")
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.clicked.connect(self._cancel_recovery)

        self.btn_export_report = QPushButton(f"📄 {i18n.tr('btn_export')}")
        self.btn_export_report.setEnabled(False)
        self.btn_export_report.clicked.connect(self._export_report)

        btn_bar.addWidget(self.btn_start)
        btn_bar.addWidget(self.btn_cancel)
        btn_bar.addWidget(self.btn_export_report)
        btn_bar.addStretch()
        p_lay.addLayout(btn_bar)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        p_lay.addWidget(self.progress_bar)

        self.lbl_prog_status = QLabel(i18n.tr("rec_status_idle"))
        self.lbl_prog_status.setStyleSheet("color: #8C90A0;")
        p_lay.addWidget(self.lbl_prog_status)

        lay.addWidget(prog_card)

        # 4. Result Display Card
        self.display_result = CodeDisplay(
            i18n.tr("rec_results_title"), read_only=True
        )
        lay.addWidget(self.display_result)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _browse_wordlist(self):
        path, _ = QFileDialog.getOpenFileName(
            self, i18n.tr("rec_wordlist_label"), "", "Wordlists (*.txt);;All Files (*)"
        )
        if path:
            try:
                count, samples, enc = self.recovery_service.inspect_wordlist(path)
                self._wordlist_count = count
                self._wordlist_path = path
                self._wordlist_encoding = enc
                self.txt_wordlist_path.setText(path)
                self.lbl_wl_info.setText(f"{count:,} {i18n.tr('rec_words_loaded')} ({enc})")
                self.lbl_wl_info.setStyleSheet("color: #28A745; font-size: 11px;")
            except Exception as e:
                QMessageBox.critical(self, "Wordlist Error", str(e))

    def _start_recovery(self):
        target = self.txt_target_hash.text().strip()
        if not target:
            QMessageBox.warning(self, "Validation Error", "Please provide a target hash.")
            return
        if not self._wordlist_path or not os.path.exists(self._wordlist_path):
            QMessageBox.warning(self, "Validation Error", "Please select a valid wordlist file.")
            return

        adapter_text = self.combo_adapter.currentText()
        if "SHA-256" in adapter_text:
            adapter = self.recovery_service.get_adapter("raw", "SHA-256")
        elif "SHA-512" in adapter_text:
            adapter = self.recovery_service.get_adapter("raw", "SHA-512")
        elif "MD5" in adapter_text:
            adapter = self.recovery_service.get_adapter("raw", "MD5")
        elif "SHA-1" in adapter_text:
            adapter = self.recovery_service.get_adapter("raw", "SHA-1")
        elif "Bcrypt" in adapter_text:
            adapter = self.recovery_service.get_adapter("bcrypt")
        elif "Argon2" in adapter_text:
            adapter = self.recovery_service.get_adapter("argon2")
        else:
            adapter = self.recovery_service.get_adapter("raw", "SHA-256")

        try:
            adapter.validate_target(target)
        except Exception as e:
            QMessageBox.warning(self, "Target Format Error", str(e))
            return

        rule_config = RuleConfig(
            apply_original=self.chk_orig.isChecked(),
            apply_lowercase=self.chk_lower.isChecked(),
            apply_uppercase=self.chk_upper.isChecked(),
            apply_capitalize=self.chk_cap.isChecked(),
            prefix=self.txt_prefix.text().strip() or None,
            suffix=self.txt_suffix.text().strip() or None,
            append_numeric_range_end=self.spin_num_range.value(),
        )
        self._last_rule_config = rule_config

        self.btn_start.setEnabled(False)
        self.btn_cancel.setEnabled(True)
        self.btn_export_report.setEnabled(False)
        self.display_result.clear()
        self.progress_bar.setValue(0)
        self.lbl_prog_status.setText(i18n.tr("rec_status_running"))

        self._worker = HashRecoveryWorker(
            wordlist_path=self._wordlist_path,
            target_hash=target,
            adapter=adapter,
            rule_config=rule_config,
            total_base_candidates=self._wordlist_count,
            encoding=self._wordlist_encoding,
        )
        self._worker.progress_signal.connect(self._on_worker_progress)
        self._worker.match_found_signal.connect(self._on_match_found)
        self._worker.finished_signal.connect(self._on_worker_finished)
        self._worker.error_signal.connect(self._on_worker_error)
        self._worker.start()

    def _cancel_recovery(self):
        if self._worker and self._worker.isRunning():
            self._worker.cancel()
            self.lbl_prog_status.setText(i18n.tr("rec_cancelling"))
            self.btn_cancel.setEnabled(False)

    def _on_worker_progress(self, attempts: int, total_base: int, rate: float):
        if total_base > 0:
            pct = min(100, int((attempts / total_base) * 100))
            self.progress_bar.setValue(pct)
        self.lbl_prog_status.setText(
            f"Evaluated {attempts:,} candidates ({rate:,.1f} {i18n.tr('rec_speed_unit')})"
        )

    def _on_match_found(self, match: RecoveryCandidateMatch):
        self._last_match = match
        out_msg = (
            "===========================================================\n"
            "   [+] MATCH VERIFIED: TARGET CANDIDATE IDENTIFIED\n"
            "===========================================================\n"
            f"Plaintext Candidate:  {match.plaintext}\n"
            f"Target Hash:          {match.target_hash}\n"
            f"Attempts Evaluated:   {match.attempts_evaluated:,}\n"
            f"Time Elapsed:         {match.time_elapsed_seconds:.3f} seconds\n"
            "==========================================================="
        )
        self.display_result.set_text(out_msg)

    def _on_worker_finished(self, match, total_attempts: int, elapsed_sec: float):
        self.btn_start.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        self.btn_export_report.setEnabled(True)
        self.progress_bar.setValue(100)

        if match:
            self.lbl_prog_status.setText(
                f"🎉 {i18n.tr('rec_status_matched')} ({total_attempts:,} attempts in {elapsed_sec:.2f}s)"
            )
        else:
            self._last_match = None
            self.lbl_prog_status.setText(
                f"⚠️ {i18n.tr('rec_status_nomatch')} ({total_attempts:,} attempts in {elapsed_sec:.2f}s)"
            )
            self.display_result.set_text(
                f"Search exhausted {total_attempts:,} candidate permutations across {elapsed_sec:.2f} seconds.\n"
                "No candidate matched the supplied target hash."
            )

    def _on_worker_error(self, err_msg: str):
        self.btn_start.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        self.lbl_prog_status.setText(f"Error: {err_msg}")
        QMessageBox.critical(self, "Recovery Task Error", err_msg)

    def _export_report(self):
        target = self.txt_target_hash.text().strip()
        adapter_name = self.combo_adapter.currentText()
        wl_name = os.path.basename(self._wordlist_path)

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Sanitized Recovery Report",
            "recovery_report.txt",
            "Text Report (*.txt);;JSON Report (*.json)",
        )
        if path:
            fmt = "json" if path.endswith(".json") else "txt"
            report_str = self.recovery_service.generate_sanitized_report(
                target_hash=target,
                adapter_name=adapter_name,
                wordlist_name=wl_name,
                total_evaluated=self._worker.total_base_candidates if self._worker else 0,
                elapsed_seconds=self._last_match.time_elapsed_seconds if self._last_match else 0.0,
                match=self._last_match,
                rule_config=self._last_rule_config or RuleConfig(),
                format_type=fmt,
            )
            with open(path, "w", encoding="utf-8") as f:
                f.write(report_str)
            QMessageBox.information(self, "Export Complete", f"Report saved to {path}")

    def retranslate_ui(self):
        """Update all text elements when interface language is toggled."""
        self.lbl_title.setText(i18n.tr("rec_title"))
        self.banner.set_text(i18n.tr("rec_disclaimer"))
        self.lbl_wl_label.setText(i18n.tr("rec_wordlist_label"))
        self.btn_browse_wl.setText(i18n.tr("btn_browse"))
        if not self._wordlist_path:
            self.lbl_wl_info.setText(i18n.tr("rec_no_wordlist"))
        else:
            self.lbl_wl_info.setText(
                f"{self._wordlist_count:,} {i18n.tr('rec_words_loaded')} ({self._wordlist_encoding})"
            )
        self.lbl_adapter.setText(i18n.tr("rec_adapter_label"))
        self.lbl_target.setText(i18n.tr("rec_target_hash"))
        self.txt_target_hash.setPlaceholderText(i18n.tr("rec_target_placeholder"))
        self.rules_group.setTitle(i18n.tr("rec_rules_group"))
        self.chk_orig.setText(i18n.tr("rec_rule_orig"))
        self.chk_lower.setText(i18n.tr("rec_rule_lower"))
        self.chk_upper.setText(i18n.tr("rec_rule_upper"))
        self.chk_cap.setText(i18n.tr("rec_rule_cap"))
        self.lbl_prefix.setText(i18n.tr("rec_rule_prefix"))
        self.txt_prefix.setPlaceholderText(i18n.tr("rec_prefix_placeholder"))
        self.lbl_suffix.setText(i18n.tr("rec_rule_suffix"))
        self.txt_suffix.setPlaceholderText(i18n.tr("rec_suffix_placeholder"))
        self.lbl_num_range.setText(i18n.tr("rec_rule_num_end"))
        self.btn_start.setText(f"▶ {i18n.tr('btn_start')}")
        self.btn_cancel.setText(f"⏹ {i18n.tr('btn_cancel')}")
        self.btn_export_report.setText(f"📄 {i18n.tr('btn_export')}")
        if self._worker is None:
            self.lbl_prog_status.setText(i18n.tr("rec_status_idle"))
        self.display_result.set_label(i18n.tr("rec_results_title"))
        self.display_result.retranslate_ui()
