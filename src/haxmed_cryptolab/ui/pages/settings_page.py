"""Module G — Settings Page."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from haxmed_cryptolab.core.config import ConfigManager
from haxmed_cryptolab.core.constants import APP_AUTHOR, APP_NAME, APP_VERSION
from haxmed_cryptolab.ui.dialogs.about_dialog import AboutDialog
from haxmed_cryptolab.ui.i18n import i18n


class SettingsPage(QWidget):
    """Application Settings and preferences management."""

    theme_changed = Signal(str)
    language_changed = Signal(str)

    def __init__(self, config_mgr: ConfigManager, parent=None):
        super().__init__(parent)
        self.config_mgr = config_mgr

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 20)
        layout.setSpacing(12)

        lbl_title = QLabel(i18n.tr("set_title"))
        lbl_title.setObjectName("section_title")
        layout.addWidget(lbl_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        lay = QVBoxLayout(container)
        lay.setSpacing(16)

        # 1. Interface Preferences
        ui_group = QGroupBox("Interface & Appearance")
        ui_lay = QGridLayout(ui_group)
        ui_lay.setSpacing(12)

        ui_lay.addWidget(QLabel(i18n.tr("set_language_label")), 0, 0)
        self.combo_lang = QComboBox()
        self.combo_lang.addItem("English (LTR)", "en")
        self.combo_lang.addItem("العربية (Arabic - RTL)", "ar")
        current_lang = self.config_mgr.config.language
        idx = 1 if current_lang == "ar" else 0
        self.combo_lang.setCurrentIndex(idx)
        self.combo_lang.currentIndexChanged.connect(self._on_language_changed)
        ui_lay.addWidget(self.combo_lang, 0, 1)

        ui_lay.addWidget(QLabel(i18n.tr("set_theme_label")), 1, 0)
        self.combo_theme = QComboBox()
        self.combo_theme.addItem("Dark Charcoal (Crimson Accents)", "dark")
        self.combo_theme.addItem("Light Modern", "light")
        current_theme = self.config_mgr.config.theme
        t_idx = 1 if current_theme == "light" else 0
        self.combo_theme.setCurrentIndex(t_idx)
        self.combo_theme.currentIndexChanged.connect(self._on_theme_changed)
        ui_lay.addWidget(self.combo_theme, 1, 1)

        lay.addWidget(ui_group)

        # 2. Privacy & History
        priv_group = QGroupBox(i18n.tr("set_privacy_group"))
        priv_lay = QVBoxLayout(priv_group)
        self.chk_history = QCheckBox(i18n.tr("set_enable_history"))
        self.chk_history.setChecked(self.config_mgr.config.enable_history)
        self.chk_history.toggled.connect(self._on_history_toggled)

        lbl_priv_desc = QLabel(
            "When enabled, operation metadata (type, algorithm, duration, status) is stored locally in SQLite. "
            "Plaintexts, secret keys, and passwords are NEVER saved under any circumstances."
        )
        lbl_priv_desc.setWordWrap(True)
        lbl_priv_desc.setStyleSheet("color: #8C90A0; font-size: 11px;")
        priv_lay.addWidget(self.chk_history)
        priv_lay.addWidget(lbl_priv_desc)
        lay.addWidget(priv_group)

        # 3. System & About Information
        sys_group = QGroupBox("Application Information")
        sys_lay = QGridLayout(sys_group)
        sys_lay.addWidget(QLabel("Application Name:"), 0, 0)
        sys_lay.addWidget(QLabel(f"<b>{APP_NAME}</b>"), 0, 1)

        sys_lay.addWidget(QLabel("Version:"), 1, 0)
        sys_lay.addWidget(QLabel(f"<b>v{APP_VERSION}</b>"), 1, 1)

        sys_lay.addWidget(QLabel("Author:"), 2, 0)
        sys_lay.addWidget(QLabel(APP_AUTHOR), 2, 1)

        btn_about = QPushButton(f"ℹ️ {i18n.tr('nav_about')}")
        btn_about.clicked.connect(self._show_about)
        sys_lay.addWidget(btn_about, 3, 0, 1, 2)
        lay.addWidget(sys_group)

        # 4. Actions
        act_row = QHBoxLayout()
        btn_reset = QPushButton(i18n.tr("btn_reset"))
        btn_reset.clicked.connect(self._reset_defaults)
        act_row.addWidget(btn_reset)
        act_row.addStretch()
        lay.addLayout(act_row)

        lay.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)

    def _on_language_changed(self):
        lang = self.combo_lang.currentData()
        config = self.config_mgr.config
        config.language = lang
        self.config_mgr.save(config)
        i18n.set_language(lang)
        self.language_changed.emit(lang)

    def _on_theme_changed(self):
        theme = self.combo_theme.currentData()
        config = self.config_mgr.config
        config.theme = theme
        self.config_mgr.save(config)
        self.theme_changed.emit(theme)

    def _on_history_toggled(self, checked: bool):
        config = self.config_mgr.config
        config.enable_history = checked
        self.config_mgr.save(config)

    def _show_about(self):
        dlg = AboutDialog(self)
        dlg.exec()

    def _reset_defaults(self):
        confirm = QMessageBox.question(
            self,
            "Reset Settings",
            "Reset all settings to default values?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            cfg = self.config_mgr.reset_defaults()
            self.combo_lang.setCurrentIndex(0)
            self.combo_theme.setCurrentIndex(0)
            self.chk_history.setChecked(cfg.enable_history)
            self.theme_changed.emit("dark")
            self.language_changed.emit("en")
            QMessageBox.information(self, "Reset", "Settings have been reset to default values.")
