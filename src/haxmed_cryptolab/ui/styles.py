"""Theme stylesheets for HAXMED CryptoLab (Dark Charcoal with Crimson & Modern Light)."""

DARK_THEME_QSS = """
/* Global Reset and Typography */
QWidget {
    background-color: #141518;
    color: #E2E4E9;
    font-family: "Segoe UI Variable Text", "Segoe UI", "Tahoma", "Cairo", "Arial", sans-serif;
    font-size: 13px;
    selection-background-color: #c01525;
    selection-color: #FFFFFF;
}

/* Main Window */
QMainWindow {
    background-color: #121316;
}

/* Surfaces and Cards */
QFrame#card, QFrame#metric_card, QGroupBox {
    background-color: #1a1b20;
    border: 1px solid #282a32;
    border-radius: 8px;
    padding: 14px;
    margin-top: 8px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    padding: 2px 10px;
    color: #E02235;
    font-weight: 700;
    font-size: 13px;
}

/* Sidebar Navigation */
QFrame#sidebar {
    background-color: #0f1013;
    border: none;
    min-width: 245px;
    max-width: 270px;
}

QFrame#brand_header {
    background-color: transparent;
    border-bottom: 1px solid #22242a;
    padding: 12px 8px;
}

QLabel#brand_title {
    color: #FFFFFF;
    font-size: 15px;
    font-weight: bold;
}

QLabel#brand_tagline {
    color: #E02235;
    font-size: 11px;
    font-weight: 600;
}

/* Navigation Buttons */
QPushButton.nav_btn {
    background-color: transparent;
    color: #A0A4B0;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 10px 14px;
    font-weight: 500;
    font-size: 13px;
}

QPushButton.nav_btn:hover {
    background-color: #1c1d22;
    color: #FFFFFF;
}

QPushButton.nav_btn:checked, QPushButton.nav_btn[active="true"] {
    background-color: #2D1A20;
    color: #FFFFFF;
    border: 1px solid #8B1B25;
    font-weight: 600;
}

/* Action Buttons */
QPushButton {
    background-color: #262830;
    color: #E2E4E9;
    border: 1px solid #363944;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
    min-height: 24px;
}

QPushButton:hover {
    background-color: #323540;
    border-color: #484c5a;
    color: #FFFFFF;
}

QPushButton:pressed {
    background-color: #1e2026;
}

QPushButton:disabled {
    background-color: #18191e;
    color: #555866;
    border-color: #22242a;
}

/* Primary Crimson Accent Buttons */
QPushButton#primary_btn, QPushButton.primary {
    background-color: #C01525;
    color: #FFFFFF;
    border: 1px solid #D61B2D;
    font-weight: 600;
}

QPushButton#primary_btn:hover, QPushButton.primary:hover {
    background-color: #D61B2D;
    border-color: #E62A3C;
}

QPushButton#primary_btn:pressed, QPushButton.primary:pressed {
    background-color: #9E0F1D;
}

/* Danger / Cancel Buttons */
QPushButton#danger_btn {
    background-color: #4A151A;
    color: #FFB3BA;
    border: 1px solid #6B1E25;
}

QPushButton#danger_btn:hover {
    background-color: #6B1E25;
    color: #FFFFFF;
}

/* Inputs, Text Edits, Combos */
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox {
    background-color: #121316;
    color: #E2E4E9;
    border: 1px solid #2C2F3A;
    border-radius: 6px;
    padding: 7px 10px;
    font-family: "Cascadia Code", "Consolas", "Courier New", monospace;
    font-size: 13px;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #E02235;
    background-color: #16171b;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #1c1d22;
    border: 1px solid #2C2F3A;
    selection-background-color: #C01525;
    selection-color: #FFFFFF;
}

/* Tab Widgets */
QTabWidget::pane {
    border: 1px solid #282a32;
    background-color: #18191e;
    border-radius: 8px;
    top: -1px;
}

QTabBar::tab {
    background-color: #141518;
    color: #8C90A0;
    padding: 9px 20px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border: 1px solid #22242a;
    border-bottom: none;
    margin-right: 2px;
    margin-left: 2px;
}

QTabBar::tab:selected {
    background-color: #18191e;
    color: #FFFFFF;
    border: 1px solid #282a32;
    border-bottom: 2px solid #E02235;
    font-weight: 600;
}

QTabBar::tab:hover:!selected {
    background-color: #1c1d22;
    color: #CCD0DC;
}

/* Tables and Tree Views */
QTableWidget, QTableView {
    background-color: #141518;
    alternate-background-color: #18191e;
    gridline-color: #24262f;
    border: 1px solid #282a32;
    border-radius: 6px;
    font-size: 12px;
}

QHeaderView::section {
    background-color: #1c1d22;
    color: #A0A4B0;
    padding: 7px 10px;
    border: none;
    border-bottom: 1px solid #282a32;
    font-weight: 600;
    font-size: 12px;
}

/* Scrollbars */
QScrollBar:vertical {
    background: #121316;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #282a32;
    border-radius: 5px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background: #3A3D48;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Progress Bar */
QProgressBar {
    background-color: #141518;
    border: 1px solid #282a32;
    border-radius: 6px;
    height: 18px;
    text-align: center;
    color: #FFFFFF;
    font-size: 11px;
    font-weight: 600;
}

QProgressBar::chunk {
    background-color: #C01525;
    border-radius: 5px;
}

/* Banners & Labels */
QLabel#disclaimer_banner {
    background-color: #241417;
    border: 1px solid #661D24;
    border-radius: 6px;
    color: #FFC0C5;
    padding: 12px 16px;
    font-size: 12px;
}

QLabel#section_title {
    font-size: 18px;
    font-weight: 700;
    color: #FFFFFF;
}

QLabel#section_desc {
    color: #8C90A0;
    font-size: 12px;
}
"""

LIGHT_THEME_QSS = """
QWidget {
    background-color: #F8F9FA;
    color: #212529;
    font-family: "Segoe UI Variable Text", "Segoe UI", "Tahoma", "Cairo", "Arial", sans-serif;
    font-size: 13px;
    selection-background-color: #C01525;
    selection-color: #FFFFFF;
}

QMainWindow {
    background-color: #F0F2F5;
}

QFrame#card, QFrame#metric_card, QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #DEE2E6;
    border-radius: 8px;
    padding: 14px;
    margin-top: 8px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    padding: 2px 10px;
    color: #C01525;
    font-weight: 700;
    font-size: 13px;
}

QFrame#sidebar {
    background-color: #FFFFFF;
    border: none;
    min-width: 245px;
    max-width: 270px;
}

QFrame#brand_header {
    border-bottom: 1px solid #DEE2E6;
    padding: 12px 8px;
}

QLabel#brand_title {
    color: #121316;
    font-size: 15px;
    font-weight: bold;
}

QLabel#brand_tagline {
    color: #C01525;
    font-size: 11px;
    font-weight: 600;
}

QPushButton.nav_btn {
    background-color: transparent;
    color: #495057;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 10px 14px;
    font-weight: 500;
    font-size: 13px;
}

QPushButton.nav_btn:hover {
    background-color: #E9ECEF;
    color: #000000;
}

QPushButton.nav_btn:checked, QPushButton.nav_btn[active="true"] {
    background-color: #FCE8E9;
    color: #C01525;
    border: 1px solid #E8A0A6;
    font-weight: 600;
}

QPushButton {
    background-color: #E9ECEF;
    color: #212529;
    border: 1px solid #CED4DA;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 500;
    min-height: 24px;
}

QPushButton:hover {
    background-color: #DEE2E6;
    color: #000000;
}

QPushButton#primary_btn, QPushButton.primary {
    background-color: #C01525;
    color: #FFFFFF;
    border: 1px solid #A0121F;
    font-weight: 600;
}

QPushButton#primary_btn:hover, QPushButton.primary:hover {
    background-color: #D61B2D;
}

QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox {
    background-color: #FFFFFF;
    color: #212529;
    border: 1px solid #CED4DA;
    border-radius: 6px;
    padding: 7px 10px;
    font-family: "Cascadia Code", "Consolas", "Courier New", monospace;
    font-size: 13px;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 1px solid #C01525;
}

QTabWidget::pane {
    border: 1px solid #DEE2E6;
    background-color: #FFFFFF;
    border-radius: 8px;
}

QTabBar::tab {
    background-color: #E9ECEF;
    color: #6C757D;
    padding: 9px 20px;
    border: 1px solid #DEE2E6;
    border-bottom: none;
    margin-right: 2px;
    margin-left: 2px;
}

QTabBar::tab:selected {
    background-color: #FFFFFF;
    color: #212529;
    border-bottom: 2px solid #C01525;
    font-weight: 600;
}

QTableWidget, QTableView {
    background-color: #FFFFFF;
    alternate-background-color: #F8F9FA;
    border: 1px solid #DEE2E6;
    font-size: 12px;
}

QHeaderView::section {
    background-color: #E9ECEF;
    color: #495057;
    padding: 7px 10px;
    border: none;
    border-bottom: 1px solid #CED4DA;
    font-weight: 600;
    font-size: 12px;
}

QProgressBar {
    background-color: #E9ECEF;
    border: 1px solid #CED4DA;
    border-radius: 6px;
    text-align: center;
    color: #212529;
    font-size: 11px;
}

QProgressBar::chunk {
    background-color: #C01525;
    border-radius: 5px;
}

QLabel#disclaimer_banner {
    background-color: #FFF3CD;
    border: 1px solid #FFEEBA;
    color: #856404;
    border-radius: 6px;
    padding: 12px 16px;
}

QLabel#section_title {
    font-size: 18px;
    font-weight: 700;
    color: #212529;
}

QLabel#section_desc {
    color: #6C757D;
    font-size: 12px;
}
"""


def get_theme_stylesheet(theme_name: str = "dark") -> str:
    """Return the QSS stylesheet for the requested theme."""
    if theme_name.lower() == "light":
        return LIGHT_THEME_QSS
    return DARK_THEME_QSS
