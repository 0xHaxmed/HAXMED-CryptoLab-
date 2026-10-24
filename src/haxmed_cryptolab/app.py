"""Application bootstrap and lifecycle management."""

import platform
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from haxmed_cryptolab.core.config import ConfigManager
from haxmed_cryptolab.core.constants import APP_NAME, ICON_PATH, ICON_PNG_PATH
from haxmed_cryptolab.services.analysis_service import AnalysisService
from haxmed_cryptolab.services.crypto_service import CryptoService
from haxmed_cryptolab.services.hash_service import HashService
from haxmed_cryptolab.services.history_service import HistoryService
from haxmed_cryptolab.services.recovery_service import RecoveryService
from haxmed_cryptolab.storage.database import DatabaseManager
from haxmed_cryptolab.storage.history_repository import HistoryRepository
from haxmed_cryptolab.ui.main_window import MainWindow


class CryptoLabApplication:
    """Encapsulates application initialization and execution."""

    def __init__(self, sys_argv=None):
        self.sys_argv = sys_argv or sys.argv

        if platform.system() == "Windows":
            try:
                import ctypes
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    "haxmed.cryptolab.toolkit.1.0"
                )
            except Exception:
                pass

        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(self.sys_argv)
            self.app.setApplicationName(APP_NAME)

        # Set application-wide brand icon
        icon_path = ICON_PNG_PATH if ICON_PNG_PATH.exists() else ICON_PATH
        if icon_path.exists():
            self.app.setWindowIcon(QIcon(str(icon_path)))

        # 1. Initialize Configuration & Database
        self.config_mgr = ConfigManager()
        self.db_manager = DatabaseManager()
        self.history_repo = HistoryRepository(self.db_manager)

        # 2. Initialize Services
        self.crypto_service = CryptoService(self.history_repo, self.config_mgr)
        self.hash_service = HashService(self.history_repo, self.config_mgr)
        self.recovery_service = RecoveryService(self.history_repo, self.config_mgr)
        self.analysis_service = AnalysisService()
        self.history_service = HistoryService(self.history_repo, self.config_mgr)

        # 3. Create Main Window
        self.main_window = MainWindow(
            config_mgr=self.config_mgr,
            crypto_service=self.crypto_service,
            hash_service=self.hash_service,
            recovery_service=self.recovery_service,
            analysis_service=self.analysis_service,
            history_service=self.history_service,
        )

    def run(self) -> int:
        """Show main window and enter Qt event loop."""
        self.main_window.show()
        return self.app.exec()


def run_app():
    """Entry point function."""
    app_instance = CryptoLabApplication()
    sys.exit(app_instance.run())
