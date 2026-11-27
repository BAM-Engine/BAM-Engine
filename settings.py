import os
from dataclasses import dataclass

THEMES = ["Dark", "Light"]
ACCENTS = ["Blue", "Orange", "Green", "Purple"]
RENDERERS = ["P.E.A.K.", "Light"]
LANGUAGES = ["BamScript", "Python", "C++", "C#"]
UI_LANGUAGES = ["English", "Polski", "Deutsch", "Español"]


@dataclass
class Settings:
    theme: str = "Dark"
    accent: str = "Blue"
    font_size: int = 13
    ui_language: str = "English"
    default_path: str = os.path.expanduser("~/BAM/Projects")
    default_renderer: str = "P.E.A.K."
    default_language: str = "BamScript"
    autosave_minutes: int = 5
    check_updates: bool = True
    show_hints: bool = True
    confirm_remove: bool = True


current = Settings()
