# Colors

from PyQt5.QtGui import QColor


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
