"""Module B — Encryption Studio Page."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QFrame,
    QGridLayout,
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
        lbl_title = QLabel(i18n.tr("nav_encryption"))
        lbl_title.setObjectName("section_title")
        main_layout.addWidget(lbl_title)

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
        banner = DisclaimerBanner(i18n.tr("enc_warning_classical"))
        layout.addWidget(banner)

        # Control Row
        ctrl_card = QFrame()
        ctrl_card.setObjectName("card")
        ctrl_layout = QGridLayout(ctrl_card)
        ctrl_layout.setContentsMargins(12, 10, 12, 10)
        ctrl_layout.setSpacing(10)

        ctrl_layout.addWidget(QLabel(i18n.tr("enc_algo_label")), 0, 0)
        self.combo_classical = QComboBox()
        self.combo_classical.addItems(
            [
                "Caesar Cipher",
                "Atbash Cipher",
                "Vigenère Cipher",
                "Monoalphabetic Substitution",
                "Columnar Transposition",
            ]
        )
        self.combo_classical.currentIndexChanged.connect(self._on_classical_algo_changed)
        ctrl_layout.addWidget(self.combo_classical, 0, 1)

        self.lbl_class_key = QLabel(i18n.tr("enc_shift_label"))
        self.txt_class_key = QLineEdit("3")
        self.txt_class_key.setPlaceholderText("Shift (e.g. 3)")
        ctrl_layout.addWidget(self.lbl_class_key, 0, 2)
        ctrl_layout.addWidget(self.txt_class_key, 0, 3)

        self.btn_caesar_bf = QPushButton(i18n.tr("enc_caesar_bf_btn"))
        self.btn_caesar_bf.clicked.connect(self._show_caesar_bruteforce)
        ctrl_layout.addWidget(self.btn_caesar_bf, 0, 4)

        # Action Buttons
        btn_row = QHBoxLayout()
        self.btn_class_encrypt = QPushButton(i18n.tr("btn_encrypt"))
        self.btn_class_encrypt.setObjectName("primary_btn")
        self.btn_class_encrypt.clicked.connect(lambda: self._execute_classical(decrypt=False))

        self.btn_class_decrypt = QPushButton(i18n.tr("btn_decrypt"))
        self.btn_class_decrypt.clicked.connect(lambda: self._execute_classical(decrypt=True))

        self.btn_class_import = QPushButton(i18n.tr("btn_import"))
        self.btn_class_import.clicked.connect(self._import_classical_text)

        btn_row.addWidget(self.btn_class_encrypt)
        btn_row.addWidget(self.btn_class_decrypt)
        btn_row.addWidget(self.btn_class_import)
        btn_row.addStretch()

        ctrl_layout.addLayout(btn_row, 1, 0, 1, 5)
        layout.addWidget(ctrl_card)

        # Splitter for Input and Output
        splitter = QSplitter(Qt.Vertical)

        # Input Box
        in_frame = QFrame()
        in_frame.setObjectName("card")
        in_layout = QVBoxLayout(in_frame)
        in_layout.setContentsMargins(10, 8, 10, 8)

        in_hdr = QHBoxLayout()
        lbl_in = QLabel(i18n.tr("enc_input_label"))
        lbl_in.setStyleSheet("font-weight: 600; color: #E02235;")
        btn_detect = QPushButton(i18n.tr("btn_auto_detect"))
        btn_detect.clicked.connect(self._auto_detect_classical_input)
        in_hdr.addWidget(lbl_in)
        in_hdr.addStretch()
        in_hdr.addWidget(btn_detect)
        in_layout.addLayout(in_hdr)

        self.txt_class_in = QPlainTextEdit()
        self.txt_class_in.setPlaceholderText("Enter plaintext or ciphertext here...")
        in_layout.addWidget(self.txt_class_in)

        # Output Box
        self.display_class_out = CodeDisplay(i18n.tr("enc_output_label"), read_only=True)

        splitter.addWidget(in_frame)
        splitter.addWidget(self.display_class_out)
        layout.addWidget(splitter)

        return widget

    def _on_classical_algo_changed(self, idx: int):
        algo = self.combo_classical.currentText()
        if "Caesar" in algo:
            self.lbl_class_key.setVisible(True)
            self.txt_class_key.setVisible(True)
            self.lbl_class_key.setText(i18n.tr("enc_shift_label"))
            self.txt_class_key.setText("3")
            self.txt_class_key.setPlaceholderText("Shift 1-25")
            self.btn_caesar_bf.setVisible(True)
        elif "Atbash" in algo:
            self.lbl_class_key.setVisible(False)
            self.txt_class_key.setVisible(False)
            self.btn_caesar_bf.setVisible(False)
        elif "Vigenère" in algo:
            self.lbl_class_key.setVisible(True)
            self.txt_class_key.setVisible(True)
            self.lbl_class_key.setText("Keyword (A-Z):")
            self.txt_class_key.setText("KEYWORD")
            self.txt_class_key.setPlaceholderText("Alphabetic key (e.g. SECRET)")
            self.btn_caesar_bf.setVisible(False)
        elif "Substitution" in algo:
            self.lbl_class_key.setVisible(True)
            self.txt_class_key.setVisible(True)
            self.lbl_class_key.setText("Alphabet Key (26 unique):")
            self.txt_class_key.setText("QWERTYUIOPASDFGHJKLZXCVBNM")
            self.txt_class_key.setPlaceholderText("Permutation of A-Z")
            self.btn_caesar_bf.setVisible(False)
        elif "Transposition" in algo:
            self.lbl_class_key.setVisible(True)
            self.txt_class_key.setVisible(True)
            self.lbl_class_key.setText("Columns (Int >= 2):")
            self.txt_class_key.setText("5")
            self.txt_class_key.setPlaceholderText("Column count")
            self.btn_caesar_bf.setVisible(False)

    def _execute_classical(self, decrypt: bool = False):
        algo = self.combo_classical.currentText()
        text = self.txt_class_in.toPlainText()
        key_val = self.txt_class_key.text()

        if not text.strip():
            QMessageBox.warning(self, "Validation Error", "Please provide input text.")
            return

        res = None
        if "Caesar" in algo:
            try:
                shift = int(key_val.strip())
                res = self.crypto_service.process_caesar(text, shift, decrypt=decrypt)
            except ValueError:
                QMessageBox.warning(self, "Validation Error", "Caesar shift must be an integer.")
                return
        elif "Atbash" in algo:
            res = self.crypto_service.process_atbash(text)
        elif "Vigenère" in algo:
            res = self.crypto_service.process_vigenere(text, key_val, decrypt=decrypt)
        elif "Substitution" in algo:
            res = self.crypto_service.process_substitution(text, key_val, decrypt=decrypt)
        elif "Transposition" in algo:
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
        dlg.setWindowTitle("Caesar Cipher — 25 Shift Brute-Force Explorer")
        dlg.resize(650, 450)
        lay = QVBoxLayout(dlg)

        table = QTableWidget(len(candidates), 2)
        table.setHorizontalHeaderLabels(["Shift (Key)", "Decrypted Candidate Text"])
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        for row, (shift, cand) in enumerate(candidates):
            table.setItem(row, 0, QTableWidgetItem(f"Shift {shift}"))
            table.setItem(row, 1, QTableWidgetItem(cand[:120] + ("..." if len(cand) > 120 else "")))

        lay.addWidget(table)
        btn_close = QPushButton("Close")
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
            self.combo_classical.setCurrentText("Caesar Cipher")
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
            self.combo_classical.setCurrentText("Monoalphabetic Substitution")
            QMessageBox.information(
                self,
                "Auto-Detect: Substitution Cipher",
                f"🎯 {report.summary}\n\n{report.details}",
            )
        elif report.category == DetectedCategory.POLYALPHABETIC_CIPHER:
            self.combo_classical.setCurrentText("Vigenère Cipher")
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
        self.modern_tabs.addTab(self._create_aes_subtab(), "AES-GCM (Authenticated)")
        self.modern_tabs.addTab(self._create_rsa_oaep_subtab(), "RSA-OAEP (Public Key)")
        self.modern_tabs.addTab(self._create_rsa_pss_subtab(), "RSA-PSS (Digital Signature)")

        layout.addWidget(self.modern_tabs)
        return widget

    def _create_aes_subtab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(10)

        key_box = QGroupBox(i18n.tr("enc_aes_key_info"))
        kb_lay = QHBoxLayout(key_box)
        self.txt_aes_key = QLineEdit()
        self.txt_aes_key.setPlaceholderText("64 hexadecimal characters (e.g. generated key)")
        btn_gen_aes = QPushButton(i18n.tr("btn_generate_key"))
        btn_gen_aes.clicked.connect(self._gen_aes_key)
        kb_lay.addWidget(self.txt_aes_key)
        kb_lay.addWidget(btn_gen_aes)
        lay.addWidget(key_box)

        # Optional AAD
        aad_box = QHBoxLayout()
        aad_box.addWidget(QLabel(i18n.tr("enc_aes_aad_label")))
        self.txt_aes_aad = QLineEdit()
        self.txt_aes_aad.setPlaceholderText("Optional Associated Authenticated Data (unencrypted)")
        aad_box.addWidget(self.txt_aes_aad)
        lay.addLayout(aad_box)

        # Buttons
        btn_row = QHBoxLayout()
        btn_enc = QPushButton(i18n.tr("btn_encrypt"))
        btn_enc.setObjectName("primary_btn")
        btn_enc.clicked.connect(self._encrypt_aes)
        btn_dec = QPushButton(i18n.tr("btn_decrypt"))
        btn_dec.clicked.connect(self._decrypt_aes)
        btn_row.addWidget(btn_enc)
        btn_row.addWidget(btn_dec)
        btn_row.addStretch()
        lay.addLayout(btn_row)

        splitter = QSplitter(Qt.Vertical)
        in_f = QFrame()
        in_f.setObjectName("card")
        in_l = QVBoxLayout(in_f)

        in_hdr = QHBoxLayout()
        in_hdr.addWidget(
            QLabel("Plaintext (for Encrypt) or JSON Container Envelope (for Decrypt):")
        )
        btn_detect_aes = QPushButton(i18n.tr("btn_auto_detect"))
        btn_detect_aes.clicked.connect(self._auto_detect_aes_input)
        in_hdr.addStretch()
        in_hdr.addWidget(btn_detect_aes)
        in_l.addLayout(in_hdr)

        self.txt_aes_in = QPlainTextEdit()
        in_l.addWidget(self.txt_aes_in)

        self.display_aes_out = CodeDisplay("Result (JSON Container or Decrypted Plaintext):")
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
        lay.addWidget(DisclaimerBanner(i18n.tr("enc_rsa_size_limit")))

        # Keygen row
        kg_card = QFrame()
        kg_card.setObjectName("card")
        kg_lay = QHBoxLayout(kg_card)
        kg_lay.addWidget(QLabel(i18n.tr("enc_rsa_keysize_label")))
        self.spin_rsa_size = QComboBox()
        self.spin_rsa_size.addItems(["2048", "3072", "4096"])
        btn_gen_rsa = QPushButton(i18n.tr("btn_generate_key"))
        btn_gen_rsa.clicked.connect(self._gen_rsa_keys)
        kg_lay.addWidget(self.spin_rsa_size)
        kg_lay.addWidget(btn_gen_rsa)
        kg_lay.addStretch()
        lay.addWidget(kg_card)

        # Keys display
        key_splitter = QSplitter(Qt.Horizontal)
        pub_f = QFrame()
        pub_l = QVBoxLayout(pub_f)
        pub_l.addWidget(QLabel(i18n.tr("enc_rsa_pubkey_label")))
        self.txt_rsa_pub = QPlainTextEdit()
        self.txt_rsa_pub.setPlaceholderText("-----BEGIN PUBLIC KEY-----...")
        pub_l.addWidget(self.txt_rsa_pub)

        priv_f = QFrame()
        priv_l = QVBoxLayout(priv_f)
        priv_l.addWidget(QLabel(i18n.tr("enc_rsa_privkey_label")))
        self.txt_rsa_priv = QPlainTextEdit()
        self.txt_rsa_priv.setPlaceholderText("-----BEGIN PRIVATE KEY-----...")
        priv_l.addWidget(self.txt_rsa_priv)

        key_splitter.addWidget(pub_f)
        key_splitter.addWidget(priv_f)
        lay.addWidget(key_splitter)

        # Action buttons
        btn_row = QHBoxLayout()
        btn_enc = QPushButton(i18n.tr("btn_encrypt"))
        btn_enc.setObjectName("primary_btn")
        btn_enc.clicked.connect(self._encrypt_rsa)
        btn_dec = QPushButton(i18n.tr("btn_decrypt"))
        btn_dec.clicked.connect(self._decrypt_rsa)
        btn_row.addWidget(btn_enc)
        btn_row.addWidget(btn_dec)
        btn_row.addStretch()
        lay.addLayout(btn_row)

        # Splitter for text in/out
        data_splitter = QSplitter(Qt.Vertical)
        in_f = QFrame()
        in_f.setObjectName("card")
        in_l = QVBoxLayout(in_f)
        in_l.addWidget(QLabel("Plaintext (to Encrypt) or Base64 Ciphertext (to Decrypt):"))
        self.txt_rsa_in = QPlainTextEdit()
        in_l.addWidget(self.txt_rsa_in)

        self.display_rsa_out = CodeDisplay("Result:")
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

        banner = DisclaimerBanner(
            "DIGITAL SIGNATURES: RSA-PSS creates a cryptographic proof of authenticity and integrity using the private key. "
            "Verification is performed with the sender's public key."
        )
        lay.addWidget(banner)

        # Message input
        msg_f = QFrame()
        msg_f.setObjectName("card")
        msg_l = QVBoxLayout(msg_f)
        msg_l.addWidget(QLabel("Message to Sign or Verify:"))
        self.txt_pss_msg = QPlainTextEdit()
        self.txt_pss_msg.setPlaceholderText("Enter message text...")
        msg_l.addWidget(self.txt_pss_msg)
        lay.addWidget(msg_f)

        # Key Inputs
        key_splitter = QSplitter(Qt.Horizontal)
        priv_f = QFrame()
        priv_l = QVBoxLayout(priv_f)
        priv_l.addWidget(QLabel("Private Key (PEM) for Signing:"))
        self.txt_pss_priv = QPlainTextEdit()
        priv_l.addWidget(self.txt_pss_priv)

        pub_f = QFrame()
        pub_l = QVBoxLayout(pub_f)
        pub_l.addWidget(QLabel("Public Key (PEM) for Verification:"))
        self.txt_pss_pub = QPlainTextEdit()
        pub_l.addWidget(self.txt_pss_pub)

        key_splitter.addWidget(priv_f)
        key_splitter.addWidget(pub_f)
        lay.addWidget(key_splitter)

        # Buttons
        btn_row = QHBoxLayout()
        btn_sign = QPushButton(i18n.tr("btn_sign"))
        btn_sign.setObjectName("primary_btn")
        btn_sign.clicked.connect(self._sign_pss)

        btn_verify = QPushButton(i18n.tr("btn_verify"))
        btn_verify.clicked.connect(self._verify_pss)

        btn_row.addWidget(btn_sign)
        btn_row.addWidget(btn_verify)
        btn_row.addStretch()
        lay.addLayout(btn_row)

        # Output / Signature Display
        self.display_pss_sig = CodeDisplay("Digital Signature (Base64) / Verification Status:")
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
