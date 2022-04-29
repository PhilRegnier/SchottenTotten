# Colors

from PyQt5.QtGui import QColor, QLinearGradient


class GlobalStyle:
    cadre_color = (57, 57, 57)
    relief_color = (53, 53, 43, 255)
    relief_color2 = (65, 71, 35, 255)
    ombrage_color = QColor(36, 36, 36, 90)
    ombrage_color_bt = QColor(36, 36, 36, 200)
    background_color = QColor(167, 159, 120)


class ColorStyle:
    def __init__(self):
        self.side0 = QColor(9, 18, 27, 90)
        self.side1 = QColor(85, 170, 255, 90)
        self.side_pen = QColor(85, 81, 44)
        self.hand = QColor(85, 170, 255, 40)
        self.hand_pen = QColor(10, 11, 8)


class GeometryStyle:
    main_width = 1200
    main_marge = 20
    marge = 5.
    r_bound = 10.
    pen_width = 1.


class GradientStyle(QLinearGradient):
    def __init__(self, height, color_up, color_down):
        super().__init__(0., height, 0., 0.)
        self.setSpread(QLinearGradient.ReflectSpread)
        self.setColorAt(0, color_up)
        self.setColorAt(1, color_down)

