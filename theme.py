from string import Template

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication

import settings

METRO_COLORS = ["#1ba1e2", "#60a917", "#f0a30a", "#aa00ff", "#d80073", "#fa6800", "#00aba9", "#e51400"]

ACCENT_COLORS = {
    "Blue": ("#007acc", "#1c97ea"),
    "Orange": ("#d4650f", "#f08a24"),
    "Green": ("#2e8b57", "#3fae6f"),
    "Purple": ("#7e57c2", "#9575cd"),
}

PALETTES = {
    "Dark": {
        "bg": "#252526", "base": "#1e1e1e", "panel": "#2d2d30", "border": "#3f3f46",
        "hover": "#3e3e42", "button": "#3f3f46", "button_hover": "#4b4b52", "button_text": "#f1f1f1",
        "text": "#dcdcdc", "strong": "#ffffff", "muted": "#858585", "nav_text": "#bdbdbd",
        "item": "#2d2d30", "item_border": "#333337", "item_hover": "#333337",
        "accent_text": "#ffffff", "disabled_bg": "#333337", "disabled_text": "#6d6d70",
        "menu": "#1b1b1c", "viewport": "#1e1e1e", "grid": "#2a2a2d", "tag": "#4ec9b0",
        "scroll": "#4b4b52", "star": "#f5c342", "danger": "#c53b3b", "sidebar_border": "#1e1e1e",
    },
    "Light": {
        "bg": "#f5f5f5", "base": "#ffffff", "panel": "#eeeef2", "border": "#cccedb",
        "hover": "#dcdce2", "button": "#e1e1e6", "button_hover": "#d3d3da", "button_text": "#1e1e1e",
        "text": "#1e1e1e", "strong": "#000000", "muted": "#717171", "nav_text": "#444444",
        "item": "#ffffff", "item_border": "#dcdce2", "item_hover": "#eef3fa",
        "accent_text": "#ffffff", "disabled_bg": "#ececf0", "disabled_text": "#a0a0a0",
        "menu": "#ffffff", "viewport": "#f0f0f0", "grid": "#dcdcdc", "tag": "#00897b",
        "scroll": "#c2c3c9", "star": "#d89b00", "danger": "#d9534f", "sidebar_border": "#cccedb",
    },
}

TEMPLATE = Template("""
QWidget { background-color: $bg; color: $text; font-family: "Segoe UI", "Roboto", "Helvetica Neue", Arial, sans-serif; font-size: ${font_size}px; }
QLabel { background: transparent; }
QMainWindow, QDialog { background-color: $panel; }
QFrame#sidebar { background-color: $panel; border-right: 1px solid $sidebar_border; }
QPushButton { background-color: $button; border: none; border-radius: 0; padding: 7px 16px; color: $button_text; }
QPushButton:hover { background-color: $button_hover; }
QPushButton:pressed { background-color: $accent; color: $accent_text; }
QPushButton:disabled { color: $disabled_text; background-color: $disabled_bg; }
QPushButton#nav { background: transparent; border-left: 4px solid transparent; text-align: left; padding: 11px 16px; font-size: ${nav_size}px; color: $nav_text; }
QPushButton#nav:hover { background-color: $hover; color: $strong; }
QPushButton#nav:checked { background-color: $base; color: $strong; border-left: 4px solid $accent; }
QPushButton#flat { background: transparent; text-align: left; padding: 8px 16px; color: $nav_text; }
QPushButton#flat:hover { color: $strong; background-color: $hover; }
QPushButton#star { background: transparent; font-size: 18px; padding: 2px; color: $star; }
QPushButton#primary { background-color: $accent; color: $accent_text; }
QPushButton#primary:hover { background-color: $accent_hover; }
QPushButton#danger:hover { background-color: $danger; color: #ffffff; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QPlainTextEdit { background-color: $base; border: 1px solid $border; border-radius: 0; padding: 5px 8px; selection-background-color: $select; selection-color: $select_text; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus { border: 1px solid $accent; }
QComboBox QAbstractItemView { background-color: $panel; selection-background-color: $select; selection-color: $select_text; border: 1px solid $border; }
QCheckBox, QRadioButton { background: transparent; }
QListWidget, QTreeWidget { background-color: $base; border: 1px solid $border; border-radius: 0; outline: none; }
QListWidget::item { background-color: $item; border: 1px solid $item_border; border-radius: 0; margin: 0 0 2px 0; }
QListWidget::item:hover { background-color: $item_hover; }
QListWidget::item:selected { background-color: $select; border: 1px solid $accent; }
QTreeWidget::item { padding: 3px; }
QTreeWidget::item:selected { background-color: $select; color: $select_text; }
QHeaderView::section { background-color: $panel; border: none; padding: 4px 8px; }
QLabel#logo { font-size: 20px; font-weight: bold; color: $strong; }
QLabel#logoSub { font-size: 10px; letter-spacing: 3px; color: $accent; }
QLabel#pageTitle { font-size: ${title_size}px; font-weight: 300; color: $strong; }
QLabel#projectName { font-size: ${name_size}px; font-weight: bold; color: $strong; }
QLabel#projectPath, QLabel#hint { color: $muted; }
QLabel#tags { color: $tag; }
QLabel#badge { background-color: $accent; padding: 2px 8px; color: $accent_text; }
QLabel#badgeAlt { background-color: $button; padding: 2px 8px; color: $button_text; }
QGroupBox { border: 1px solid $border; border-radius: 0; margin-top: 12px; padding: 14px 10px 10px 10px; }
QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 4px; color: $accent; }
QMenuBar { background-color: $panel; }
QMenuBar::item { padding: 5px 10px; background: transparent; }
QMenuBar::item:selected, QMenu::item:selected { background-color: $hover; }
QMenu { background-color: $menu; border: 1px solid $border; }
QMenu::item { padding: 5px 24px; }
QToolBar { background-color: $panel; border: none; spacing: 4px; padding: 4px; }
QToolButton { background-color: transparent; border: none; border-radius: 0; padding: 6px 12px; }
QToolButton:hover { background-color: $hover; }
QToolButton:pressed { background-color: $accent; color: $accent_text; }
QToolButton#tile { color: #ffffff; border: 2px solid transparent; padding: 8px 4px; font-size: 12px; }
QToolButton#tile:hover { border: 2px solid rgba(255, 255, 255, 150); }
QToolButton#tile:pressed { padding-top: 11px; }
QToolButton#tile[tone="open"] { background-color: #1ba1e2; }
QToolButton#tile[tone="launch"] { background-color: #60a917; }
QToolButton#tile[tone="rename"] { background-color: #f0a30a; }
QToolButton#tile[tone="clone"] { background-color: #aa00ff; }
QToolButton#tile[tone="tags"] { background-color: #d80073; }
QToolButton#tile[tone="remove"] { background-color: #e51400; }
QToolButton#tile[tone="clean"] { background-color: #647687; }
QToolButton#tile:disabled { background-color: $disabled_bg; color: $disabled_text; }
QDockWidget::title { background-color: $panel; padding: 6px; border-bottom: 1px solid $border; }
QTabWidget::pane { border: 1px solid $border; }
QTabBar::tab { background-color: $panel; padding: 6px 18px; border: none; border-top: 2px solid transparent; color: $nav_text; }
QTabBar::tab:selected { background-color: $base; border-top: 2px solid $accent; color: $strong; }
QStatusBar { background-color: $accent; color: $accent_text; }
QScrollBar:vertical { background: $base; width: 12px; }
QScrollBar::handle:vertical { background: $scroll; min-height: 24px; }
QScrollBar::add-line, QScrollBar::sub-line { height: 0; width: 0; }
""")


def mix(a, b, amount):
    ca = QColor(a)
    cb = QColor(b)
    return QColor(
        int(ca.red() * amount + cb.red() * (1 - amount)),
        int(ca.green() * amount + cb.green() * (1 - amount)),
        int(ca.blue() * amount + cb.blue() * (1 - amount)),
    ).name()


def palette():
    s = settings.current
    colors = dict(PALETTES.get(s.theme, PALETTES["Dark"]))
    accent, hover = ACCENT_COLORS.get(s.accent, ACCENT_COLORS["Blue"])
    dark = s.theme != "Light"
    colors["accent"] = accent
    colors["accent_hover"] = hover
    colors["select"] = mix(accent, colors["base"], 0.4) if dark else mix(accent, "#ffffff", 0.2)
    colors["select_text"] = "#ffffff" if dark else "#000000"
    colors["font_size"] = s.font_size
    colors["nav_size"] = s.font_size + 1
    colors["name_size"] = s.font_size + 2
    colors["title_size"] = s.font_size + 11
    return colors


def build_style():
    return TEMPLATE.substitute(palette())


def apply_theme():
    app = QApplication.instance()
    if app is not None:
        app.setStyleSheet(build_style())


def make_pixmap(size, color=None):
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(color or palette()["accent"]))
    p.drawRect(QRectF(0, 0, size, size))
    font = QFont("Sans Serif")
    font.setBold(True)
    font.setPixelSize(int(size * 0.62))
    p.setFont(font)
    p.setPen(QColor("#ffffff"))
    p.drawText(QRectF(0, 0, size, size), Qt.AlignmentFlag.AlignCenter, "B")
    p.end()
    return pix


def make_icon(size=64):
    return QIcon(make_pixmap(size))
