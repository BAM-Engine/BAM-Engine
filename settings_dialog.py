from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox, QComboBox, QDialog, QFileDialog, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSpinBox, QTabWidget, QVBoxLayout, QWidget,
)

import settings
from icons import attach, refresh_icons
from theme import apply_theme


class SettingsDialog(QDialog):
    applied = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("BAM Settings")
        self.setMinimumSize(540, 400)
        layout = QVBoxLayout(self)

        tabs = QTabWidget()

        general = QWidget()
        general_form = QFormLayout(general)
        self.ui_language = QComboBox()
        self.ui_language.addItems(settings.UI_LANGUAGES)
        self.path_edit = QLineEdit()
        browse = QPushButton("Browse")
        browse.clicked.connect(self.browse)
        attach(browse, "folder")
        path_row = QHBoxLayout()
        path_row.addWidget(self.path_edit, 1)
        path_row.addWidget(browse)
        self.check_updates = QCheckBox("Check for updates on startup")
        self.confirm_remove = QCheckBox("Ask before removing a project from the list")
        general_form.addRow("Interface Language:", self.ui_language)
        general_form.addRow("Default Project Path:", path_row)
        general_form.addRow("", self.check_updates)
        general_form.addRow("", self.confirm_remove)
        tabs.addTab(general, "General")

        appearance = QWidget()
        appearance_form = QFormLayout(appearance)
        self.theme = QComboBox()
        self.theme.addItems(settings.THEMES)
        self.accent = QComboBox()
        self.accent.addItems(settings.ACCENTS)
        self.font_size = QSpinBox()
        self.font_size.setRange(10, 20)
        self.font_size.setSuffix(" px")
        appearance_form.addRow("Theme:", self.theme)
        appearance_form.addRow("Accent Color:", self.accent)
        appearance_form.addRow("Font Size:", self.font_size)
        tabs.addTab(appearance, "Appearance")

        defaults = QWidget()
        defaults_form = QFormLayout(defaults)
        self.renderer = QComboBox()
        self.renderer.addItems(settings.RENDERERS)
        self.language = QComboBox()
        self.language.addItems(settings.LANGUAGES)
        defaults_form.addRow("Default Renderer:", self.renderer)
        defaults_form.addRow("Default Scripting Language:", self.language)
        tabs.addTab(defaults, "New Projects")

        editor = QWidget()
        editor_form = QFormLayout(editor)
        self.autosave = QSpinBox()
        self.autosave.setRange(0, 60)
        self.autosave.setSuffix(" min")
        self.autosave.setSpecialValueText("Off")
        self.show_hints = QCheckBox("Show tips in the output panel")
        editor_form.addRow("Autosave Interval:", self.autosave)
        editor_form.addRow("", self.show_hints)
        tabs.addTab(editor, "Editor")

        layout.addWidget(tabs, 1)

        note = QLabel("Settings last for this session only and are not saved to disk.")
        note.setObjectName("hint")
        layout.addWidget(note)

        buttons = QHBoxLayout()
        reset = QPushButton("Reset to Defaults")
        reset.clicked.connect(lambda: self.load_values(settings.Settings()))
        attach(reset, "refresh")
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        attach(cancel, "close")
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply)
        attach(apply_button, "check")
        ok = QPushButton("OK")
        ok.setObjectName("primary")
        ok.clicked.connect(self.accept_and_apply)
        attach(ok, "check", "white")
        buttons.addWidget(reset)
        buttons.addStretch()
        buttons.addWidget(cancel)
        buttons.addWidget(apply_button)
        buttons.addWidget(ok)
        layout.addLayout(buttons)

        self.load_values(settings.current)

    def browse(self):
        chosen = QFileDialog.getExistingDirectory(self, "Select Default Project Folder", self.path_edit.text())
        if chosen:
            self.path_edit.setText(chosen)

    def load_values(self, s):
        self.ui_language.setCurrentText(s.ui_language)
        self.path_edit.setText(s.default_path)
        self.check_updates.setChecked(s.check_updates)
        self.confirm_remove.setChecked(s.confirm_remove)
        self.theme.setCurrentText(s.theme)
        self.accent.setCurrentText(s.accent)
        self.font_size.setValue(s.font_size)
        self.renderer.setCurrentText(s.default_renderer)
        self.language.setCurrentText(s.default_language)
        self.autosave.setValue(s.autosave_minutes)
        self.show_hints.setChecked(s.show_hints)

    def apply(self):
        s = settings.current
        s.ui_language = self.ui_language.currentText()
        s.default_path = self.path_edit.text().strip() or s.default_path
        s.check_updates = self.check_updates.isChecked()
        s.confirm_remove = self.confirm_remove.isChecked()
        s.theme = self.theme.currentText()
        s.accent = self.accent.currentText()
        s.font_size = self.font_size.value()
        s.default_renderer = self.renderer.currentText()
        s.default_language = self.language.currentText()
        s.autosave_minutes = self.autosave.value()
        s.show_hints = self.show_hints.isChecked()
        apply_theme()
        refresh_icons()
        self.applied.emit()

    def accept_and_apply(self):
        self.apply()
        self.accept()
