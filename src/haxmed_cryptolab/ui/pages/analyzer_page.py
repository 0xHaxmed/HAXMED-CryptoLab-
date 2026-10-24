"""Module E — Classical Cipher Analyzer Page."""

import string

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from haxmed_cryptolab.engines.analysis.frequency import ENGLISH_LETTER_FREQUENCIES
from haxmed_cryptolab.services.analysis_service import AnalysisService
from haxmed_cryptolab.ui.i18n import i18n
from haxmed_cryptolab.ui.widgets.disclaimer_banner import DisclaimerBanner


class AnalyzerPage(QWidget):
    """Classical Cipher Analyzer with frequency metrics and Caesar shift ranking."""

    def __init__(self, analysis_service: AnalysisService, parent=None):
        super().__init__(parent)
        self.analysis_service = analysis_service

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 20)
        layout.setSpacing(12)

        lbl_title = QLabel(i18n.tr("ana_title"))
        lbl_title.setObjectName("section_title")
        layout.addWidget(lbl_title)

        banner = DisclaimerBanner(
            "CRYPTANALYSIS HEURISTICS: Frequency distribution and Index of Coincidence (IoC) provide statistical heuristics, "
            "not absolute proofs. Natural language text must be of sufficient length for frequencies to stabilize."
        )
        layout.addWidget(banner)

        # Input Card
        in_card = QFrame()
        in_card.setObjectName("card")
        in_lay = QVBoxLayout(in_card)
        in_lay.addWidget(QLabel(i18n.tr("ana_input_label")))
        self.txt_cipher_in = QPlainTextEdit()
        self.txt_cipher_in.setPlaceholderText(
            "Paste ciphertext here to analyze letter frequencies and Caesar rotations..."
        )
        self.txt_cipher_in.setMaximumHeight(100)
        in_lay.addWidget(self.txt_cipher_in)

        btn_row = QHBoxLayout()
        self.btn_analyze = QPushButton(f"🔍 {i18n.tr('ana_btn_analyze')}")
        self.btn_analyze.setObjectName("primary_btn")
        self.btn_analyze.clicked.connect(self._run_analysis)
        btn_row.addWidget(self.btn_analyze)
        btn_row.addStretch()
        in_lay.addLayout(btn_row)
        layout.addWidget(in_card)

        # Results Splitter (Left: Frequency table & IoC, Right: Caesar Shifts Ranking)
        splitter = QSplitter(Qt.Horizontal)

        # Left Column: Frequencies & IoC
        left_widget = QWidget()
        left_lay = QVBoxLayout(left_widget)
        left_lay.setContentsMargins(0, 0, 0, 0)

        ioc_box = QFrame()
        ioc_box.setObjectName("card")
        ioc_lay = QVBoxLayout(ioc_box)
        self.lbl_ioc_val = QLabel(f"{i18n.tr('ana_ioc_label')} --")
        self.lbl_ioc_val.setStyleSheet("font-size: 15px; font-weight: bold; color: #E02235;")
        lbl_ioc_sub = QLabel(i18n.tr("ana_ioc_explanation"))
        lbl_ioc_sub.setStyleSheet("color: #8C90A0; font-size: 11px;")
        ioc_lay.addWidget(self.lbl_ioc_val)
        ioc_lay.addWidget(lbl_ioc_sub)
        left_lay.addWidget(ioc_box)

        self.table_freq = QTableWidget(26, 4)
        self.table_freq.setHorizontalHeaderLabels(
            ["Letter", "Count", "Observed %", "English Exp. %"]
        )
        self.table_freq.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_lay.addWidget(self.table_freq)
        splitter.addWidget(left_widget)

        # Right Column: Caesar Ranking Table
        right_widget = QWidget()
        right_lay = QVBoxLayout(right_widget)
        right_lay.setContentsMargins(0, 0, 0, 0)

        right_header = QLabel(i18n.tr("ana_caesar_rank_title"))
        right_header.setStyleSheet(
            "font-weight: 600; color: #FFFFFF; font-size: 13px; padding-bottom: 4px;"
        )
        right_lay.addWidget(right_header)

        self.table_caesar = QTableWidget(26, 4)
        self.table_caesar.setHorizontalHeaderLabels(
            ["Rank", "Shift", "Chi-Sq Score", "Candidate Plaintext Preview"]
        )
        self.table_caesar.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        right_lay.addWidget(self.table_caesar)
        splitter.addWidget(right_widget)

        layout.addWidget(splitter)

    def _run_analysis(self):
        text = self.txt_cipher_in.toPlainText()
        if not text.strip():
            return

        counts, pcts, ioc, total_chars = self.analysis_service.analyze_frequencies(text)
        self.lbl_ioc_val.setText(f"{i18n.tr('ana_ioc_label')} {ioc:.4f}")

        # Populate frequency table
        for row, letter in enumerate(string.ascii_uppercase):
            cnt = counts[letter]
            pct = pcts[letter]
            exp_pct = ENGLISH_LETTER_FREQUENCIES[letter]

            self.table_freq.setItem(row, 0, QTableWidgetItem(letter))
            self.table_freq.setItem(row, 1, QTableWidgetItem(f"{cnt:,}"))
            self.table_freq.setItem(row, 2, QTableWidgetItem(f"{pct:.2f}%"))
            self.table_freq.setItem(row, 3, QTableWidgetItem(f"{exp_pct:.2f}%"))

        # Populate Caesar Ranking table
        caesar_candidates = self.analysis_service.analyze_caesar_shifts(text)
        self.table_caesar.setRowCount(len(caesar_candidates))

        for row, cand in enumerate(caesar_candidates):
            preview = cand.plaintext[:60].replace("\n", " ") + (
                "..." if len(cand.plaintext) > 60 else ""
            )
            self.table_caesar.setItem(row, 0, QTableWidgetItem(f"#{cand.rank}"))
            self.table_caesar.setItem(row, 1, QTableWidgetItem(f"Shift {cand.shift}"))
            self.table_caesar.setItem(row, 2, QTableWidgetItem(f"{cand.chi_squared:.1f}"))
            self.table_caesar.setItem(row, 3, QTableWidgetItem(preview))
