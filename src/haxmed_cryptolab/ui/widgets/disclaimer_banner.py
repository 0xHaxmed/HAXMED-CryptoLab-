"""Prominent educational security banner."""

from PySide6.QtWidgets import QLabel


class DisclaimerBanner(QLabel):
    """Visual alert highlighting security warnings and educational scopes."""

    def __init__(self, text: str, is_warning: bool = True, parent=None):
        super().__init__(text, parent)
        self.setObjectName("disclaimer_banner")
        self.setWordWrap(True)
        self.setMargin(8)

    def set_text(self, text: str):
        """Helper alias for setText."""
        self.setText(text)
