# Style classes

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QLinearGradient, QPen, QBrush
from PyQt6.QtWidgets import QGraphicsDropShadowEffect


class GlobalStyle:
    cadre_color = (57, 57, 57)
    relief_color = (53, 53, 43, 255)
    relief_color2 = (65, 71, 35, 255)
    ombrage_color = QColor(36, 36, 36, 90)
    ombrage_color_bt = QColor(36, 36, 36, 200)
    background_color = QColor(167, 159, 120)


class ManagerStyle:
    brush = QBrush(QColor(255, 255, 255, 180))
    pen = QPen(QColor(166, 166, 166, 255), 1)


class PlayerColors:
    side0 = QColor(9, 18, 27, 90)
    side1 = QColor(85, 170, 255, 90)
    side_pen = QColor(85, 81, 44)
    hand = QColor(85, 170, 255, 40)
    hand_pen = QColor(10, 11, 8)


class AutomatonColors:
    side0 = QColor(70, 23, 0, 90)
    side1 = QColor(255, 85, 0, 90)
    side_pen = QColor(85, 81, 44)
    hand = QColor(49, 53, 42, 150)
    hand_pen = QColor(10, 11, 8)


class GeometryStyle:
    main_width = 1200
    main_marge = 20
    marge = 5.
    r_bound = 10.
    pen_width = 1.

    # main_height must be redefined after initialization of the view by the init method of GameWindow
    main_height = 0


class GradientStyle(QLinearGradient):
    def __init__(self, height, color_up, color_down):
        super().__init__(0., height, 0., 0.)
        self.setSpread(QLinearGradient.Spread.ReflectSpread)
        self.setColorAt(0, color_up)
        self.setColorAt(1, color_down)


class Pen(QPen):
    def __init__(self):
        super().__init__()
        self.setWidth(2)
        self.setColor(QColor(67, 66, 37, 255))
        self.setCapStyle(Qt.PenCapStyle.SquareCap)
        self.setJoinStyle(Qt.PenJoinStyle.BevelJoin)


class Shadow(QGraphicsDropShadowEffect):
    def __init__(self):
        super().__init__()
        self.setColor(QColor(31, 21, 17, 255))
        self.setBlurRadius(3)
        self.setXOffset(1)
        self.setYOffset(3)
