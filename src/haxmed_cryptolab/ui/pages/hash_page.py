"""Module C — Hash Workbench Page."""

from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
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
from haxmed_cryptolab.engines.hashes.identifier import IDENTIFICATION_DISCLAIMER
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

        lbl_title = QLabel(i18n.tr("nav_hash"))
        lbl_title.setObjectName("section_title")
        layout.addWidget(lbl_title)

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
        ctrl_lay = QGridLayout(ctrl_card)

        ctrl_lay.addWidget(QLabel("Algorithm:"), 0, 0)
        self.combo_hash_algo = QComboBox()
        self.combo_hash_algo.addItems(SUPPORTED_HASH_ALGORITHMS)
        self.combo_hash_algo.currentIndexChanged.connect(self._check_legacy_warning)
        ctrl_lay.addWidget(self.combo_hash_algo, 0, 1)

        # Mode Radio
        self.radio_text = QRadioButton(i18n.tr("hash_mode_text"))
        self.radio_file = QRadioButton(i18n.tr("hash_mode_file"))
        self.radio_text.setChecked(True)
        self.radio_text.toggled.connect(self._toggle_input_mode)
        mode_box = QHBoxLayout()
        mode_box.addWidget(self.radio_text)
        mode_box.addWidget(self.radio_file)
        ctrl_lay.addLayout(mode_box, 0, 2)

        # Calculate Button
        self.btn_calc_hash = QPushButton(i18n.tr("btn_calculate"))
        self.btn_calc_hash.setObjectName("primary_btn")
        self.btn_calc_hash.clicked.connect(self._execute_hash_calculation)
        self.btn_cancel_hash = QPushButton(i18n.tr("btn_cancel"))
        self.btn_cancel_hash.setEnabled(False)
        self.btn_cancel_hash.clicked.connect(self._cancel_file_hash)
        btn_h = QHBoxLayout()
        btn_h.addWidget(self.btn_calc_hash)
        btn_h.addWidget(self.btn_cancel_hash)
        ctrl_lay.addLayout(btn_h, 0, 3)

        lay.addWidget(ctrl_card)

        # Legacy warning banner
        self.banner_legacy = DisclaimerBanner(
            "LEGACY ALGORITHM NOTICE: MD5 and SHA-1 are cryptographically broken for collision resistance. "
            "They should only be used for legacy checksum verification, never for security."
        )
        self.banner_legacy.setVisible(False)
        lay.addWidget(self.banner_legacy)

        # Text input card
        self.frame_text_in = QFrame()
        self.frame_text_in.setObjectName("card")
        tin_l = QVBoxLayout(self.frame_text_in)
        tin_l.addWidget(QLabel("Enter Text to Hash:"))
        self.txt_hash_in = QPlainTextEdit()
        tin_l.addWidget(self.txt_hash_in)
        lay.addWidget(self.frame_text_in)

        # File input card
        self.frame_file_in = QFrame()
        self.frame_file_in.setObjectName("card")
        self.frame_file_in.setVisible(False)
        fin_l = QVBoxLayout(self.frame_file_in)
        fin_l.addWidget(QLabel("Target File:"))
        file_row = QHBoxLayout()
        self.txt_file_path = QLineEdit()
        self.txt_file_path.setReadOnly(True)
        btn_browse = QPushButton(i18n.tr("btn_browse"))
        btn_browse.clicked.connect(self._browse_file_for_hash)
        file_row.addWidget(self.txt_file_path)
        file_row.addWidget(btn_browse)
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

        c_lay.addWidget(QLabel(i18n.tr("hash_compare_a")))
        self.txt_cmp_a = QLineEdit()
        self.txt_cmp_a.setPlaceholderText("Hexadecimal digest A")
        c_lay.addWidget(self.txt_cmp_a)

        c_lay.addWidget(QLabel(i18n.tr("hash_compare_b")))
        self.txt_cmp_b = QLineEdit()
        self.txt_cmp_b.setPlaceholderText("Hexadecimal digest B")
        c_lay.addWidget(self.txt_cmp_b)

        btn_row = QHBoxLayout()
        btn_cmp = QPushButton(i18n.tr("btn_compare"))
        btn_cmp.setObjectName("primary_btn")
        btn_cmp.clicked.connect(self._compare_digests)
        btn_row.addWidget(btn_cmp)
        btn_row.addStretch()
        c_lay.addLayout(btn_row)

        lay.addWidget(card)

        # Comparison Result Badge Card
        res_card = QFrame()
        res_card.setObjectName("card")
        res_lay = QVBoxLayout(res_card)
        self.lbl_cmp_status = QLabel("AWAITING INPUT")
        self.lbl_cmp_status.setStyleSheet("font-size: 20px; font-weight: bold; color: #8C90A0;")
        self.lbl_cmp_details = QLabel(
            "Enter two hexadecimal digests to verify equivalence in constant time."
        )
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

        lay.addWidget(DisclaimerBanner(IDENTIFICATION_DISCLAIMER))

        in_card = QFrame()
        in_card.setObjectName("card")
        in_l = QHBoxLayout(in_card)
        self.txt_id_input = QLineEdit()
        self.txt_id_input.setPlaceholderText("Enter hash string (Hex, $2b$..., $argon2id$...)")
        btn_id = QPushButton(i18n.tr("btn_identify"))
        btn_id.setObjectName("primary_btn")
        btn_id.clicked.connect(self._identify_hash)
        in_l.addWidget(self.txt_id_input)
        in_l.addWidget(btn_id)
        lay.addWidget(in_card)

        self.table_id = QTableWidget(0, 4)
        self.table_id.setHorizontalHeaderLabels(
            ["Algorithm", "Bit Length", "Confidence", "Analysis Notes"]
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

        title = QLabel("Understanding Cryptographic Hash Functions")
        title.setObjectName("section_title")
        c_lay.addWidget(title)

        edu_box = QFrame()
        edu_box.setObjectName("card")
        e_lay = QVBoxLayout(edu_box)
        lbl_body = QLabel(i18n.tr("hash_edu_text"))
        lbl_body.setStyleSheet("line-height: 160%; color: #C2C6D2; font-size: 13px;")
        lbl_body.setWordWrap(True)
        e_lay.addWidget(lbl_body)
        c_lay.addWidget(edu_box)

        c_lay.addStretch()
        scroll.setWidget(container)
        lay.addWidget(scroll)
        return w
