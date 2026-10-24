"""Output text viewer with copy, clear, and export actions."""

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)

from haxmed_cryptolab.ui.i18n import i18n


class CodeDisplay(QFrame):
    """Text viewer with action toolbar for copying, clearing, and exporting."""

    def __init__(self, title: str = "", read_only: bool = True, parent=None):
        super().__init__(parent)
        self.setObjectName("card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)

        # Header toolbar
        header = QHBoxLayout()
        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet("font-weight: 600; color: #E02235;")

        self.lbl_meta = QLabel("0 chars")
        self.lbl_meta.setStyleSheet("color: #717584; font-size: 11px;")

        self.btn_copy = QPushButton(i18n.tr("btn_copy"))
        self.btn_copy.setFixedHeight(26)
        self.btn_copy.clicked.connect(self._copy_to_clipboard)

        self.btn_clear = QPushButton(i18n.tr("btn_clear"))
        self.btn_clear.setFixedHeight(26)
        self.btn_clear.clicked.connect(self.clear)

        self.btn_export = QPushButton(i18n.tr("btn_export"))
        self.btn_export.setFixedHeight(26)
        self.btn_export.clicked.connect(self._export_to_file)

        header.addWidget(self.lbl_title)
        header.addStretch()
        header.addWidget(self.lbl_meta)
        header.addWidget(self.btn_copy)
        header.addWidget(self.btn_export)
        header.addWidget(self.btn_clear)

        # Main text view
        self.text_edit = QPlainTextEdit()
        self.text_edit.setReadOnly(read_only)
        self.text_edit.textChanged.connect(self._update_meta)

        layout.addLayout(header)
        layout.addWidget(self.text_edit)

    def set_text(self, text: str):
        self.text_edit.setPlainText(text)
        self._update_meta()

    def get_text(self) -> str:
        return self.text_edit.toPlainText()

    def clear(self):
        self.text_edit.clear()
        self._update_meta()

    def _update_meta(self):
        chars = len(self.text_edit.toPlainText())
        bytes_count = len(self.text_edit.toPlainText().encode("utf-8"))
        self.lbl_meta.setText(f"{chars:,} chars ({bytes_count:,} bytes)")

    def _copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())

    def _export_to_file(self):
        text = self.text_edit.toPlainText()
        if not text:
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            i18n.tr("btn_export"),
            "cryptolab_export.txt",
            "Text Files (*.txt);;All Files (*)",
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
