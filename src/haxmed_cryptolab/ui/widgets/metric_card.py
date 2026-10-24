"""Reusable Metric Card for dashboard and monitoring statistics."""

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class MetricCard(QFrame):
    """Card displaying a labeled numeric or status value."""

    def __init__(self, title: str, value: str = "0", subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("metric_card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)

        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet(
            "color: #8C90A0; font-size: 11px; font-weight: 600; text-transform: uppercase;"
        )

        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet(
            "color: #FFFFFF; font-size: 22px; font-weight: bold; font-family: monospace;"
        )

        self.lbl_sub = QLabel(subtitle)
        self.lbl_sub.setStyleSheet("color: #E02235; font-size: 11px;")
        if not subtitle:
            self.lbl_sub.hide()

        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_value)
        layout.addWidget(self.lbl_sub)

    def set_value(self, value: str):
        self.lbl_value.setText(value)

    def set_title(self, title: str):
        self.lbl_title.setText(title)

    def set_subtitle(self, subtitle: str):
        self.lbl_sub.setText(subtitle)
        self.lbl_sub.setVisible(bool(subtitle))
