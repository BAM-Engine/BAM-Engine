from dataclasses import dataclass, field

ENGINE_VERSION = "0.1"


@dataclass
class Entity:
    name: str
    kind: str
    x: float
    y: float
    w: float
    h: float
    color: str
    static: bool = False


@dataclass
class Project:
    name: str
    path: str
    version: str = ENGINE_VERSION
    edited: str = "2026-11-26 00:00:00"
    renderer: str = "P.E.A.K."
    template: str = "Empty"
    language: str = "BamScript"
    width: int = 1152
    height: int = 648
    vsync: bool = True
    version_control: str = "None"
    favorite: bool = False
    tags: list = field(default_factory=list)
    entities: list = field(default_factory=list)


def build_entities(template):
    if template == "2D Platformer":
        return [
            Entity("Ground", "Rectangle", 40, 440, 640, 50, "#6a6a70", True),
            Entity("Player", "Rectangle", 120, 360, 50, 80, "#1c97ea"),
        ]
    if template == "3D Starter":
        return [
            Entity("Floor", "Rectangle", 60, 420, 600, 40, "#6a6a70", True),
            Entity("Cube", "Rectangle", 280, 300, 110, 110, "#d98a3d"),
            Entity("Light", "Circle", 520, 120, 50, 50, "#f2d54b", True),
        ]
    return []


def example_projects():
    platformer = Project(
        name="Example Project #1",
        path=r"C:\Users\Kocialko\Appdata\Roaming\BAM\Projects\example_1",
        edited="2026-11-25 21:04:12",
        renderer="P.E.A.K.",
        template="2D Platformer",
        tags=["2d", "platformer"],
        entities=[
            Entity("Ground", "Rectangle", 40, 440, 640, 50, "#6a6a70", True),
            Entity("Platform", "Rectangle", 300, 340, 140, 18, "#6a6a70", True),
            Entity("Player", "Rectangle", 120, 360, 50, 80, "#1c97ea"),
            Entity("Coin", "Circle", 350, 290, 36, 36, "#f2d54b"),
            Entity("Enemy", "Rectangle", 520, 390, 50, 50, "#c9524f"),
        ],
    )
    topdown = Project(
        name="Example Project #2",
        path="/home/Kocialko/BAM/Projects/example_2",
        edited="2026-11-24 18:30:45",
        renderer="Light",
        template="Top Down",
        tags=["2d", "rpg"],
        entities=[
            Entity("WallTop", "Rectangle", 60, 60, 600, 24, "#6a6a70", True),
            Entity("WallLeft", "Rectangle", 60, 60, 24, 380, "#6a6a70", True),
            Entity("Chest", "Rectangle", 520, 120, 70, 50, "#a8743a"),
            Entity("Tree", "Circle", 160, 330, 90, 90, "#4f9a5b", True),
            Entity("Hero", "Circle", 300, 220, 56, 56, "#1c97ea"),
            Entity("Slime", "Circle", 440, 300, 44, 44, "#7bc96f"),
        ],
    )
    return [platformer, topdown]
