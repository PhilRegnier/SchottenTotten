from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsDropShadowEffect

from src.Scene.Game.Pixel import Pixel
from src.Style import Pen, Shadow


class Digit(QGraphicsItem):
    nb_pixels_width = 4
    nb_pixels_height = 7
    gap = 1

    NUMBER = []
    NUMBER[0] = [0, 1, 2, 3, 4, 7, 8, 11, 12, 15, 16, 19, 20, 23, 24, 25, 26, 27]
    NUMBER[1] = [3, 7, 11, 15, 19, 23, 27]
    NUMBER[2] = [0, 1, 2, 3, 7, 11, 12, 13, 14, 15, 16, 20, 24, 25, 26, 27]
    NUMBER[3] = [0, 1, 2, 3, 7, 11, 12, 13, 14, 15, 19, 23, 24, 25, 26, 27]
    NUMBER[4] = [0, 3, 4, 7, 8, 11, 12, 13, 14, 15, 19, 23, 27]
    NUMBER[5] = [0, 1, 2, 3, 4, 8, 12, 13, 14, 15, 19, 23, 24, 25, 26, 27]
    NUMBER[6] = [0, 4, 8, 12, 13, 14, 15, 16, 19, 20, 23, 24, 25, 26, 27]
    NUMBER[7] = [0, 1, 2, 3, 7, 11, 14, 15, 19, 23, 27]
    NUMBER[8] = [0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15, 16, 19, 20, 23, 24, 25, 26, 27]
    NUMBER[9] = [0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15, 19, 23, 27]

    def __init__(self):
        super().__init__()
        nb_pixels = Digit.nb_pixels_height * Digit.nb_pixels_width
        self.pixels = [nb_pixels]
        k = 0
        for i in range(Digit.nb_pixels_height):
            for j in range(Digit.nb_pixels_width):
                self.pixels[k] = Pixel()
                self.pixels[k].setParentItem(self)
                self.pixels[k].setX(Digit.gap + j * (Digit.gap + Pixel.width))
                self.pixels[k].setY(Digit.gap + i * (Digit.gap + Pixel.height))
                k += 1

        self.brush = QBrush()
        self.brush.setColor(QColor(31, 21, 17, 255))
        self.pen = Pen()
        self.setGraphicsEffect(Shadow())

        self.rect = QRectF(
            0,
            0,
            Digit.nb_pixels_width * (Pixel.width + Digit.gap) + Digit.gap,
            Digit.nb_pixels_height * (Pixel.height + Digit.gap) + Digit.gap
        )

    def boundingRect(self):
        return QRectF(
            self.rect.X() - self.pen.width(),
            self.rect.Y() - self.pen.width(),
            self.rect.width() + self.pen.width(),
            self.rect.height() + self.pen.width()
        )

    def paint(self, painter, option, widget=0):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawRect(self.rect.X())

    def display_none(self):
        for pixel in self.pixels:
            pixel.set_light_off()

    def display_number(self, number):
        self.display_none()
        for k in Digit.NUMBER[number]:
            self.pixels[k].set_light_on()
