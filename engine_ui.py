import math
from datetime import datetime

from PyQt6.QtCore import QPointF, QRectF, QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import (
    QApplication, QColorDialog, QDockWidget, QDoubleSpinBox, QFormLayout,
    QLabel, QLineEdit, QMainWindow, QMessageBox, QPlainTextEdit, QPushButton,
    QSizePolicy, QTabWidget, QToolBar, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget,
)

import settings
from icons import attach
from models import Entity
from settings_dialog import SettingsDialog
from theme import make_icon, palette


class Viewport(QWidget):
    selection_changed = pyqtSignal(int)
    entity_moved = pyqtSignal(int)

    def __init__(self, entities):
        super().__init__()
        self.entities = entities
        self.selected = -1
        self.playing = False
        self.phase = 0.0
        self.drag_offset = None
        self.setMinimumSize(420, 300)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)

    def tick(self):
        if self.playing:
            self.phase += 0.08
            self.update()

    def offset_for(self, index, entity):
        if self.playing and not entity.static:
            return math.sin(self.phase + index) * 8
        return 0.0

    def entity_rect(self, index, entity):
        return QRectF(entity.x, entity.y + self.offset_for(index, entity), entity.w, entity.h)

    def paintEvent(self, event):
        colors = palette()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor(colors["viewport"]))
        p.setPen(QPen(QColor(colors["grid"]), 1))
        for x in range(0, self.width(), 32):
            p.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), 32):
            p.drawLine(0, y, self.width(), y)
        p.setPen(QPen(QColor("#d9534f"), 1))
        p.drawLine(0, 0, self.width(), 0)
        p.setPen(QPen(QColor("#5cb85c"), 1))
        p.drawLine(0, 0, 0, self.height())

        for i, entity in enumerate(self.entities):
            rect = self.entity_rect(i, entity)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QColor(entity.color))
            if entity.kind == "Circle":
                p.drawEllipse(rect)
            else:
                p.drawRect(rect)
            p.setPen(QColor("#ffffff"))
            p.drawText(rect, Qt.AlignmentFlag.AlignCenter, entity.name)
            if i == self.selected:
                pen = QPen(QColor(colors["accent"]), 2, Qt.PenStyle.DashLine)
                p.setPen(pen)
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.drawRect(rect.adjusted(-4, -4, 4, 4))

        if self.playing:
            font = QFont()
            font.setBold(True)
            p.setFont(font)
            p.setPen(QColor(colors["tag"]))
            p.drawText(12, 22, "RUNNING")

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton or self.playing:
            return
        pos = event.position()
        hit = -1
        for i in range(len(self.entities) - 1, -1, -1):
            if self.entity_rect(i, self.entities[i]).contains(pos):
                hit = i
                break
        self.selected = hit
        if hit >= 0:
            entity = self.entities[hit]
            self.drag_offset = QPointF(pos.x() - entity.x, pos.y() - entity.y)
        else:
            self.drag_offset = None
        self.selection_changed.emit(hit)
        self.update()

    def mouseMoveEvent(self, event):
        if self.drag_offset is None or self.selected < 0:
            return
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        pos = event.position()
        entity = self.entities[self.selected]
        entity.x = pos.x() - self.drag_offset.x()
        entity.y = pos.y() - self.drag_offset.y()
        self.entity_moved.emit(self.selected)
        self.update()

    def mouseReleaseEvent(self, event):
        self.drag_offset = None


class EngineWindow(QMainWindow):
    back_to_manager = pyqtSignal()

    def __init__(self, project):
        super().__init__()
        self.project = project
        self.loading = False
        self.setWindowTitle(project.name + " - BAM Engine")
        self.setWindowIcon(make_icon(64))
        self.resize(1320, 780)

        self.viewport = Viewport(project.entities)
        self.viewport.selection_changed.connect(self.on_viewport_select)
        self.viewport.entity_moved.connect(self.load_inspector)

        self.autosave = QTimer(self)
        self.autosave.timeout.connect(self.on_autosave)

        self.build_menu()
        self.build_toolbar()
        self.build_center()
        self.build_hierarchy_dock()
        self.build_properties_dock()
        self.build_bottom_docks()
        self.populate_tree()
        self.load_inspector(-1)
        self.restart_autosave()

        self.statusBar().showMessage("BAM Engine v0.1 | " + project.renderer + " renderer | " + str(project.width) + "x" + str(project.height))
        self.log("Project '" + project.name + "' opened")
        self.log("Renderer: " + project.renderer + ", scripting: " + project.language)
        self.log("Nothing in this session is saved to disk")
        if settings.current.show_hints:
            self.log("Tip: click a shape in the 2D View and drag it to move it")

    def log(self, text):
        self.console.appendPlainText("[" + datetime.now().strftime("%H:%M:%S") + "] " + text)

    def restart_autosave(self):
        self.autosave.stop()
        minutes = settings.current.autosave_minutes
        if minutes > 0:
            self.autosave.start(minutes * 60000)

    def on_autosave(self):
        self.log("Autosave skipped: project is in memory only")

    def build_menu(self):
        bar = self.menuBar()

        file_menu = bar.addMenu("File")
        save = QAction("Save", self)
        save.setShortcut("Ctrl+S")
        save.triggered.connect(self.save_project)
        settings_action = QAction("Settings...", self)
        settings_action.triggered.connect(self.open_settings)
        back = QAction("Close Project", self)
        back.triggered.connect(self.close)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        attach(save, "save", "toolbar", 0)
        attach(settings_action, "gear", "toolbar", 0)
        attach(back, "close", "toolbar", 0)
        attach(exit_action, "exit", "toolbar", 0)
        file_menu.addAction(save)
        file_menu.addAction(settings_action)
        file_menu.addSeparator()
        file_menu.addAction(back)
        file_menu.addAction(exit_action)

        objects_menu = bar.addMenu("Objects")
        add_rect = QAction("Add Rectangle", self)
        add_rect.triggered.connect(lambda: self.add_entity("Rectangle"))
        add_circle = QAction("Add Circle", self)
        add_circle.triggered.connect(lambda: self.add_entity("Circle"))
        delete = QAction("Delete Selected", self)
        delete.setShortcut("Delete")
        delete.triggered.connect(self.delete_selected)
        attach(add_rect, "rect", "toolbar", 0)
        attach(add_circle, "circle", "toolbar", 0)
        attach(delete, "trash", "toolbar", 0)
        objects_menu.addAction(add_rect)
        objects_menu.addAction(add_circle)
        objects_menu.addSeparator()
        objects_menu.addAction(delete)

        help_menu = bar.addMenu("Help")
        about = QAction("About BAM Engine", self)
        about.triggered.connect(self.show_about)
        attach(about, "info", "toolbar", 0)
        help_menu.addAction(about)

    def build_toolbar(self):
        top = QToolBar("Run")
        top.setMovable(False)
        top.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        top.setIconSize(QSize(18, 18))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, top)
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        left_spacer.setStyleSheet("background: transparent;")
        top.addWidget(left_spacer)
        for label, glyph, handler in [("Start", "play", self.play), ("Pause", "pause", self.pause), ("Stop", "stop", self.stop)]:
            action = QAction(label, self)
            attach(action, glyph, "toolbar", 0)
            action.triggered.connect(handler)
            top.addAction(action)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        right_spacer.setStyleSheet("background: transparent;")
        top.addWidget(right_spacer)

        tools = QToolBar("Tools")
        tools.setMovable(False)
        tools.setIconSize(QSize(22, 22))
        tools.setOrientation(Qt.Orientation.Vertical)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, tools)
        for label, tip, handler in [
            ("rect", "Add Rectangle", lambda: self.add_entity("Rectangle")),
            ("circle", "Add Circle", lambda: self.add_entity("Circle")),
            ("trash", "Delete Selected", self.delete_selected),
        ]:
            action = QAction(self)
            attach(action, label, "toolbar", 0)
            action.setToolTip(tip)
            action.triggered.connect(handler)
            tools.addAction(action)

    def build_center(self):
        tabs = QTabWidget()
        tabs.addTab(self.viewport, "2D View")

        view3d = QLabel("The 3D View is not implemented in this proof of concept.")
        view3d.setObjectName("hint")
        view3d.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tabs.addTab(view3d, "3D View")

        script = QPlainTextEdit()
        mono = QFont("Monospace")
        mono.setStyleHint(QFont.StyleHint.Monospace)
        script.setFont(mono)
        script.setPlainText(
            "class Player : Entity2D\n\n"
            "speed = 220\n\n"
            "on_start():\n"
            "    log(\"Hello from BAM\")\n\n"
            "on_update(dt):\n"
            "    position.x += speed * dt\n"
        )
        tabs.addTab(script, "Code")
        self.setCentralWidget(tabs)

    def build_hierarchy_dock(self):
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.currentItemChanged.connect(self.on_tree_select)
        dock = QDockWidget("Hierarchy", self)
        dock.setWidget(self.tree)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        self.hierarchy_dock = dock

    def build_properties_dock(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        form = QFormLayout()
        self.name_edit = QLineEdit()
        self.name_edit.editingFinished.connect(self.apply_inspector)
        self.kind_label = QLabel("-")
        self.spins = {}
        for key in ("x", "y", "w", "h"):
            spin = QDoubleSpinBox()
            spin.setRange(-10000, 10000)
            spin.setDecimals(1)
            spin.valueChanged.connect(self.apply_inspector)
            self.spins[key] = spin
        self.color_button = QPushButton()
        self.color_button.clicked.connect(self.pick_color)
        form.addRow("Name", self.name_edit)
        form.addRow("Type", self.kind_label)
        form.addRow("Position X", self.spins["x"])
        form.addRow("Position Y", self.spins["y"])
        form.addRow("Width", self.spins["w"])
        form.addRow("Height", self.spins["h"])
        form.addRow("Color", self.color_button)
        layout.addLayout(form)
        layout.addStretch()
        self.inspector_container = container

        dock = QDockWidget("Properties", self)
        dock.setWidget(container)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        self.properties_dock = dock
        self.resizeDocks([self.hierarchy_dock, dock], [260, 300], Qt.Orientation.Horizontal)

    def build_bottom_docks(self):
        files = QTreeWidget()
        files.setHeaderLabel("project://")
        structure = {
            "scenes": ["main.bscn"],
            "scripts": ["player.bs", "enemy.bs"],
            "assets": ["icon.svg", "tiles.png"],
        }
        for folder, children in structure.items():
            parent = QTreeWidgetItem(files, [folder])
            for child in children:
                QTreeWidgetItem(parent, [child])
        QTreeWidgetItem(files, ["project.bam"])
        files.expandAll()

        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)

        files_dock = QDockWidget("Assets", self)
        files_dock.setWidget(files)
        console_dock = QDockWidget("Output", self)
        console_dock.setWidget(self.console)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, console_dock)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, files_dock)
        self.tabifyDockWidget(console_dock, files_dock)
        console_dock.raise_()
        self.resizeDocks([console_dock], [170], Qt.Orientation.Vertical)

    def entity_label(self, entity):
        return entity.name + " (" + entity.kind + ")"

    def populate_tree(self, select=-1):
        self.tree.blockSignals(True)
        self.tree.clear()
        self.root_item = QTreeWidgetItem(self.tree, [self.project.name])
        for entity in self.project.entities:
            QTreeWidgetItem(self.root_item, [self.entity_label(entity)])
        self.root_item.setExpanded(True)
        if 0 <= select < self.root_item.childCount():
            self.tree.setCurrentItem(self.root_item.child(select))
        self.tree.blockSignals(False)

    def on_tree_select(self, current, previous):
        index = -1
        if current is not None and current.parent() is self.root_item:
            index = self.root_item.indexOfChild(current)
        self.viewport.selected = index
        self.viewport.update()
        self.load_inspector(index)

    def on_viewport_select(self, index):
        self.tree.blockSignals(True)
        if index >= 0:
            self.tree.setCurrentItem(self.root_item.child(index))
        else:
            self.tree.setCurrentItem(self.root_item)
        self.tree.blockSignals(False)
        self.load_inspector(index)

    def load_inspector(self, index):
        self.loading = True
        enabled = 0 <= index < len(self.project.entities)
        self.inspector_container.setEnabled(enabled)
        if enabled:
            entity = self.project.entities[index]
            self.name_edit.setText(entity.name)
            self.kind_label.setText(entity.kind)
            self.spins["x"].setValue(entity.x)
            self.spins["y"].setValue(entity.y)
            self.spins["w"].setValue(entity.w)
            self.spins["h"].setValue(entity.h)
            self.set_color_button(entity.color)
        else:
            self.name_edit.setText("")
            self.kind_label.setText("-")
            for spin in self.spins.values():
                spin.setValue(0)
            self.set_color_button(palette()["button"])
        self.loading = False

    def set_color_button(self, color):
        self.color_button.setText(color)
        self.color_button.setStyleSheet("background-color: " + color + "; color: #ffffff;")

    def apply_inspector(self):
        if self.loading:
            return
        index = self.viewport.selected
        if not (0 <= index < len(self.project.entities)):
            return
        entity = self.project.entities[index]
        entity.name = self.name_edit.text() or entity.name
        entity.x = self.spins["x"].value()
        entity.y = self.spins["y"].value()
        entity.w = self.spins["w"].value()
        entity.h = self.spins["h"].value()
        self.root_item.child(index).setText(0, self.entity_label(entity))
        self.viewport.update()

    def pick_color(self):
        index = self.viewport.selected
        if not (0 <= index < len(self.project.entities)):
            return
        entity = self.project.entities[index]
        color = QColorDialog.getColor(QColor(entity.color), self)
        if color.isValid():
            entity.color = color.name()
            self.set_color_button(entity.color)
            self.viewport.update()

    def add_entity(self, kind):
        number = len(self.project.entities) + 1
        entity = Entity(kind + str(number), kind, 80 + number * 20, 80 + number * 20, 80, 80, "#1c97ea")
        self.project.entities.append(entity)
        index = len(self.project.entities) - 1
        self.populate_tree(index)
        self.viewport.selected = index
        self.viewport.update()
        self.load_inspector(index)
        self.log("Added " + entity.name)

    def delete_selected(self):
        index = self.viewport.selected
        if not (0 <= index < len(self.project.entities)):
            return
        removed = self.project.entities.pop(index)
        self.viewport.selected = -1
        self.populate_tree()
        self.viewport.update()
        self.load_inspector(-1)
        self.log("Deleted " + removed.name)

    def play(self):
        self.viewport.playing = True
        self.viewport.selected = -1
        self.load_inspector(-1)
        self.log("Scene running")
        self.statusBar().showMessage("Running")

    def pause(self):
        self.viewport.playing = False
        self.log("Scene paused")

    def stop(self):
        self.viewport.playing = False
        self.viewport.phase = 0.0
        self.viewport.update()
        self.log("Scene stopped")
        self.statusBar().showMessage("Stopped")

    def save_project(self):
        self.statusBar().showMessage("Proof of concept: nothing is written to disk", 4000)
        self.log("Save skipped (in-memory project)")

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.applied.connect(self.on_settings_applied)
        dialog.exec()

    def on_settings_applied(self):
        self.restart_autosave()
        self.load_inspector(self.viewport.selected)
        self.viewport.update()
        self.log("Settings applied: " + settings.current.theme + " theme, " + settings.current.accent + " accent")

    def show_about(self):
        QMessageBox.about(self, "About BAM Engine", "BAM Engine v0.1\nProof of concept built with PyQt6.")

    def closeEvent(self, event):
        self.viewport.timer.stop()
        self.autosave.stop()
        self.back_to_manager.emit()
        event.accept()
