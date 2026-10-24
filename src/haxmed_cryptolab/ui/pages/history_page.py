"""Module F — History & Reports Page."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from haxmed_cryptolab.services.history_service import HistoryService
from haxmed_cryptolab.ui.i18n import i18n
from haxmed_cryptolab.ui.widgets.disclaimer_banner import DisclaimerBanner


class HistoryPage(QWidget):
    """Audit history inspection and report generation."""

    def __init__(self, history_service: HistoryService, parent=None):
        super().__init__(parent)
        self.history_service = history_service

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 20)
        layout.setSpacing(12)

        lbl_title = QLabel(i18n.tr("hist_title"))
        lbl_title.setObjectName("section_title")
        layout.addWidget(lbl_title)

        banner = DisclaimerBanner(i18n.tr("hist_privacy_notice"))
        layout.addWidget(banner)

        # Toolbar
        tb_card = QFrame()
        tb_card.setObjectName("card")
        tb_lay = QHBoxLayout(tb_card)

        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.clicked.connect(self.refresh_table)

        btn_exp_txt = QPushButton(i18n.tr("hist_btn_export_txt"))
        btn_exp_txt.clicked.connect(lambda: self._export("txt"))

        btn_exp_json = QPushButton(i18n.tr("hist_btn_export_json"))
        btn_exp_json.clicked.connect(lambda: self._export("json"))

        btn_clear = QPushButton(i18n.tr("hist_btn_clear"))
        btn_clear.setObjectName("danger_btn")
        btn_clear.clicked.connect(self._clear_history)

        tb_lay.addWidget(btn_refresh)
        tb_lay.addWidget(btn_exp_txt)
        tb_lay.addWidget(btn_exp_json)
        tb_lay.addStretch()
        tb_lay.addWidget(btn_clear)
        layout.addWidget(tb_card)

        # Table
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Timestamp (UTC)",
                "Operation",
                "Algorithm",
                "Status",
                "Duration (ms)",
            ]
        )
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.table)

    def refresh_table(self):
        records = self.history_service.get_recent_history(limit=200)
        self.table.setRowCount(len(records))

        for row, r in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(str(r.id or "")))
            self.table.setItem(row, 1, QTableWidgetItem(r.timestamp))
            self.table.setItem(row, 2, QTableWidgetItem(r.operation_type))
            self.table.setItem(row, 3, QTableWidgetItem(r.algorithm))

            status_item = QTableWidgetItem(r.status)
            if r.status in ("SUCCESS", "MATCH"):
                status_item.setForeground(Qt.green)
            elif r.status in ("FAILED", "INVALID_INPUT"):
                status_item.setForeground(Qt.red)
            self.table.setItem(row, 4, status_item)

            self.table.setItem(row, 5, QTableWidgetItem(f"{r.duration_ms:.2f}"))

    def _export(self, fmt: str):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Audit History",
            f"cryptolab_audit_history.{fmt}",
            f"{fmt.upper()} Files (*.{fmt});;All Files (*)",
        )
        if path:
            content = self.history_service.export_history(fmt)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            QMessageBox.information(self, "Export Complete", f"History saved to {path}")

    def _clear_history(self):
        confirm = QMessageBox.question(
            self,
            "Confirm Clear History",
            "Are you sure you want to delete all local history records? This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.history_service.clear_history()
            self.refresh_table()
            QMessageBox.information(
                self, "History Cleared", "All audit history records have been purged."
            )
