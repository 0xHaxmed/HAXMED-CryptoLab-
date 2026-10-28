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

        self.lbl_title = QLabel(i18n.tr("set_title"))
        self.lbl_title.setObjectName("section_title")
        layout.addWidget(self.lbl_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        lay = QVBoxLayout(container)
        lay.setSpacing(16)

        # 1. Interface Preferences
        self.ui_group = QGroupBox(i18n.tr("set_ui_group"))
        ui_lay = QGridLayout(self.ui_group)
        ui_lay.setContentsMargins(14, 12, 14, 12)
        ui_lay.setSpacing(12)

        self.lbl_lang = QLabel(i18n.tr("set_language_label"))
        ui_lay.addWidget(self.lbl_lang, 0, 0)
        self.combo_lang = QComboBox()
        self.combo_lang.addItem("English (LTR)", "en")
        self.combo_lang.addItem("العربية (Arabic - RTL)", "ar")
        current_lang = self.config_mgr.config.language
        idx = 1 if current_lang == "ar" else 0
        self.combo_lang.setCurrentIndex(idx)
        self.combo_lang.currentIndexChanged.connect(self._on_language_changed)
        ui_lay.addWidget(self.combo_lang, 0, 1)

        self.lbl_theme = QLabel(i18n.tr("set_theme_label"))
        ui_lay.addWidget(self.lbl_theme, 1, 0)
        self.combo_theme = QComboBox()
        self._populate_theme_combo()
        current_theme = self.config_mgr.config.theme
        t_idx = 1 if current_theme == "light" else 0
        self.combo_theme.setCurrentIndex(t_idx)
        self.combo_theme.currentIndexChanged.connect(self._on_theme_changed)
        ui_lay.addWidget(self.combo_theme, 1, 1)

        lay.addWidget(self.ui_group)

        # 2. Privacy & History
        self.priv_group = QGroupBox(i18n.tr("set_privacy_group"))
        priv_lay = QVBoxLayout(self.priv_group)
        priv_lay.setContentsMargins(14, 12, 14, 12)
        priv_lay.setSpacing(8)

        self.chk_history = QCheckBox(i18n.tr("set_enable_history"))
        self.chk_history.setChecked(self.config_mgr.config.enable_history)
        self.chk_history.toggled.connect(self._on_history_toggled)

        self.lbl_priv_desc = QLabel(i18n.tr("set_privacy_desc"))
        self.lbl_priv_desc.setWordWrap(True)
        self.lbl_priv_desc.setStyleSheet("color: #8C90A0; font-size: 11px;")
        priv_lay.addWidget(self.chk_history)
        priv_lay.addWidget(self.lbl_priv_desc)
        lay.addWidget(self.priv_group)

        # 3. System & About Information
        self.sys_group = QGroupBox(i18n.tr("set_app_info_group"))
        sys_lay = QGridLayout(self.sys_group)
        sys_lay.setContentsMargins(14, 12, 14, 12)
        sys_lay.setSpacing(10)

        self.lbl_app_name_key = QLabel(i18n.tr("set_app_name"))
        sys_lay.addWidget(self.lbl_app_name_key, 0, 0)
        sys_lay.addWidget(QLabel(f"<b>{APP_NAME}</b>"), 0, 1)

        self.lbl_version_key = QLabel(i18n.tr("set_version"))
        sys_lay.addWidget(self.lbl_version_key, 1, 0)
        sys_lay.addWidget(QLabel(f"<b>v{APP_VERSION}</b>"), 1, 1)

        self.lbl_author_key = QLabel(i18n.tr("set_author"))
        sys_lay.addWidget(self.lbl_author_key, 2, 0)
        sys_lay.addWidget(QLabel(APP_AUTHOR), 2, 1)

        self.btn_about = QPushButton(f"ℹ️ {i18n.tr('nav_about')}")
        self.btn_about.clicked.connect(self._show_about)
        sys_lay.addWidget(self.btn_about, 3, 0, 1, 2)
        lay.addWidget(self.sys_group)

        # 4. Actions
        act_row = QHBoxLayout()
        self.btn_reset = QPushButton(i18n.tr("btn_reset"))
        self.btn_reset.clicked.connect(self._reset_defaults)
        act_row.addWidget(self.btn_reset)
        act_row.addStretch()
        lay.addLayout(act_row)

        lay.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)

    def _populate_theme_combo(self):
        curr = self.combo_theme.currentData() if hasattr(self, "combo_theme") and self.combo_theme.count() > 0 else "dark"
        self.combo_theme.blockSignals(True)
        self.combo_theme.clear()
        self.combo_theme.addItem(i18n.tr("set_theme_dark"), "dark")
        self.combo_theme.addItem(i18n.tr("set_theme_light"), "light")
        idx = self.combo_theme.findData(curr)
        if idx >= 0:
            self.combo_theme.setCurrentIndex(idx)
        self.combo_theme.blockSignals(False)

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
        reply = QMessageBox.question(
            self,
            "Reset Preferences",
            "Reset all preferences to default values?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            cfg = self.config_mgr.reset_defaults()
            idx = 1 if cfg.language == "ar" else 0
            self.combo_lang.setCurrentIndex(idx)
            t_idx = 1 if cfg.theme == "light" else 0
            self.combo_theme.setCurrentIndex(t_idx)
            self.chk_history.setChecked(cfg.enable_history)

    def retranslate_ui(self):
        """Update all text elements when interface language is toggled."""
        self.lbl_title.setText(i18n.tr("set_title"))
        self.ui_group.setTitle(i18n.tr("set_ui_group"))
        self.lbl_lang.setText(i18n.tr("set_language_label"))
        self.lbl_theme.setText(i18n.tr("set_theme_label"))
        self._populate_theme_combo()

        self.priv_group.setTitle(i18n.tr("set_privacy_group"))
        self.chk_history.setText(i18n.tr("set_enable_history"))
        self.lbl_priv_desc.setText(i18n.tr("set_privacy_desc"))

        self.sys_group.setTitle(i18n.tr("set_app_info_group"))
        self.lbl_app_name_key.setText(i18n.tr("set_app_name"))
        self.lbl_version_key.setText(i18n.tr("set_version"))
        self.lbl_author_key.setText(i18n.tr("set_author"))
        self.btn_about.setText(f"ℹ️ {i18n.tr('nav_about')}")
        self.btn_reset.setText(i18n.tr("btn_reset"))
