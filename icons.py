from PyQt6.QtCore import QPointF, QRectF, QSize, Qt
from PyQt6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPen, QPixmap, QPolygonF

from theme import palette

REGISTRY = []


def pts(*coords):
    return QPolygonF([QPointF(x, y) for x, y in coords])


def line(p, x1, y1, x2, y2):
    p.drawLine(QPointF(x1, y1), QPointF(x2, y2))


def box(x, y, w, h):
    return QRectF(x, y, w, h)


def g_plus(p, c):
    line(p, 16, 6, 16, 26)
    line(p, 6, 16, 26, 16)


def g_folder(p, c):
    path = QPainterPath()
    path.moveTo(4, 26)
    path.lineTo(4, 8)
    path.lineTo(13, 8)
    path.lineTo(16, 11)
    path.lineTo(28, 11)
    path.lineTo(28, 26)
    path.closeSubpath()
    p.drawPath(path)


def g_import(p, c):
    line(p, 16, 5, 16, 20)
    p.drawPolyline(pts((9, 13), (16, 20), (23, 13)))
    p.drawPolyline(pts((6, 21), (6, 26), (26, 26), (26, 21)))


def g_search(p, c):
    p.drawEllipse(box(5, 5, 15, 15))
    line(p, 17, 17, 27, 27)


def g_play(p, c):
    p.setBrush(c)
    p.drawPolygon(pts((10, 6), (26, 16), (10, 26)))


def g_pause(p, c):
    p.setBrush(c)
    p.drawRect(box(8, 6, 6, 20))
    p.drawRect(box(18, 6, 6, 20))


def g_stop(p, c):
    p.setBrush(c)
    p.drawRect(box(7, 7, 18, 18))


def g_launch(p, c):
    p.drawEllipse(box(4, 4, 24, 24))
    p.setBrush(c)
    p.drawPolygon(pts((13, 10), (23, 16), (13, 22)))


def g_gear(p, c):
    p.drawEllipse(box(7, 7, 18, 18))
    p.drawEllipse(box(12, 12, 8, 8))
    for i in range(8):
        p.save()
        p.translate(16, 16)
        p.rotate(i * 45)
        line(p, 0, -9, 0, -14)
        p.restore()


def g_trash(p, c):
    line(p, 6, 9, 26, 9)
    p.drawRect(box(9, 9, 14, 17))
    p.drawPolyline(pts((13, 9), (13, 5), (19, 5), (19, 9)))
    line(p, 14, 13, 14, 22)
    line(p, 18, 13, 18, 22)


def g_pencil(p, c):
    p.drawPolygon(pts((6, 26), (8, 18), (20, 6), (26, 12), (14, 24)))
    line(p, 17, 9, 23, 15)


def g_clone(p, c):
    p.drawRect(box(5, 11, 16, 16))
    p.drawPolyline(pts((11, 9), (11, 5), (27, 5), (27, 21), (23, 21)))


def g_tag(p, c):
    p.drawPolygon(pts((4, 4), (16, 4), (28, 16), (16, 28), (4, 16)))
    p.drawEllipse(box(8, 8, 4, 4))


def g_refresh(p, c):
    p.drawArc(box(6, 6, 20, 20), 40 * 16, 280 * 16)
    p.drawPolyline(pts((25, 4), (24, 10), (18, 9)))


def g_heart(p, c):
    path = QPainterPath()
    path.moveTo(16, 27)
    path.cubicTo(2, 16, 6, 4, 16, 10)
    path.cubicTo(26, 4, 30, 16, 16, 27)
    p.setBrush(c)
    p.drawPath(path)


def g_store(p, c):
    p.drawRect(box(6, 12, 20, 15))
    p.drawPolyline(pts((11, 12), (11, 8), (21, 8), (21, 12)))


def g_grid(p, c):
    p.setBrush(c)
    p.drawRect(box(5, 5, 9, 9))
    p.drawRect(box(18, 5, 9, 9))
    p.drawRect(box(5, 18, 9, 9))
    p.drawRect(box(18, 18, 9, 9))


def g_save(p, c):
    p.drawRect(box(5, 5, 22, 22))
    p.drawRect(box(10, 5, 12, 8))
    p.drawRect(box(9, 18, 14, 9))


def g_close(p, c):
    line(p, 7, 7, 25, 25)
    line(p, 25, 7, 7, 25)


def g_check(p, c):
    p.drawPolyline(pts((6, 17), (13, 24), (26, 8)))


def g_info(p, c):
    p.drawEllipse(box(4, 4, 24, 24))
    line(p, 16, 14, 16, 23)
    p.drawPoint(QPointF(16, 10))


def g_rect(p, c):
    p.drawRect(box(6, 9, 20, 14))


def g_circle(p, c):
    p.drawEllipse(box(6, 6, 20, 20))


def g_exit(p, c):
    p.drawPolyline(pts((14, 6), (6, 6), (6, 26), (14, 26)))
    line(p, 12, 16, 26, 16)
    p.drawPolyline(pts((20, 10), (26, 16), (20, 22)))


GLYPHS = {
    "plus": g_plus, "folder": g_folder, "import": g_import, "search": g_search,
    "play": g_play, "pause": g_pause, "stop": g_stop, "launch": g_launch,
    "gear": g_gear, "trash": g_trash, "pencil": g_pencil, "clone": g_clone,
    "tag": g_tag, "refresh": g_refresh, "heart": g_heart, "store": g_store,
    "grid": g_grid, "save": g_save, "close": g_close, "check": g_check,
    "info": g_info, "rect": g_rect, "circle": g_circle, "exit": g_exit,
}


def glyph_pixmap(name, color, size=64):
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.scale(size / 32.0, size / 32.0)
    c = QColor(color)
    pen = QPen(c, 2.6)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)
    GLYPHS[name](p, c)
    p.end()
    return pix


def color_for(kind):
    colors = palette()
    if kind == "white":
        return "#ffffff"
    if kind == "toolbar":
        return colors["text"]
    return colors["button_text"]


def icon(name, color):
    return QIcon(glyph_pixmap(name, color))


def attach(target, name, kind="neutral", size=18):
    target.setIcon(icon(name, color_for(kind)))
    if size and hasattr(target, "setIconSize"):
        target.setIconSize(QSize(size, size))
    REGISTRY.append((target, name, kind))


def refresh_icons():
    alive = []
    for target, name, kind in REGISTRY:
        try:
            target.setIcon(icon(name, color_for(kind)))
            alive.append((target, name, kind))
        except RuntimeError:
            pass
    REGISTRY[:] = alive
