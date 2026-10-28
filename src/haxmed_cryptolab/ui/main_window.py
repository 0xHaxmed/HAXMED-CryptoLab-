"""Main application window for HAXMED CryptoLab."""

from typing import Dict

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QStatusBar,
    QWidget,
)

from haxmed_cryptolab.core.config import ConfigManager
from haxmed_cryptolab.core.constants import (
    APP_NAME,
    APP_VERSION,
    ICON_PATH,
    ICON_PNG_PATH,
)
from haxmed_cryptolab.services.analysis_service import AnalysisService
from haxmed_cryptolab.services.crypto_service import CryptoService
from haxmed_cryptolab.services.hash_service import HashService
from haxmed_cryptolab.services.history_service import HistoryService
from haxmed_cryptolab.services.recovery_service import RecoveryService
from haxmed_cryptolab.ui.i18n import i18n
from haxmed_cryptolab.ui.navigation import NavigationSidebar
from haxmed_cryptolab.ui.pages.analyzer_page import AnalyzerPage
from haxmed_cryptolab.ui.pages.dashboard_page import DashboardPage
from haxmed_cryptolab.ui.pages.encryption_page import EncryptionPage
from haxmed_cryptolab.ui.pages.hash_page import HashPage
from haxmed_cryptolab.ui.pages.history_page import HistoryPage
from haxmed_cryptolab.ui.pages.recovery_page import RecoveryPage
from haxmed_cryptolab.ui.pages.settings_page import SettingsPage
from haxmed_cryptolab.ui.styles import get_theme_stylesheet


class MainWindow(QMainWindow):
    """Central Application Window."""

    def __init__(
        self,
        config_mgr: ConfigManager,
        crypto_service: CryptoService,
        hash_service: HashService,
        recovery_service: RecoveryService,
        analysis_service: AnalysisService,
        history_service: HistoryService,
        parent=None,
    ):
        super().__init__(parent)
        self.config_mgr = config_mgr
        self.crypto_service = crypto_service
        self.hash_service = hash_service
        self.recovery_service = recovery_service
        self.analysis_service = analysis_service
        self.history_service = history_service

        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(1120, 740)
        self.setMinimumSize(960, 620)

        icon_to_use = ICON_PNG_PATH if ICON_PNG_PATH.exists() else ICON_PATH
        if icon_to_use.exists():
            self.setWindowIcon(QIcon(str(icon_to_use)))

        # Apply initial theme & language
        self.apply_theme(self.config_mgr.config.theme)
        i18n.set_language(self.config_mgr.config.language)
        i18n.language_changed.connect(self._on_language_changed)

        # Central Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Sidebar Navigation
        self.sidebar = NavigationSidebar()
        self.sidebar.page_changed.connect(self._switch_page)
        self.main_layout.addWidget(self.sidebar)

        # Pages Stack
        self.stack = QStackedWidget()
        self.pages: Dict[str, QWidget] = {}

        self.page_dashboard = DashboardPage(
            self.crypto_service, self.history_service, self.analysis_service
        )
        self.page_dashboard.navigate_requested.connect(self._on_dashboard_navigate)
        self._add_page("dashboard", self.page_dashboard)

        self.page_encryption = EncryptionPage(self.crypto_service)
        self._add_page("encryption", self.page_encryption)

        self.page_hash = HashPage(self.hash_service)
        self._add_page("hash", self.page_hash)

        self.page_recovery = RecoveryPage(self.recovery_service)
        self._add_page("recovery", self.page_recovery)

        self.page_analyzer = AnalyzerPage(self.analysis_service)
        self._add_page("analyzer", self.page_analyzer)

        self.page_history = HistoryPage(self.history_service)
        self._add_page("history", self.page_history)

        self.page_settings = SettingsPage(self.config_mgr)
        self.page_settings.theme_changed.connect(self.apply_theme)
        self._add_page("settings", self.page_settings)

        self.main_layout.addWidget(self.stack)

        # Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage(
            f"HAXMED CryptoLab v{APP_VERSION} initialized. Local-only mode active."
        )

    def _add_page(self, key: str, page: QWidget):
        self.pages[key] = page
        self.stack.addWidget(page)

    def _switch_page(self, key: str):
        if key in self.pages:
            self.stack.setCurrentWidget(self.pages[key])
            self.sidebar.set_active_key(key)
            if key == "dashboard" and hasattr(self.page_dashboard, "refresh_stats"):
                self.page_dashboard.refresh_stats()
            elif key == "history" and hasattr(self.page_history, "refresh_table"):
                self.page_history.refresh_table()

    def _on_dashboard_navigate(self, page_key: str):
        self.sidebar.select_page(page_key)

    def apply_theme(self, theme_name: str):
        qss = get_theme_stylesheet(theme_name)
        app = QApplication.instance()
        if app:
            app.setStyleSheet(qss)
        else:
            self.setStyleSheet(qss)

    def _on_language_changed(self, lang_code: str):
        self.sidebar.update_texts()
        self.setWindowTitle(f"{i18n.tr('app_title')} v{APP_VERSION}")
        if hasattr(self, "statusBar") and self.statusBar:
            self.statusBar.showMessage(
                f"{i18n.tr('app_title')} v{APP_VERSION} - {i18n.tr('app_subtitle')}"
            )
        for page in self.pages.values():
            if hasattr(page, "retranslate_ui"):
                page.retranslate_ui()
