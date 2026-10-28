"""Module B — Encryption Studio Page."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from haxmed_cryptolab.engines.analysis.detector import SmartDetector
from haxmed_cryptolab.engines.classical.caesar import CaesarCipher
from haxmed_cryptolab.models import DetectedCategory
from haxmed_cryptolab.services.crypto_service import CryptoService
from haxmed_cryptolab.ui.i18n import i18n
from haxmed_cryptolab.ui.widgets.code_display import CodeDisplay
from haxmed_cryptolab.ui.widgets.disclaimer_banner import DisclaimerBanner


class EncryptionPage(QWidget):
    """Complete Encryption Studio for classical and modern ciphers."""

    def __init__(self, crypto_service: CryptoService, parent=None):
        super().__init__(parent)
        self.crypto_service = crypto_service

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 16, 20, 20)
        main_layout.setSpacing(12)

        # Header Title
        self.lbl_title = QLabel(i18n.tr("nav_encryption"))
        self.lbl_title.setObjectName("section_title")
        main_layout.addWidget(self.lbl_title)

        # Tabs for Classical vs Modern
        self.tabs = QTabWidget()
        self.tab_classical = self._create_classical_tab()
        self.tab_modern = self._create_modern_tab()

        self.tabs.addTab(self.tab_classical, i18n.tr("enc_tab_classical"))
        self.tabs.addTab(self.tab_modern, i18n.tr("enc_tab_modern"))
        main_layout.addWidget(self.tabs)

    # -------------------------------------------------------------
    # CLASSICAL CIPHERS WORKSPACE
    # -------------------------------------------------------------
    def _create_classical_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Educational Warning Banner
        self.banner_classical = DisclaimerBanner(i18n.tr("enc_warning_classical"))
        layout.addWidget(self.banner_classical)

        # Control Card
        ctrl_card = QFrame()
        ctrl_card.setObjectName("card")
        ctrl_layout = QVBoxLayout(ctrl_card)
        ctrl_layout.setContentsMargins(14, 12, 14, 12)
        ctrl_layout.setSpacing(10)

        # Row 1: Algorithm & Parameters
        row1 = QHBoxLayout()
        row1.setSpacing(8)
        self.lbl_class_algo = QLabel(i18n.tr("enc_algo_label"))
        self.combo_classical = QComboBox()
        self._populate_classical_combos()
        self.combo_classical.currentIndexChanged.connect(self._on_classical_algo_changed)

        self.lbl_class_key = QLabel(i18n.tr("enc_shift_label"))
        self.txt_class_key = QLineEdit("3")
        self.txt_class_key.setPlaceholderText(i18n.tr("enc_shift_placeholder"))
        self.txt_class_key.setMinimumWidth(110)

        self.btn_caesar_bf = QPushButton(i18n.tr("enc_caesar_bf_btn"))
        self.btn_caesar_bf.clicked.connect(self._show_caesar_bruteforce)

        row1.addWidget(self.lbl_class_algo)
        row1.addWidget(self.combo_classical)
        row1.addSpacing(10)
        row1.addWidget(self.lbl_class_key)
        row1.addWidget(self.txt_class_key)
        row1.addSpacing(10)
        row1.addWidget(self.btn_caesar_bf)
        row1.addStretch()
        ctrl_layout.addLayout(row1)

        # Row 2: Action Buttons
        row2 = QHBoxLayout()
        row2.setSpacing(8)
        self.btn_class_encrypt = QPushButton(i18n.tr("btn_encrypt"))
        self.btn_class_encrypt.setObjectName("primary_btn")
        self.btn_class_encrypt.clicked.connect(lambda: self._execute_classical(decrypt=False))

        self.btn_class_decrypt = QPushButton(i18n.tr("btn_decrypt"))
        self.btn_class_decrypt.clicked.connect(lambda: self._execute_classical(decrypt=True))

        self.btn_class_import = QPushButton(i18n.tr("btn_import"))
        self.btn_class_import.clicked.connect(self._import_classical_text)

        row2.addWidget(self.btn_class_encrypt)
        row2.addWidget(self.btn_class_decrypt)
        row2.addWidget(self.btn_class_import)
        row2.addStretch()
        ctrl_layout.addLayout(row2)

        layout.addWidget(ctrl_card)

        # Splitter for Input and Output
        splitter = QSplitter(Qt.Vertical)

        # Input Box
        in_frame = QFrame()
        in_frame.setObjectName("card")
        in_layout = QVBoxLayout(in_frame)
        in_layout.setContentsMargins(12, 10, 12, 10)
        in_layout.setSpacing(8)

        in_hdr = QHBoxLayout()
        self.lbl_class_in = QLabel(i18n.tr("enc_input_label"))
        self.lbl_class_in.setStyleSheet("font-weight: 600; color: #E02235;")
        self.btn_detect_class = QPushButton(i18n.tr("btn_auto_detect"))
        self.btn_detect_class.clicked.connect(self._auto_detect_classical_input)
        in_hdr.addWidget(self.lbl_class_in)
        in_hdr.addStretch()
        in_hdr.addWidget(self.btn_detect_class)
        in_layout.addLayout(in_hdr)

        self.txt_class_in = QPlainTextEdit()
        self.txt_class_in.setPlaceholderText(i18n.tr("enc_input_placeholder"))
        in_layout.addWidget(self.txt_class_in)

        # Output Box
        self.display_class_out = CodeDisplay(i18n.tr("enc_output_label"), read_only=True)

        splitter.addWidget(in_frame)
        splitter.addWidget(self.display_class_out)
        layout.addWidget(splitter)

        return widget

    def _populate_classical_combos(self):
        curr_key = self.combo_classical.currentData() if hasattr(self, "combo_classical") and self.combo_classical.count() > 0 else "caesar"
        self.combo_classical.blockSignals(True)
        self.combo_classical.clear()
        self.combo_classical.addItem(i18n.tr("enc_algo_caesar"), "caesar")
        self.combo_classical.addItem(i18n.tr("enc_algo_atbash"), "atbash")
        self.combo_classical.addItem(i18n.tr("enc_algo_vigenere"), "vigenere")
        self.combo_classical.addItem(i18n.tr("enc_algo_substitution"), "substitution")
        self.combo_classical.addItem(i18n.tr("enc_algo_transposition"), "transposition")

        idx = self.combo_classical.findData(curr_key)
        if idx >= 0:
            self.combo_classical.setCurrentIndex(idx)
        self.combo_classical.blockSignals(False)

    def _on_classical_algo_changed(self, idx: int):
        algo_key = self.combo_classical.currentData()
        if algo_key == "caesar":
            self.lbl_class_key.setVisible(True)
            self.txt_class_key.setVisible(True)
            self.lbl_class_key.setText(i18n.tr("enc_shift_label"))
            self.txt_class_key.setText("3")
            self.txt_class_key.setPlaceholderText(i18n.tr("enc_shift_placeholder"))
            self.btn_caesar_bf.setVisible(True)
        elif algo_key == "atbash":
            self.lbl_class_key.setVisible(False)
            self.txt_class_key.setVisible(False)
            self.btn_caesar_bf.setVisible(False)
        elif algo_key == "vigenere":
            self.lbl_class_key.setVisible(True)
            self.txt_class_key.setVisible(True)
            self.lbl_class_key.setText(i18n.tr("enc_key_keyword"))
            self.txt_class_key.setText("KEYWORD")
            self.txt_class_key.setPlaceholderText(i18n.tr("enc_key_keyword_ph"))
            self.btn_caesar_bf.setVisible(False)
        elif algo_key == "substitution":
            self.lbl_class_key.setVisible(True)
            self.txt_class_key.setVisible(True)
            self.lbl_class_key.setText(i18n.tr("enc_key_alphabet"))
            self.txt_class_key.setText("QWERTYUIOPASDFGHJKLZXCVBNM")
            self.txt_class_key.setPlaceholderText(i18n.tr("enc_key_alphabet_ph"))
            self.btn_caesar_bf.setVisible(False)
        elif algo_key == "transposition":
            self.lbl_class_key.setVisible(True)
            self.txt_class_key.setVisible(True)
            self.lbl_class_key.setText(i18n.tr("enc_key_columns"))
            self.txt_class_key.setText("5")
            self.txt_class_key.setPlaceholderText(i18n.tr("enc_key_columns_ph"))
            self.btn_caesar_bf.setVisible(False)

    def _execute_classical(self, decrypt: bool = False):
        algo_key = self.combo_classical.currentData()
        text = self.txt_class_in.toPlainText()
        key_val = self.txt_class_key.text()

        if not text.strip():
            QMessageBox.warning(self, "Validation Error", "Please provide input text.")
            return

        res = None
        if algo_key == "caesar":
            try:
                shift = int(key_val.strip())
                res = self.crypto_service.process_caesar(text, shift, decrypt=decrypt)
            except ValueError:
                QMessageBox.warning(self, "Validation Error", "Caesar shift must be an integer.")
                return
        elif algo_key == "atbash":
            res = self.crypto_service.process_atbash(text)
        elif algo_key == "vigenere":
            res = self.crypto_service.process_vigenere(text, key_val, decrypt=decrypt)
        elif algo_key == "substitution":
            res = self.crypto_service.process_substitution(text, key_val, decrypt=decrypt)
        elif algo_key == "transposition":
            res = self.crypto_service.process_transposition(text, key_val, decrypt=decrypt)

        if res:
            if res.success:
                self.display_class_out.set_text(res.data)
            else:
                QMessageBox.critical(
                    self, "Operation Failed", res.error_message or "An error occurred."
                )

    def _show_caesar_bruteforce(self):
        text = self.txt_class_in.toPlainText()
        if not text.strip():
            QMessageBox.information(
                self, "Caesar Explorer", "Enter ciphertext first to explore shifts."
            )
            return

        candidates = CaesarCipher.brute_force(text)
        dlg = QDialog(self)
        dlg.setWindowTitle(i18n.tr("enc_caesar_explorer_title"))
        dlg.resize(650, 450)
        lay = QVBoxLayout(dlg)

        table = QTableWidget(len(candidates), 2)
        table.setHorizontalHeaderLabels([i18n.tr("enc_caesar_col_shift"), i18n.tr("enc_caesar_col_candidate")])
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        for row, (shift, cand) in enumerate(candidates):
            table.setItem(row, 0, QTableWidgetItem(f"Shift {shift}"))
            table.setItem(row, 1, QTableWidgetItem(cand[:120] + ("..." if len(cand) > 120 else "")))

        lay.addWidget(table)
        btn_close = QPushButton(i18n.tr("btn_close"))
        btn_close.clicked.connect(dlg.accept)
        lay.addWidget(btn_close)
        dlg.exec()

    def _import_classical_text(self):
        path, _ = QFileDialog.getOpenFileName(
            self, i18n.tr("btn_import"), "", "Text Files (*.txt);;All Files (*)"
        )
        if path:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                self.txt_class_in.setPlainText(f.read())

    def _auto_detect_classical_input(self):
        text = self.txt_class_in.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "Auto-Detect", "Please enter or paste text to detect.")
            return

        report = SmartDetector.analyze(text)
        if report.category == DetectedCategory.AES_GCM_CONTAINER:
            self.tabs.setCurrentIndex(1)
            self.modern_tabs.setCurrentIndex(0)
            self.txt_aes_in.setPlainText(text)
            QMessageBox.information(
                self,
                "Auto-Detect: AES-GCM Container",
                f"🎯 {report.summary}\n\nAuto-redirected to Modern AES-GCM workspace.",
            )
        elif report.category in (DetectedCategory.RSA_CIPHERTEXT, DetectedCategory.PEM_KEY):
            self.tabs.setCurrentIndex(1)
            self.modern_tabs.setCurrentIndex(1)
            self.txt_rsa_in.setPlainText(text)
            QMessageBox.information(
                self,
                f"Auto-Detect: {report.suggested_algorithm}",
                f"🎯 {report.summary}\n\nAuto-redirected to Modern RSA-OAEP workspace.",
            )
        elif report.category == DetectedCategory.CAESAR_CIPHER:
            shift = report.metadata.get("shift", 3)
            idx = self.combo_classical.findData("caesar")
            if idx >= 0:
                self.combo_classical.setCurrentIndex(idx)
            self.txt_class_key.setText(str(shift))
            preview = report.metadata.get("preview", "")
            QMessageBox.information(
                self,
                "Auto-Detect: Caesar Cipher",
                f"🎯 {report.summary}\n\nConfidence: {report.confidence}\n"
                f"Candidate Plaintext Preview:\n'{preview[:100]}'\n\n"
                f"Shift has been automatically set to {shift}. Click 'Decrypt' to decrypt full text.",
            )
        elif report.category == DetectedCategory.CLASSICAL_SUBSTITUTION:
            idx = self.combo_classical.findData("substitution")
            if idx >= 0:
                self.combo_classical.setCurrentIndex(idx)
            QMessageBox.information(
                self,
                "Auto-Detect: Substitution Cipher",
                f"🎯 {report.summary}\n\n{report.details}",
            )
        elif report.category == DetectedCategory.POLYALPHABETIC_CIPHER:
            idx = self.combo_classical.findData("vigenere")
            if idx >= 0:
                self.combo_classical.setCurrentIndex(idx)
            QMessageBox.information(
                self,
                "Auto-Detect: Polyalphabetic Cipher",
                f"🎯 {report.summary}\n\n{report.details}",
            )
        elif report.category == DetectedCategory.HASH:
            QMessageBox.information(
                self,
                "Auto-Detect: Hash Digest",
                f"🎯 {report.summary}\n\nThis is a one-way hash digest ({report.suggested_algorithm}), not an encryption ciphertext. You can analyze it in the Hash Workbench.",
            )
        else:
            QMessageBox.information(
                self,
                "Auto-Detect Result",
                f"{report.summary}\n\n{report.details}",
            )

    # -------------------------------------------------------------
    # MODERN CRYPTOGRAPHY WORKSPACE
    # -------------------------------------------------------------
    def _create_modern_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        self.modern_tabs = QTabWidget()
        self.modern_tabs.addTab(self._create_aes_subtab(), i18n.tr("enc_modern_aes_tab"))
        self.modern_tabs.addTab(self._create_rsa_oaep_subtab(), i18n.tr("enc_modern_rsa_oaep_tab"))
        self.modern_tabs.addTab(self._create_rsa_pss_subtab(), i18n.tr("enc_modern_rsa_pss_tab"))

        layout.addWidget(self.modern_tabs)
        return widget

    def _create_aes_subtab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(10)

        self.key_box_aes = QGroupBox(i18n.tr("enc_aes_key_info"))
        kb_lay = QHBoxLayout(self.key_box_aes)
        self.txt_aes_key = QLineEdit()
        self.txt_aes_key.setPlaceholderText("64 hexadecimal characters (e.g. generated key)")
        self.btn_gen_aes = QPushButton(i18n.tr("btn_generate_key"))
        self.btn_gen_aes.clicked.connect(self._gen_aes_key)
        kb_lay.addWidget(self.txt_aes_key)
        kb_lay.addWidget(self.btn_gen_aes)
        lay.addWidget(self.key_box_aes)

        # Optional AAD
        aad_box = QHBoxLayout()
        self.lbl_aes_aad = QLabel(i18n.tr("enc_aes_aad_label"))
        aad_box.addWidget(self.lbl_aes_aad)
        self.txt_aes_aad = QLineEdit()
        self.txt_aes_aad.setPlaceholderText(i18n.tr("enc_aes_aad_placeholder"))
        aad_box.addWidget(self.txt_aes_aad)
        lay.addLayout(aad_box)

        # Buttons
        btn_row = QHBoxLayout()
        self.btn_aes_enc = QPushButton(i18n.tr("btn_encrypt"))
        self.btn_aes_enc.setObjectName("primary_btn")
        self.btn_aes_enc.clicked.connect(self._encrypt_aes)
        self.btn_aes_dec = QPushButton(i18n.tr("btn_decrypt"))
        self.btn_aes_dec.clicked.connect(self._decrypt_aes)
        btn_row.addWidget(self.btn_aes_enc)
        btn_row.addWidget(self.btn_aes_dec)
        btn_row.addStretch()
        lay.addLayout(btn_row)

        splitter = QSplitter(Qt.Vertical)
        in_f = QFrame()
        in_f.setObjectName("card")
        in_l = QVBoxLayout(in_f)

        in_hdr = QHBoxLayout()
        self.lbl_aes_in = QLabel(i18n.tr("enc_aes_in_label"))
        self.btn_detect_aes = QPushButton(i18n.tr("btn_auto_detect"))
        self.btn_detect_aes.clicked.connect(self._auto_detect_aes_input)
        in_hdr.addWidget(self.lbl_aes_in)
        in_hdr.addStretch()
        in_hdr.addWidget(self.btn_detect_aes)
        in_l.addLayout(in_hdr)

        self.txt_aes_in = QPlainTextEdit()
        in_l.addWidget(self.txt_aes_in)

        self.display_aes_out = CodeDisplay(i18n.tr("enc_aes_out_label"))
        splitter.addWidget(in_f)
        splitter.addWidget(self.display_aes_out)
        lay.addWidget(splitter)

        return w

    def _auto_detect_aes_input(self):
        text = self.txt_aes_in.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "Auto-Detect", "Please enter or paste data to detect.")
            return
        report = SmartDetector.analyze(text)
        QMessageBox.information(
            self,
            "Auto-Detect Result",
            f"🎯 {report.suggested_algorithm} [{report.confidence} CONFIDENCE]\n\n"
            f"{report.summary}\n\n{report.details}",
        )

    def _gen_aes_key(self):
        key = self.crypto_service.generate_aes_key()
        self.txt_aes_key.setText(key)

    def _encrypt_aes(self):
        pt = self.txt_aes_in.toPlainText()
        key = self.txt_aes_key.text()
        aad = self.txt_aes_aad.text()
        if not pt:
            QMessageBox.warning(self, "Input Error", "Please provide plaintext.")
            return
        if not key:
            QMessageBox.warning(self, "Key Error", "Please generate or provide an AES-256 hex key.")
            return
        res = self.crypto_service.encrypt_aes_gcm(pt, key, aad)
        if res.success:
            self.display_aes_out.set_text(res.data)
        else:
            QMessageBox.critical(self, "Encryption Failed", res.error_message)

    def _decrypt_aes(self):
        container = self.txt_aes_in.toPlainText()
        key = self.txt_aes_key.text()
        if not container:
            QMessageBox.warning(
                self, "Input Error", "Please provide the JSON container envelope to decrypt."
            )
            return
        if not key:
            QMessageBox.warning(self, "Key Error", "Please provide the secret AES-256 key.")
            return
        res = self.crypto_service.decrypt_aes_gcm(container, key)
        if res.success:
            self.display_aes_out.set_text(res.data)
        else:
            QMessageBox.critical(
                self, "Decryption Failed (Authentication Error)", res.error_message
            )

    def _create_rsa_oaep_subtab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(10)

        # Warning
        self.banner_rsa = DisclaimerBanner(i18n.tr("enc_rsa_size_limit"))
        lay.addWidget(self.banner_rsa)

        # Keygen row
        kg_card = QFrame()
        kg_card.setObjectName("card")
        kg_lay = QHBoxLayout(kg_card)
        self.lbl_rsa_keysize = QLabel(i18n.tr("enc_rsa_keysize_label"))
        kg_lay.addWidget(self.lbl_rsa_keysize)
        self.spin_rsa_size = QComboBox()
        self.spin_rsa_size.addItems(["2048", "3072", "4096"])
        self.btn_gen_rsa = QPushButton(i18n.tr("btn_generate_key"))
        self.btn_gen_rsa.clicked.connect(self._gen_rsa_keys)
        kg_lay.addWidget(self.spin_rsa_size)
        kg_lay.addWidget(self.btn_gen_rsa)
        kg_lay.addStretch()
        lay.addWidget(kg_card)

        # Keys display
        key_splitter = QSplitter(Qt.Horizontal)
        pub_f = QFrame()
        pub_f.setObjectName("card")
        pub_l = QVBoxLayout(pub_f)
        self.lbl_rsa_pub = QLabel(i18n.tr("enc_rsa_pubkey_label"))
        pub_l.addWidget(self.lbl_rsa_pub)
        self.txt_rsa_pub = QPlainTextEdit()
        self.txt_rsa_pub.setPlaceholderText("-----BEGIN PUBLIC KEY-----...")
        pub_l.addWidget(self.txt_rsa_pub)

        priv_f = QFrame()
        priv_f.setObjectName("card")
        priv_l = QVBoxLayout(priv_f)
        self.lbl_rsa_priv = QLabel(i18n.tr("enc_rsa_privkey_label"))
        priv_l.addWidget(self.lbl_rsa_priv)
        self.txt_rsa_priv = QPlainTextEdit()
        self.txt_rsa_priv.setPlaceholderText("-----BEGIN PRIVATE KEY-----...")
        priv_l.addWidget(self.txt_rsa_priv)

        key_splitter.addWidget(pub_f)
        key_splitter.addWidget(priv_f)
        lay.addWidget(key_splitter)

        # Action buttons
        btn_row = QHBoxLayout()
        self.btn_rsa_enc = QPushButton(i18n.tr("btn_encrypt"))
        self.btn_rsa_enc.setObjectName("primary_btn")
        self.btn_rsa_enc.clicked.connect(self._encrypt_rsa)
        self.btn_rsa_dec = QPushButton(i18n.tr("btn_decrypt"))
        self.btn_rsa_dec.clicked.connect(self._decrypt_rsa)
        btn_row.addWidget(self.btn_rsa_enc)
        btn_row.addWidget(self.btn_rsa_dec)
        btn_row.addStretch()
        lay.addLayout(btn_row)

        # Splitter for text in/out
        data_splitter = QSplitter(Qt.Vertical)
        in_f = QFrame()
        in_f.setObjectName("card")
        in_l = QVBoxLayout(in_f)
        self.lbl_rsa_in = QLabel(i18n.tr("enc_rsa_in_label"))
        in_l.addWidget(self.lbl_rsa_in)
        self.txt_rsa_in = QPlainTextEdit()
        in_l.addWidget(self.txt_rsa_in)

        self.display_rsa_out = CodeDisplay(i18n.tr("enc_rsa_out_label"))
        data_splitter.addWidget(in_f)
        data_splitter.addWidget(self.display_rsa_out)
        lay.addWidget(data_splitter)

        return w

    def _gen_rsa_keys(self):
        size = int(self.spin_rsa_size.currentText())
        priv, pub = self.crypto_service.generate_rsa_keypair(size)
        self.txt_rsa_priv.setPlainText(priv)
        self.txt_rsa_pub.setPlainText(pub)
        if hasattr(self, "txt_pss_priv"):
            self.txt_pss_priv.setPlainText(priv)
        if hasattr(self, "txt_pss_pub"):
            self.txt_pss_pub.setPlainText(pub)

    def _encrypt_rsa(self):
        pt = self.txt_rsa_in.toPlainText()
        pub = self.txt_rsa_pub.toPlainText()
        if not pt:
            QMessageBox.warning(self, "Input Error", "Please provide plaintext.")
            return
        if not pub:
            QMessageBox.warning(self, "Key Error", "Please provide RSA Public Key (PEM).")
            return
        res = self.crypto_service.encrypt_rsa_oaep(pt, pub)
        if res.success:
            self.display_rsa_out.set_text(res.data)
        else:
            QMessageBox.critical(self, "RSA Encryption Failed", res.error_message)

    def _decrypt_rsa(self):
        ct = self.txt_rsa_in.toPlainText()
        priv = self.txt_rsa_priv.toPlainText()
        if not ct:
            QMessageBox.warning(self, "Input Error", "Please provide Base64 ciphertext.")
            return
        if not priv:
            QMessageBox.warning(self, "Key Error", "Please provide RSA Private Key (PEM).")
            return
        res = self.crypto_service.decrypt_rsa_oaep(ct, priv)
        if res.success:
            self.display_rsa_out.set_text(res.data)
        else:
            QMessageBox.critical(self, "RSA Decryption Failed", res.error_message)

    def _create_rsa_pss_subtab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(10)

        self.banner_pss = DisclaimerBanner(i18n.tr("enc_pss_banner"))
        lay.addWidget(self.banner_pss)

        # Message input
        msg_f = QFrame()
        msg_f.setObjectName("card")
        msg_l = QVBoxLayout(msg_f)
        self.lbl_pss_msg = QLabel(i18n.tr("enc_pss_msg_label"))
        msg_l.addWidget(self.lbl_pss_msg)
        self.txt_pss_msg = QPlainTextEdit()
        self.txt_pss_msg.setPlaceholderText(i18n.tr("enc_pss_msg_ph"))
        msg_l.addWidget(self.txt_pss_msg)
        lay.addWidget(msg_f)

        # Key Inputs
        key_splitter = QSplitter(Qt.Horizontal)
        priv_f = QFrame()
        priv_f.setObjectName("card")
        priv_l = QVBoxLayout(priv_f)
        self.lbl_pss_priv = QLabel(i18n.tr("enc_pss_priv_label"))
        priv_l.addWidget(self.lbl_pss_priv)
        self.txt_pss_priv = QPlainTextEdit()
        priv_l.addWidget(self.txt_pss_priv)

        pub_f = QFrame()
        pub_f.setObjectName("card")
        pub_l = QVBoxLayout(pub_f)
        self.lbl_pss_pub = QLabel(i18n.tr("enc_pss_pub_label"))
        pub_l.addWidget(self.lbl_pss_pub)
        self.txt_pss_pub = QPlainTextEdit()
        pub_l.addWidget(self.txt_pss_pub)

        key_splitter.addWidget(priv_f)
        key_splitter.addWidget(pub_f)
        lay.addWidget(key_splitter)

        # Buttons
        btn_row = QHBoxLayout()
        self.btn_pss_sign = QPushButton(i18n.tr("btn_sign"))
        self.btn_pss_sign.setObjectName("primary_btn")
        self.btn_pss_sign.clicked.connect(self._sign_pss)

        self.btn_pss_verify = QPushButton(i18n.tr("btn_verify"))
        self.btn_pss_verify.clicked.connect(self._verify_pss)

        btn_row.addWidget(self.btn_pss_sign)
        btn_row.addWidget(self.btn_pss_verify)
        btn_row.addStretch()
        lay.addLayout(btn_row)

        # Output / Signature Display
        self.display_pss_sig = CodeDisplay(i18n.tr("enc_pss_sig_label"))
        lay.addWidget(self.display_pss_sig)

        return w

    def _sign_pss(self):
        msg = self.txt_pss_msg.toPlainText()
        priv = self.txt_pss_priv.toPlainText()
        if not msg:
            QMessageBox.warning(self, "Input Error", "Please enter message text.")
            return
        if not priv:
            QMessageBox.warning(self, "Key Error", "Please provide RSA Private Key (PEM) to sign.")
            return
        res = self.crypto_service.sign_rsa_pss(msg, priv)
        if res.success:
            self.display_pss_sig.set_text(res.data)
        else:
            QMessageBox.critical(self, "Signature Failed", res.error_message)

    def _verify_pss(self):
        msg = self.txt_pss_msg.toPlainText()
        pub = self.txt_pss_pub.toPlainText()
        sig = self.display_pss_sig.get_text()
        if not msg:
            QMessageBox.warning(self, "Input Error", "Please enter message text.")
            return
        if not pub:
            QMessageBox.warning(self, "Key Error", "Please provide RSA Public Key (PEM).")
            return
        if not sig:
            QMessageBox.warning(
                self, "Signature Error", "Please provide Base64 signature to verify."
            )
            return

        res = self.crypto_service.verify_rsa_pss(msg, sig, pub)
        if res.success:
            QMessageBox.information(self, "Signature Verification", res.data)
        else:
            QMessageBox.warning(self, "Signature Verification", res.data)

    def retranslate_ui(self):
        """Update all text elements when interface language is toggled."""
        self.lbl_title.setText(i18n.tr("nav_encryption"))

        # Main tabs
        self.tabs.setTabText(0, i18n.tr("enc_tab_classical"))
        self.tabs.setTabText(1, i18n.tr("enc_tab_modern"))

        # Classical Tab
        self.banner_classical.set_text(i18n.tr("enc_warning_classical"))
        self.lbl_class_algo.setText(i18n.tr("enc_algo_label"))
        self._populate_classical_combos()
        self._on_classical_algo_changed(self.combo_classical.currentIndex())
        self.btn_caesar_bf.setText(i18n.tr("enc_caesar_bf_btn"))
        self.btn_class_encrypt.setText(i18n.tr("btn_encrypt"))
        self.btn_class_decrypt.setText(i18n.tr("btn_decrypt"))
        self.btn_class_import.setText(i18n.tr("btn_import"))
        self.lbl_class_in.setText(i18n.tr("enc_input_label"))
        self.btn_detect_class.setText(i18n.tr("btn_auto_detect"))
        self.txt_class_in.setPlaceholderText(i18n.tr("enc_input_placeholder"))
        self.display_class_out.set_label(i18n.tr("enc_output_label"))
        self.display_class_out.retranslate_ui()

        # Modern Subtabs
        self.modern_tabs.setTabText(0, i18n.tr("enc_modern_aes_tab"))
        self.modern_tabs.setTabText(1, i18n.tr("enc_modern_rsa_oaep_tab"))
        self.modern_tabs.setTabText(2, i18n.tr("enc_modern_rsa_pss_tab"))

        # AES
        self.key_box_aes.setTitle(i18n.tr("enc_aes_key_info"))
        self.btn_gen_aes.setText(i18n.tr("btn_generate_key"))
        self.lbl_aes_aad.setText(i18n.tr("enc_aes_aad_label"))
        self.txt_aes_aad.setPlaceholderText(i18n.tr("enc_aes_aad_placeholder"))
        self.btn_aes_enc.setText(i18n.tr("btn_encrypt"))
        self.btn_aes_dec.setText(i18n.tr("btn_decrypt"))
        self.lbl_aes_in.setText(i18n.tr("enc_aes_in_label"))
        self.btn_detect_aes.setText(i18n.tr("btn_auto_detect"))
        self.display_aes_out.set_label(i18n.tr("enc_aes_out_label"))
        self.display_aes_out.retranslate_ui()

        # RSA-OAEP
        self.banner_rsa.set_text(i18n.tr("enc_rsa_size_limit"))
        self.lbl_rsa_keysize.setText(i18n.tr("enc_rsa_keysize_label"))
        self.btn_gen_rsa.setText(i18n.tr("btn_generate_key"))
        self.lbl_rsa_pub.setText(i18n.tr("enc_rsa_pubkey_label"))
        self.lbl_rsa_priv.setText(i18n.tr("enc_rsa_privkey_label"))
        self.btn_rsa_enc.setText(i18n.tr("btn_encrypt"))
        self.btn_rsa_dec.setText(i18n.tr("btn_decrypt"))
        self.lbl_rsa_in.setText(i18n.tr("enc_rsa_in_label"))
        self.display_rsa_out.set_label(i18n.tr("enc_rsa_out_label"))
        self.display_rsa_out.retranslate_ui()

        # RSA-PSS
        self.banner_pss.set_text(i18n.tr("enc_pss_banner"))
        self.lbl_pss_msg.setText(i18n.tr("enc_pss_msg_label"))
        self.txt_pss_msg.setPlaceholderText(i18n.tr("enc_pss_msg_ph"))
        self.lbl_pss_priv.setText(i18n.tr("enc_pss_priv_label"))
        self.lbl_pss_pub.setText(i18n.tr("enc_pss_pub_label"))
        self.btn_pss_sign.setText(i18n.tr("btn_sign"))
        self.btn_pss_verify.setText(i18n.tr("btn_verify"))
        self.display_pss_sig.set_label(i18n.tr("enc_pss_sig_label"))
        self.display_pss_sig.retranslate_ui()
