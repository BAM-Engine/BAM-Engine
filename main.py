import sys

from PyQt6.QtWidgets import QApplication

from engine_ui import EngineWindow
from project_screen import ProjectManager
from theme import apply_theme


class BamApp:
    def __init__(self):
        self.manager = ProjectManager()
        self.manager.project_opened.connect(self.open_project)
        self.engine = None

    def open_project(self, project):
        self.engine = EngineWindow(project)
        self.engine.back_to_manager.connect(self.manager.show_again)
        self.manager.hide()
        self.engine.show()

    def start(self):
        self.manager.show()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("BAM Engine")
    apply_theme()
    bam = BamApp()
    bam.start()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
