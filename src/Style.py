# Style classes

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QLinearGradient, QPen, QBrush, QFont
from PyQt6.QtWidgets import QGraphicsDropShadowEffect


class GlobalStyle:
    cadre_color = (57, 57, 57)
    relief_color = (53, 53, 43, 255)
    relief_color2 = (65, 71, 35, 255)
    ombrage_color = QColor(36, 36, 36, 90)
    ombrage_color_bt = QColor(36, 36, 36, 200)
    background_color = QColor(167, 159, 120)
    shadow_color = QColor(31, 21, 17, 255)
    glow_color = QColor(176, 186, 58, 255)
    text_color = QColor(176, 186, 58, 255)
    text_font = QFont("Helvetica [Cronyx]", 28)


class DisplayStyle:
    brush = QBrush(QColor(255, 255, 255, 100))
    pen = QPen(QColor(166, 166, 166, 100), 1)


class WarningStyle:
    brush = QBrush(QColor(255, 0, 0, 150))
    pen = QPen(QColor(255, 0, 0, 200), 1)


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


class MainGeometry:
    width = 1200
    marge = 20
    r_bound = 10.
    pen_width = 1.
    spot_marge = 5.

    width_display_ratio = 0.2

    # main_height must be redefined after initialization of the view by the init method of GameWindow
    height = 0

    @staticmethod
    def centered(pos0, total_width, effective_width):
        return pos0 + (total_width - effective_width) / 2


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

