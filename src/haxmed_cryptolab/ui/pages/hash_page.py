"""Module C — Hash Workbench Page."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from haxmed_cryptolab.core.constants import LEGACY_INSECURE_HASHES, SUPPORTED_HASH_ALGORITHMS
from haxmed_cryptolab.engines.analysis.detector import SmartDetector
from haxmed_cryptolab.models import DetectedCategory
from haxmed_cryptolab.services.hash_service import HashService
from haxmed_cryptolab.ui.i18n import i18n
from haxmed_cryptolab.ui.widgets.code_display import CodeDisplay
from haxmed_cryptolab.ui.widgets.disclaimer_banner import DisclaimerBanner
from haxmed_cryptolab.workers.file_hash_worker import FileHashWorker


class HashPage(QWidget):
    """Complete Hash Workbench for calculation, comparison, identification, and education."""

    def __init__(self, hash_service: HashService, parent=None):
        super().__init__(parent)
        self.hash_service = hash_service
        self._file_worker: FileHashWorker = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 20)
        layout.setSpacing(12)

        self.lbl_title = QLabel(i18n.tr("nav_hash"))
        self.lbl_title.setObjectName("section_title")
        layout.addWidget(self.lbl_title)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_calc_tab(), i18n.tr("hash_tab_calc"))
        self.tabs.addTab(self._create_compare_tab(), i18n.tr("hash_tab_compare"))
        self.tabs.addTab(self._create_identify_tab(), i18n.tr("hash_tab_identify"))
        self.tabs.addTab(self._create_edu_tab(), i18n.tr("hash_tab_edu"))

        layout.addWidget(self.tabs)

    # -------------------------------------------------------------
    # 1. HASH CALCULATION
    # -------------------------------------------------------------
    def _create_calc_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(10)

        # Control Row
        ctrl_card = QFrame()
        ctrl_card.setObjectName("card")
        ctrl_lay = QVBoxLayout(ctrl_card)
        ctrl_lay.setContentsMargins(14, 12, 14, 12)
        ctrl_lay.setSpacing(10)

        row = QHBoxLayout()
        row.setSpacing(10)
        self.lbl_hash_algo = QLabel(i18n.tr("hash_algo_label"))
        self.combo_hash_algo = QComboBox()
        self.combo_hash_algo.addItems(SUPPORTED_HASH_ALGORITHMS)
        self.combo_hash_algo.currentIndexChanged.connect(self._check_legacy_warning)
        row.addWidget(self.lbl_hash_algo)
        row.addWidget(self.combo_hash_algo)

        row.addSpacing(12)
        self.radio_text = QRadioButton(i18n.tr("hash_mode_text"))
        self.radio_file = QRadioButton(i18n.tr("hash_mode_file"))
        self.radio_text.setChecked(True)
        self.radio_text.toggled.connect(self._toggle_input_mode)
        row.addWidget(self.radio_text)
        row.addWidget(self.radio_file)

        row.addSpacing(12)
        self.btn_calc_hash = QPushButton(i18n.tr("btn_calculate"))
        self.btn_calc_hash.setObjectName("primary_btn")
        self.btn_calc_hash.clicked.connect(self._execute_hash_calculation)
        self.btn_cancel_hash = QPushButton(i18n.tr("btn_cancel"))
        self.btn_cancel_hash.setEnabled(False)
        self.btn_cancel_hash.clicked.connect(self._cancel_file_hash)
        row.addWidget(self.btn_calc_hash)
        row.addWidget(self.btn_cancel_hash)
        row.addStretch()

        ctrl_lay.addLayout(row)
        lay.addWidget(ctrl_card)

        # Legacy warning banner
        self.banner_legacy = DisclaimerBanner(i18n.tr("hash_legacy_warning"))
        self.banner_legacy.setVisible(False)
        lay.addWidget(self.banner_legacy)

        # Text input card
        self.frame_text_in = QFrame()
        self.frame_text_in.setObjectName("card")
        tin_l = QVBoxLayout(self.frame_text_in)

        t_hdr = QHBoxLayout()
        self.lbl_text_prompt = QLabel(i18n.tr("hash_enter_text_prompt"))
        self.btn_detect_hash = QPushButton(i18n.tr("btn_auto_detect"))
        self.btn_detect_hash.clicked.connect(self._auto_detect_hash_input)
        t_hdr.addWidget(self.lbl_text_prompt)
        t_hdr.addStretch()
        t_hdr.addWidget(self.btn_detect_hash)
        tin_l.addLayout(t_hdr)

        self.txt_hash_in = QPlainTextEdit()
        tin_l.addWidget(self.txt_hash_in)
        lay.addWidget(self.frame_text_in)

        # File input card
        self.frame_file_in = QFrame()
        self.frame_file_in.setObjectName("card")
        self.frame_file_in.setVisible(False)
        fin_l = QVBoxLayout(self.frame_file_in)
        self.lbl_file_target = QLabel(i18n.tr("hash_target_file_label"))
        fin_l.addWidget(self.lbl_file_target)
        file_row = QHBoxLayout()
        self.txt_file_path = QLineEdit()
        self.txt_file_path.setReadOnly(True)
        self.btn_browse_file = QPushButton(i18n.tr("btn_browse"))
        self.btn_browse_file.clicked.connect(self._browse_file_for_hash)
        file_row.addWidget(self.txt_file_path)
        file_row.addWidget(self.btn_browse_file)
        fin_l.addLayout(file_row)

        self.progress_file = QProgressBar()
        self.progress_file.setValue(0)
        self.progress_file.setTextVisible(True)
        fin_l.addWidget(self.progress_file)
        lay.addWidget(self.frame_file_in)

        # Digest Output
        self.display_digest = CodeDisplay(i18n.tr("hash_digest_output"), read_only=True)
        lay.addWidget(self.display_digest)

        return w

    def _auto_detect_hash_input(self):
        text = self.txt_hash_in.toPlainText().strip()
        if not text:
            QMessageBox.warning(
                self, "Auto-Detect", "Please enter or paste a hash digest to inspect."
            )
            return

        report = SmartDetector.analyze(text)
        if report.category == DetectedCategory.HASH:
            algo = report.metadata.get("algo")
            if algo:
                idx = self.combo_hash_algo.findText(algo, Qt.MatchContains)
                if idx >= 0:
                    self.combo_hash_algo.setCurrentIndex(idx)
            QMessageBox.information(
                self,
                "Auto-Detect: Hash Recognized",
                f"🎯 {report.suggested_algorithm} [{report.confidence} CONFIDENCE]\n\n"
                f"{report.summary}\n\n{report.details}",
            )
        else:
            QMessageBox.information(
                self,
                "Auto-Detect Result",
                f"🎯 {report.suggested_algorithm} [{report.confidence} CONFIDENCE]\n\n"
                f"{report.summary}\n\n{report.details}",
            )

    def _check_legacy_warning(self):
        algo = self.combo_hash_algo.currentText()
        self.banner_legacy.setVisible(algo in LEGACY_INSECURE_HASHES)

    def _toggle_input_mode(self):
        is_text = self.radio_text.isChecked()
        self.frame_text_in.setVisible(is_text)
        self.frame_file_in.setVisible(not is_text)

    def _browse_file_for_hash(self):
        path, _ = QFileDialog.getOpenFileName(self, i18n.tr("hash_file_select"))
        if path:
            self.txt_file_path.setText(path)

    def _execute_hash_calculation(self):
        algo = self.combo_hash_algo.currentText()
        if self.radio_text.isChecked():
            text = self.txt_hash_in.toPlainText()
            res = self.hash_service.hash_text(text, algo)
            self.display_digest.set_text(res.digest_hex)
        else:
            path = self.txt_file_path.text()
            if not path:
                QMessageBox.warning(self, "Validation Error", "Please select a file to hash.")
                return

            self.btn_calc_hash.setEnabled(False)
            self.btn_cancel_hash.setEnabled(True)
            self.progress_file.setValue(0)

            self._file_worker = FileHashWorker(self.hash_service, path, algo, chunk_size_kb=64)
            self._file_worker.progress_signal.connect(self._on_file_progress)
            self._file_worker.finished_signal.connect(self._on_file_finished)
            self._file_worker.error_signal.connect(self._on_file_error)
            self._file_worker.start()

    def _cancel_file_hash(self):
        if self._file_worker and self._file_worker.isRunning():
            self._file_worker.cancel()
            self.btn_cancel_hash.setEnabled(False)

    def _on_file_progress(self, read_bytes: int, total_bytes: int):
        if total_bytes > 0:
            pct = int((read_bytes / total_bytes) * 100)
            self.progress_file.setValue(pct)

    def _on_file_finished(self, result):
        self.progress_file.setValue(100)
        self.display_digest.set_text(result.digest_hex)
        self.btn_calc_hash.setEnabled(True)
        self.btn_cancel_hash.setEnabled(False)

    def _on_file_error(self, err_msg: str):
        self.btn_calc_hash.setEnabled(True)
        self.btn_cancel_hash.setEnabled(False)
        QMessageBox.critical(self, "Hashing Error", err_msg)

    # -------------------------------------------------------------
    # 2. HASH COMPARISON
    # -------------------------------------------------------------
    def _create_compare_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(12)

        card = QFrame()
        card.setObjectName("card")
        c_lay = QVBoxLayout(card)

        self.lbl_cmp_a = QLabel(i18n.tr("hash_compare_a"))
        c_lay.addWidget(self.lbl_cmp_a)
        self.txt_cmp_a = QLineEdit()
        self.txt_cmp_a.setPlaceholderText("Hexadecimal digest A")
        c_lay.addWidget(self.txt_cmp_a)

        self.lbl_cmp_b = QLabel(i18n.tr("hash_compare_b"))
        c_lay.addWidget(self.lbl_cmp_b)
        self.txt_cmp_b = QLineEdit()
        self.txt_cmp_b.setPlaceholderText("Hexadecimal digest B")
        c_lay.addWidget(self.txt_cmp_b)

        btn_row = QHBoxLayout()
        self.btn_cmp = QPushButton(i18n.tr("btn_compare"))
        self.btn_cmp.setObjectName("primary_btn")
        self.btn_cmp.clicked.connect(self._compare_digests)
        btn_row.addWidget(self.btn_cmp)
        btn_row.addStretch()
        c_lay.addLayout(btn_row)

        lay.addWidget(card)

        # Comparison Result Badge Card
        res_card = QFrame()
        res_card.setObjectName("card")
        res_lay = QVBoxLayout(res_card)
        self.lbl_cmp_status = QLabel(i18n.tr("hash_awaiting_input"))
        self.lbl_cmp_status.setStyleSheet("font-size: 20px; font-weight: bold; color: #8C90A0;")
        self.lbl_cmp_details = QLabel(i18n.tr("hash_cmp_details_prompt"))
        self.lbl_cmp_details.setWordWrap(True)
        res_lay.addWidget(self.lbl_cmp_status)
        res_lay.addWidget(self.lbl_cmp_details)
        lay.addWidget(res_card)

        lay.addStretch()
        return w

    def _compare_digests(self):
        da = self.txt_cmp_a.text()
        db = self.txt_cmp_b.text()
        res = self.hash_service.compare_digests(da, db)

        if res.is_match:
            self.lbl_cmp_status.setText(f"✅ {i18n.tr('hash_match')}")
            self.lbl_cmp_status.setStyleSheet("font-size: 20px; font-weight: bold; color: #28A745;")
        elif res.status_label == "INVALID INPUT":
            self.lbl_cmp_status.setText(f"⚠️ {i18n.tr('hash_invalid_input')}")
            self.lbl_cmp_status.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFC107;")
        else:
            self.lbl_cmp_status.setText(f"❌ {i18n.tr('hash_no_match')}")
            self.lbl_cmp_status.setStyleSheet("font-size: 20px; font-weight: bold; color: #E02235;")

        self.lbl_cmp_details.setText(res.details)

    # -------------------------------------------------------------
    # 3. HASH IDENTIFICATION
    # -------------------------------------------------------------
    def _create_identify_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(12)

        self.banner_id = DisclaimerBanner(i18n.tr("hash_id_disclaimer"))
        lay.addWidget(self.banner_id)

        in_card = QFrame()
        in_card.setObjectName("card")
        in_l = QHBoxLayout(in_card)
        self.txt_id_input = QLineEdit()
        self.txt_id_input.setPlaceholderText("Enter hash string (Hex, $2b$..., $argon2id$...)")
        self.btn_id = QPushButton(i18n.tr("btn_identify"))
        self.btn_id.setObjectName("primary_btn")
        self.btn_id.clicked.connect(self._identify_hash)
        in_l.addWidget(self.txt_id_input)
        in_l.addWidget(self.btn_id)
        lay.addWidget(in_card)

        self.table_id = QTableWidget(0, 4)
        self.table_id.setHorizontalHeaderLabels(
            [
                i18n.tr("hash_col_algo"),
                i18n.tr("hash_col_bits"),
                i18n.tr("hash_col_conf"),
                i18n.tr("hash_col_notes"),
            ]
        )
        self.table_id.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        lay.addWidget(self.table_id)

        return w

    def _identify_hash(self):
        h = self.txt_id_input.text()
        candidates = self.hash_service.identify_format(h)
        self.table_id.setRowCount(len(candidates))

        for row, cand in enumerate(candidates):
            self.table_id.setItem(row, 0, QTableWidgetItem(cand.algorithm))
            self.table_id.setItem(
                row, 1, QTableWidgetItem(str(cand.bit_length) if cand.bit_length else "N/A")
            )
            self.table_id.setItem(row, 2, QTableWidgetItem(cand.confidence))
            self.table_id.setItem(row, 3, QTableWidgetItem(cand.notes))

    # -------------------------------------------------------------
    # 4. HASHING EDUCATION
    # -------------------------------------------------------------
    def _create_edu_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(16, 16, 16, 16)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        c_lay = QVBoxLayout(container)
        c_lay.setSpacing(14)

        self.lbl_edu_title = QLabel(i18n.tr("hash_edu_title"))
        self.lbl_edu_title.setObjectName("section_title")
        c_lay.addWidget(self.lbl_edu_title)

        edu_box = QFrame()
        edu_box.setObjectName("card")
        e_lay = QVBoxLayout(edu_box)
        self.lbl_edu_body = QLabel(i18n.tr("hash_edu_text"))
        self.lbl_edu_body.setStyleSheet("line-height: 160%; color: #C2C6D2; font-size: 13px;")
        self.lbl_edu_body.setWordWrap(True)
        e_lay.addWidget(self.lbl_edu_body)
        c_lay.addWidget(edu_box)

        c_lay.addStretch()
        scroll.setWidget(container)
        lay.addWidget(scroll)
        return w

    def retranslate_ui(self):
        """Update all text elements when interface language is toggled."""
        self.lbl_title.setText(i18n.tr("nav_hash"))
        self.tabs.setTabText(0, i18n.tr("hash_tab_calc"))
        self.tabs.setTabText(1, i18n.tr("hash_tab_compare"))
        self.tabs.setTabText(2, i18n.tr("hash_tab_identify"))
        self.tabs.setTabText(3, i18n.tr("hash_tab_edu"))

        # Tab 1: Calc
        self.lbl_hash_algo.setText(i18n.tr("hash_algo_label"))
        self.radio_text.setText(i18n.tr("hash_mode_text"))
        self.radio_file.setText(i18n.tr("hash_mode_file"))
        self.btn_calc_hash.setText(i18n.tr("btn_calculate"))
        self.btn_cancel_hash.setText(i18n.tr("btn_cancel"))
        self.banner_legacy.set_text(i18n.tr("hash_legacy_warning"))
        self.lbl_text_prompt.setText(i18n.tr("hash_enter_text_prompt"))
        self.btn_detect_hash.setText(i18n.tr("btn_auto_detect"))
        self.lbl_file_target.setText(i18n.tr("hash_target_file_label"))
        self.btn_browse_file.setText(i18n.tr("btn_browse"))
        self.display_digest.set_label(i18n.tr("hash_digest_output"))
        self.display_digest.retranslate_ui()

        # Tab 2: Compare
        self.lbl_cmp_a.setText(i18n.tr("hash_compare_a"))
        self.lbl_cmp_b.setText(i18n.tr("hash_compare_b"))
        self.btn_cmp.setText(i18n.tr("btn_compare"))
        if not self.txt_cmp_a.text() and not self.txt_cmp_b.text():
            self.lbl_cmp_status.setText(i18n.tr("hash_awaiting_input"))
            self.lbl_cmp_details.setText(i18n.tr("hash_cmp_details_prompt"))

        # Tab 3: Identify
        self.banner_id.set_text(i18n.tr("hash_id_disclaimer"))
        self.btn_id.setText(i18n.tr("btn_identify"))
        self.table_id.setHorizontalHeaderLabels(
            [
                i18n.tr("hash_col_algo"),
                i18n.tr("hash_col_bits"),
                i18n.tr("hash_col_conf"),
                i18n.tr("hash_col_notes"),
            ]
        )

        # Tab 4: Education
        self.lbl_edu_title.setText(i18n.tr("hash_edu_title"))
        self.lbl_edu_body.setText(i18n.tr("hash_edu_text"))
