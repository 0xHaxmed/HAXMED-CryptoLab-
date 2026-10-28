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
        self._last_ioc = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 20)
        layout.setSpacing(12)

        self.lbl_title = QLabel(i18n.tr("ana_title"))
        self.lbl_title.setObjectName("section_title")
        layout.addWidget(self.lbl_title)

        self.banner = DisclaimerBanner(i18n.tr("ana_heuristics_banner"))
        layout.addWidget(self.banner)

        # Input Card
        in_card = QFrame()
        in_card.setObjectName("card")
        in_lay = QVBoxLayout(in_card)
        in_lay.setContentsMargins(14, 12, 14, 12)
        in_lay.setSpacing(10)

        self.lbl_in = QLabel(i18n.tr("ana_input_label"))
        in_lay.addWidget(self.lbl_in)
        self.txt_cipher_in = QPlainTextEdit()
        self.txt_cipher_in.setPlaceholderText(i18n.tr("ana_input_placeholder"))
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
        left_lay.setSpacing(8)

        ioc_box = QFrame()
        ioc_box.setObjectName("card")
        ioc_lay = QVBoxLayout(ioc_box)
        self.lbl_ioc_val = QLabel(f"{i18n.tr('ana_ioc_label')} --")
        self.lbl_ioc_val.setStyleSheet("font-size: 15px; font-weight: bold; color: #E02235;")
        self.lbl_ioc_sub = QLabel(i18n.tr("ana_ioc_explanation"))
        self.lbl_ioc_sub.setStyleSheet("color: #8C90A0; font-size: 11px;")
        ioc_lay.addWidget(self.lbl_ioc_val)
        ioc_lay.addWidget(self.lbl_ioc_sub)
        left_lay.addWidget(ioc_box)

        self.table_freq = QTableWidget(26, 4)
        self._set_freq_headers()
        self.table_freq.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_lay.addWidget(self.table_freq)
        splitter.addWidget(left_widget)

        # Right Column: Caesar Ranking Table
        right_widget = QWidget()
        right_lay = QVBoxLayout(right_widget)
        right_lay.setContentsMargins(0, 0, 0, 0)
        right_lay.setSpacing(8)

        self.right_header = QLabel(i18n.tr("ana_caesar_rank_title"))
        self.right_header.setStyleSheet(
            "font-weight: 600; color: #FFFFFF; font-size: 13px; padding-bottom: 4px;"
        )
        right_lay.addWidget(self.right_header)

        self.table_caesar = QTableWidget(26, 4)
        self._set_caesar_headers()
        self.table_caesar.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        right_lay.addWidget(self.table_caesar)
        splitter.addWidget(right_widget)

        layout.addWidget(splitter)

    def _set_freq_headers(self):
        self.table_freq.setHorizontalHeaderLabels(
            [
                i18n.tr("ana_col_letter"),
                i18n.tr("ana_col_count"),
                i18n.tr("ana_col_obs"),
                i18n.tr("ana_col_exp"),
            ]
        )

    def _set_caesar_headers(self):
        self.table_caesar.setHorizontalHeaderLabels(
            [
                i18n.tr("ana_rank_col_rank"),
                i18n.tr("ana_rank_col_shift"),
                i18n.tr("ana_rank_col_chisq"),
                i18n.tr("ana_rank_col_preview"),
            ]
        )

    def _run_analysis(self):
        text = self.txt_cipher_in.toPlainText()
        if not text.strip():
            return

        counts, pcts, ioc, total_chars = self.analysis_service.analyze_frequencies(text)
        self._last_ioc = ioc
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
            self.table_caesar.setItem(row, 2, QTableWidgetItem(f"{cand.chi_squared:.2f}"))
            self.table_caesar.setItem(row, 3, QTableWidgetItem(preview))

    def retranslate_ui(self):
        """Update all text elements when interface language is toggled."""
        self.lbl_title.setText(i18n.tr("ana_title"))
        self.banner.set_text(i18n.tr("ana_heuristics_banner"))
        self.lbl_in.setText(i18n.tr("ana_input_label"))
        self.txt_cipher_in.setPlaceholderText(i18n.tr("ana_input_placeholder"))
        self.btn_analyze.setText(f"🔍 {i18n.tr('ana_btn_analyze')}")
        if self._last_ioc is not None:
            self.lbl_ioc_val.setText(f"{i18n.tr('ana_ioc_label')} {self._last_ioc:.4f}")
        else:
            self.lbl_ioc_val.setText(f"{i18n.tr('ana_ioc_label')} --")
        self.lbl_ioc_sub.setText(i18n.tr("ana_ioc_explanation"))
        self.right_header.setText(i18n.tr("ana_caesar_rank_title"))
        self._set_freq_headers()
        self._set_caesar_headers()
