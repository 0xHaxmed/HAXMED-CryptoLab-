"""UI testing with pytest-qt for MainWindow, navigation, and bilingual switching."""

import os

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from haxmed_cryptolab.core.config import ConfigManager
from haxmed_cryptolab.services.analysis_service import AnalysisService
from haxmed_cryptolab.services.crypto_service import CryptoService
from haxmed_cryptolab.services.hash_service import HashService
from haxmed_cryptolab.services.history_service import HistoryService
from haxmed_cryptolab.services.recovery_service import RecoveryService
from haxmed_cryptolab.storage.database import DatabaseManager
from haxmed_cryptolab.storage.history_repository import HistoryRepository
from haxmed_cryptolab.ui.i18n import i18n
from haxmed_cryptolab.ui.main_window import MainWindow


@pytest.fixture
def app_window(qtbot, tmp_path):
    os.environ["QT_QPA_PLATFORM"] = "offscreen"

    db_path = tmp_path / "ui_test.db"
    cfg_path = tmp_path / "ui_test_cfg.json"

    cfg_mgr = ConfigManager(config_path=cfg_path)
    db_mgr = DatabaseManager(db_path=db_path)
    hist_repo = HistoryRepository(db_mgr)

    crypto_svc = CryptoService(hist_repo, cfg_mgr)
    hash_svc = HashService(hist_repo, cfg_mgr)
    rec_svc = RecoveryService(hist_repo, cfg_mgr)
    ana_svc = AnalysisService()
    hist_svc = HistoryService(hist_repo, cfg_mgr)

    win = MainWindow(
        config_mgr=cfg_mgr,
        crypto_service=crypto_svc,
        hash_service=hash_svc,
        recovery_service=rec_svc,
        analysis_service=ana_svc,
        history_service=hist_svc,
    )
    qtbot.addWidget(win)
    return win


class TestMainWindowUI:
    def test_window_startup_and_pages(self, app_window, qtbot):
        assert app_window.windowTitle().startswith("HAXMED CryptoLab")
        assert app_window.stack.count() == 7
        assert app_window.stack.currentWidget() == app_window.page_dashboard

    def test_navigation_switching(self, app_window, qtbot):
        # Click Encryption button
        qtbot.mouseClick(app_window.sidebar.nav_buttons["encryption"], Qt.LeftButton)
        assert app_window.stack.currentWidget() == app_window.page_encryption

        # Click Hash button
        qtbot.mouseClick(app_window.sidebar.nav_buttons["hash"], Qt.LeftButton)
        assert app_window.stack.currentWidget() == app_window.page_hash

        # Click Recovery button
        qtbot.mouseClick(app_window.sidebar.nav_buttons["recovery"], Qt.LeftButton)
        assert app_window.stack.currentWidget() == app_window.page_recovery

        # Click Analyzer button
        qtbot.mouseClick(app_window.sidebar.nav_buttons["analyzer"], Qt.LeftButton)
        assert app_window.stack.currentWidget() == app_window.page_analyzer

        # Click History button
        qtbot.mouseClick(app_window.sidebar.nav_buttons["history"], Qt.LeftButton)
        assert app_window.stack.currentWidget() == app_window.page_history

        # Click Settings button
        qtbot.mouseClick(app_window.sidebar.nav_buttons["settings"], Qt.LeftButton)
        assert app_window.stack.currentWidget() == app_window.page_settings

    def test_language_switching_rtl(self, app_window, qtbot):
        # Switch to Arabic
        i18n.set_language("ar")
        assert QApplication.isRightToLeft() is True
        assert "لوحة التحكم" in app_window.sidebar.nav_buttons["dashboard"].text()

        # Switch back to English
        i18n.set_language("en")
        assert QApplication.isLeftToRight() is True
        assert "Dashboard" in app_window.sidebar.nav_buttons["dashboard"].text()

    def test_theme_switching(self, app_window, qtbot):
        app_window.apply_theme("light")
        # Should execute without exceptions
        app_window.apply_theme("dark")
