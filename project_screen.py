import copy
import os
import re
from datetime import datetime

from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QButtonGroup, QCheckBox, QComboBox, QDialog, QFileDialog, QFormLayout, QFrame,
    QGroupBox, QHBoxLayout, QInputDialog, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMessageBox, QPushButton, QRadioButton,
    QSpinBox, QStackedWidget, QToolButton, QVBoxLayout, QWidget,
)

import settings
from models import ENGINE_VERSION, Project, build_entities, example_projects
from settings_dialog import SettingsDialog
from icons import attach
from theme import METRO_COLORS, make_icon, make_pixmap

RENDERER_INFO = [
    ("P.E.A.K.", "High-end renderer for desktop GPUs. Dynamic lights, shadows and post-processing."),
    ("Light", "Lightweight renderer for low-end, mobile and web targets. Fewer effects, faster startup."),
]


class ProjectRow(QWidget):
    favorite_changed = pyqtSignal()

    def __init__(self, project):
        super().__init__()
        self.project = project
        self.setObjectName("projectRow")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 16, 8)
        layout.setSpacing(14)

        self.star = QPushButton("★" if project.favorite else "☆")
        self.star.setObjectName("star")
        self.star.setCheckable(True)
        self.star.setChecked(project.favorite)
        self.star.setCursor(Qt.CursorShape.PointingHandCursor)
        self.star.toggled.connect(self.toggle_favorite)

        icon = QLabel()
        icon.setPixmap(make_pixmap(52, METRO_COLORS[sum(ord(ch) for ch in project.name) % len(METRO_COLORS)]))

        info = QVBoxLayout()
        info.setSpacing(4)
        title_row = QHBoxLayout()
        name = QLabel(project.name)
        name.setObjectName("projectName")
        title_row.addWidget(name)
        if project.tags:
            tags = QLabel("  ".join("#" + t for t in project.tags))
            tags.setObjectName("tags")
            title_row.addWidget(tags)
        title_row.addStretch()
        path = QLabel(project.path)
        path.setObjectName("projectPath")
        info.addLayout(title_row)
        info.addWidget(path)

        version = QLabel("v" + project.version)
        version.setObjectName("badge")
        renderer = QLabel(project.renderer)
        renderer.setObjectName("badgeAlt")
        edited = QLabel(project.edited)
        edited.setObjectName("projectPath")

        layout.addWidget(self.star)
        layout.addWidget(icon)
        layout.addLayout(info, 1)
        layout.addWidget(renderer)
        layout.addWidget(version)
        layout.addWidget(edited)

    def toggle_favorite(self, checked):
        self.project.favorite = checked
        self.star.setText("★" if checked else "☆")
        self.favorite_changed.emit()


class CreateProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Project")
        self.setMinimumWidth(580)
        self.base = settings.current.default_path

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        form = QFormLayout()
        self.name_edit = QLineEdit("New BAM Project")
        self.name_edit.textChanged.connect(self.update_path)
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        browse = QPushButton("Browse")
        browse.clicked.connect(self.browse)
        attach(browse, "folder")
        path_row = QHBoxLayout()
        path_row.addWidget(self.path_edit, 1)
        path_row.addWidget(browse)
        self.template = QComboBox()
        self.template.addItems(["Empty", "2D Platformer", "3D Starter"])
        self.language = QComboBox()
        self.language.addItems(settings.LANGUAGES)
        self.language.setCurrentText(settings.current.default_language)
        self.vcs = QComboBox()
        self.vcs.addItems(["None", "Git"])
        form.addRow("Project Name:", self.name_edit)
        form.addRow("Location:", path_row)
        form.addRow("Template:", self.template)
        form.addRow("Scripting Language:", self.language)
        form.addRow("Version Control:", self.vcs)
        layout.addLayout(form)

        renderer_box = QGroupBox("Renderer")
        renderer_layout = QVBoxLayout(renderer_box)
        self.renderer_group = QButtonGroup(self)
        for title, hint in RENDERER_INFO:
            radio = QRadioButton(title)
            radio.setChecked(title == settings.current.default_renderer)
            self.renderer_group.addButton(radio)
            description = QLabel(hint)
            description.setObjectName("hint")
            description.setWordWrap(True)
            description.setContentsMargins(24, 0, 0, 4)
            renderer_layout.addWidget(radio)
            renderer_layout.addWidget(description)
        if self.renderer_group.checkedButton() is None:
            self.renderer_group.buttons()[0].setChecked(True)
        layout.addWidget(renderer_box)

        display_box = QGroupBox("Display")
        display_layout = QHBoxLayout(display_box)
        self.width_spin = QSpinBox()
        self.width_spin.setRange(64, 8192)
        self.width_spin.setValue(1152)
        self.height_spin = QSpinBox()
        self.height_spin.setRange(64, 8192)
        self.height_spin.setValue(648)
        self.vsync = QCheckBox("VSync")
        self.vsync.setChecked(True)
        display_layout.addWidget(QLabel("Width:"))
        display_layout.addWidget(self.width_spin)
        display_layout.addWidget(QLabel("Height:"))
        display_layout.addWidget(self.height_spin)
        display_layout.addStretch()
        display_layout.addWidget(self.vsync)
        layout.addWidget(display_box)

        note = QLabel("Proof of concept: this project lives in memory only and is never written to disk.")
        note.setObjectName("hint")
        note.setWordWrap(True)
        layout.addWidget(note)

        buttons = QHBoxLayout()
        buttons.addStretch()
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        attach(cancel, "close")
        create = QPushButton("Create && Open")
        create.setObjectName("primary")
        attach(create, "check", "white")
        create.setDefault(True)
        create.clicked.connect(self.try_accept)
        buttons.addWidget(cancel)
        buttons.addWidget(create)
        layout.addLayout(buttons)

        self.update_path()

    def slug(self):
        text = re.sub(r"[^a-z0-9]+", "_", self.name_edit.text().lower()).strip("_")
        return text or "project"

    def update_path(self):
        self.path_edit.setText(os.path.join(self.base, self.slug()))

    def browse(self):
        chosen = QFileDialog.getExistingDirectory(self, "Select Project Folder", self.base)
        if chosen:
            self.base = chosen
            self.update_path()

    def try_accept(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Invalid Name", "Please enter a project name.")
            return
        self.accept()

    def project(self):
        checked = self.renderer_group.checkedButton()
        template = self.template.currentText()
        return Project(
            name=self.name_edit.text().strip(),
            path=self.path_edit.text(),
            version=ENGINE_VERSION,
            edited=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            renderer=checked.text() if checked else "P.E.A.K.",
            template=template,
            language=self.language.currentText(),
            width=self.width_spin.value(),
            height=self.height_spin.value(),
            vsync=self.vsync.isChecked(),
            version_control=self.vcs.currentText(),
            entities=build_entities(template),
        )


class ProjectManager(QMainWindow):
    project_opened = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BAM Engine - Projects")
        self.setWindowIcon(make_icon(64))
        self.resize(1160, 660)
        self.projects = example_projects()
        self.visible = []
        self.build_ui()
        self.refresh()

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(210)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(0, 18, 0, 12)
        side.setSpacing(2)

        brand = QHBoxLayout()
        brand.setContentsMargins(16, 0, 16, 0)
        self.logo_icon = QLabel()
        self.logo_icon.setPixmap(make_pixmap(40))
        titles = QVBoxLayout()
        titles.setSpacing(0)
        logo_text = QLabel("BAM")
        logo_text.setObjectName("logo")
        logo_sub = QLabel("ENGINE")
        logo_sub.setObjectName("logoSub")
        titles.addWidget(logo_text)
        titles.addWidget(logo_sub)
        brand.addWidget(self.logo_icon)
        brand.addLayout(titles)
        brand.addStretch()
        side.addLayout(brand)
        side.addSpacing(22)

        self.tab_projects = QPushButton("Projects")
        self.tab_market = QPushButton("Marketplace")
        group = QButtonGroup(self)
        group.setExclusive(True)
        for tab in (self.tab_projects, self.tab_market):
            tab.setObjectName("nav")
            tab.setCheckable(True)
            group.addButton(tab)
            side.addWidget(tab)
        self.tab_projects.setChecked(True)
        attach(self.tab_projects, "grid", "toolbar", 20)
        attach(self.tab_market, "store", "toolbar", 20)
        side.addStretch()

        settings_button = QPushButton("Settings")
        settings_button.setObjectName("flat")
        settings_button.clicked.connect(self.show_settings)
        attach(settings_button, "gear", "toolbar", 20)
        donate = QPushButton("Support BAM")
        donate.setObjectName("flat")
        donate.clicked.connect(self.donate)
        attach(donate, "heart", "toolbar", 20)
        side.addWidget(settings_button)
        side.addWidget(donate)
        root.addWidget(sidebar)

        self.pages = QStackedWidget()
        self.pages.addWidget(self.build_projects_page())
        self.pages.addWidget(self.build_market_page())
        root.addWidget(self.pages, 1)

        self.tab_projects.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.tab_market.clicked.connect(lambda: self.pages.setCurrentIndex(1))

        self.statusBar().showMessage("BAM Engine v" + ENGINE_VERSION + " - proof of concept")

    def build_market_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel("The Marketplace is not available in this proof of concept.")
        label.setObjectName("hint")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        return page

    def build_projects_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(22, 18, 22, 16)
        layout.setSpacing(12)

        top = QHBoxLayout()
        title = QLabel("Projects")
        title.setObjectName("pageTitle")
        top.addWidget(title)
        top.addStretch()
        create_btn = QPushButton("New Project")
        create_btn.setObjectName("primary")
        import_btn = QPushButton("Import")
        find_btn = QPushButton("Find Projects")
        create_btn.clicked.connect(self.create_project)
        import_btn.clicked.connect(self.import_project)
        find_btn.clicked.connect(self.find_projects)
        attach(create_btn, "plus", "white")
        attach(import_btn, "import")
        attach(find_btn, "search")
        top.addWidget(find_btn)
        top.addWidget(import_btn)
        top.addWidget(create_btn)
        layout.addLayout(top)

        search = QHBoxLayout()
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("Search projects by name or location")
        self.filter_edit.setClearButtonEnabled(True)
        self.filter_edit.textChanged.connect(self.refresh)
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Recently Opened", "Name", "Location"])
        self.sort_combo.currentIndexChanged.connect(self.refresh)
        search.addWidget(self.filter_edit, 1)
        search.addWidget(QLabel("Sort by"))
        search.addWidget(self.sort_combo)
        layout.addLayout(search)

        self.list = QListWidget()
        self.list.currentRowChanged.connect(self.update_buttons)
        self.list.itemDoubleClicked.connect(lambda item: self.open_selected())
        layout.addWidget(self.list, 1)

        bar = QHBoxLayout()
        bar.setSpacing(8)
        self.buttons = {}
        tiles = [
            ("Open", "open", "folder", self.open_selected),
            ("Launch", "launch", "launch", self.launch_selected),
            ("Rename", "rename", "pencil", self.rename_selected),
            ("Clone", "clone", "clone", self.clone_selected),
            ("Edit Tags", "tags", "tag", self.tags_selected),
            ("Remove", "remove", "trash", self.remove_selected),
            ("Clean Up", "clean", "refresh", self.clean_missing),
        ]
        for label, tone, glyph, handler in tiles:
            if label == "Clean Up":
                bar.addStretch()
            button = QToolButton()
            button.setObjectName("tile")
            button.setProperty("tone", tone)
            button.setText(label)
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            button.setFixedSize(104, 88)
            button.clicked.connect(handler)
            attach(button, glyph, "white", 30)
            bar.addWidget(button)
            self.buttons[label] = button
        self.buttons["Clean Up"].setToolTip("Remove missing projects from the list")
        layout.addLayout(bar)
        return page

    def current_project(self):
        row = self.list.currentRow()
        if 0 <= row < len(self.visible):
            return self.visible[row]
        return None

    def update_buttons(self):
        has_selection = self.current_project() is not None
        for label, button in self.buttons.items():
            if label == "Clean Up":
                continue
            button.setEnabled(has_selection)

    def refresh(self):
        selected = self.current_project()
        text = self.filter_edit.text().strip().lower()
        items = [p for p in self.projects if text in p.name.lower() or text in p.path.lower()]
        mode = self.sort_combo.currentText()
        if mode == "Recently Opened":
            items.sort(key=lambda p: p.edited, reverse=True)
        elif mode == "Name":
            items.sort(key=lambda p: p.name.lower())
        else:
            items.sort(key=lambda p: p.path.lower())
        items.sort(key=lambda p: not p.favorite)
        self.visible = items

        self.list.blockSignals(True)
        self.list.clear()
        for project in items:
            item = QListWidgetItem(self.list)
            item.setSizeHint(QSize(0, 78))
            row = ProjectRow(project)
            row.favorite_changed.connect(lambda: QTimer.singleShot(0, self.refresh))
            self.list.setItemWidget(item, row)
        index = next((i for i, p in enumerate(items) if p is selected), -1)
        self.list.setCurrentRow(index)
        self.list.blockSignals(False)
        self.update_buttons()

    def open_project(self, project):
        project.edited = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.project_opened.emit(project)

    def show_again(self):
        self.refresh()
        self.show()
        self.raise_()

    def create_project(self):
        dialog = CreateProjectDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            project = dialog.project()
            self.projects.append(project)
            self.refresh()
            self.open_project(project)

    def import_project(self):
        folder = QFileDialog.getExistingDirectory(self, "Import Project Folder", settings.current.default_path)
        if not folder:
            return
        project = Project(
            name=os.path.basename(folder.rstrip("/\\")) or "Imported Project",
            path=folder,
            renderer=settings.current.default_renderer,
            edited=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self.projects.append(project)
        self.refresh()
        self.statusBar().showMessage("Imported " + project.name + " (in memory only)", 4000)

    def find_projects(self):
        QMessageBox.information(self, "Find Projects", "Search finished. No new projects found in " + settings.current.default_path)

    def open_selected(self):
        project = self.current_project()
        if project:
            self.open_project(project)

    def launch_selected(self):
        project = self.current_project()
        if project:
            QMessageBox.information(self, "Launch", "Launching " + project.name + " with the " + project.renderer + " renderer...\n\n(Proof of concept: use Open to see the editor.)")

    def rename_selected(self):
        project = self.current_project()
        if not project:
            return
        text, ok = QInputDialog.getText(self, "Rename Project", "New name:", text=project.name)
        if ok and text.strip():
            project.name = text.strip()
            self.refresh()

    def clone_selected(self):
        project = self.current_project()
        if not project:
            return
        clone = copy.deepcopy(project)
        clone.name = project.name + " Copy"
        clone.path = project.path + "_copy"
        clone.favorite = False
        clone.edited = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.projects.append(clone)
        self.refresh()

    def tags_selected(self):
        project = self.current_project()
        if not project:
            return
        text, ok = QInputDialog.getText(self, "Edit Tags", "Tags (comma separated):", text=", ".join(project.tags))
        if ok:
            project.tags = [t.strip() for t in text.split(",") if t.strip()]
            self.refresh()

    def remove_selected(self):
        project = self.current_project()
        if not project:
            return
        if settings.current.confirm_remove:
            answer = QMessageBox.question(self, "Remove Project", "Remove " + project.name + " from the list?\n\nNothing is deleted from disk.")
            if answer != QMessageBox.StandardButton.Yes:
                return
        self.projects = [p for p in self.projects if p is not project]
        self.refresh()

    def clean_missing(self):
        QMessageBox.information(self, "Clean Up Missing", "No missing projects found.")

    def donate(self):
        QMessageBox.information(self, "Support BAM", "Thanks for the thought! This is only a proof of concept.")

    def show_settings(self):
        dialog = SettingsDialog(self)
        dialog.applied.connect(self.on_settings_applied)
        dialog.exec()

    def on_settings_applied(self):
        self.logo_icon.setPixmap(make_pixmap(40))
        self.refresh()