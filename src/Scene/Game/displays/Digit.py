from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QGraphicsItem

from src.Scene.Game.displays.Pixel import Pixel
from src.Style import Pen, Shadow


class Digit(QGraphicsItem):
    nb_pixels_width = 4
    nb_pixels_height = 7
    gap = 1

    NUMBER = [
        [0, 1, 2, 3, 4, 7, 8, 11, 12, 15, 16, 19, 20, 23, 24, 25, 26, 27],
        [3, 7, 11, 15, 19, 23, 27],
        [0, 1, 2, 3, 7, 11, 12, 13, 14, 15, 16, 20, 24, 25, 26, 27],
        [0, 1, 2, 3, 7, 11, 12, 13, 14, 15, 19, 23, 24, 25, 26, 27],
        [0, 3, 4, 7, 8, 11, 12, 13, 14, 15, 19, 23, 27],
        [0, 1, 2, 3, 4, 8, 12, 13, 14, 15, 19, 23, 24, 25, 26, 27],
        [0, 4, 8, 12, 13, 14, 15, 16, 19, 20, 23, 24, 25, 26, 27],
        [0, 1, 2, 3, 7, 11, 14, 15, 19, 23, 27],
        [0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15, 16, 19, 20, 23, 24, 25, 26, 27],
        [0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15, 19, 23, 27]
    ]

    def __init__(self, parent_item):
        super(Digit, self).__init__()
        self.pixels = []
        for i in range(Digit.nb_pixels_height):
            for j in range(Digit.nb_pixels_width):
                pixel = Pixel()
                pixel.setParentItem(self)
                pixel.setX(Digit.gap + j * (Digit.gap + Pixel.width))
                pixel.setY(Digit.gap + i * (Digit.gap + Pixel.height))
                self.pixels.append(pixel)

        self.setParentItem(parent_item)
        self.brush = QBrush()
        self.brush.setColor(QColor(31, 21, 17, 255))
        self.pen = Pen()
        self.setGraphicsEffect(Shadow(-1, -2))

        self.rect = QRectF(
            0,
            0,
            Digit.nb_pixels_width * (Pixel.width + Digit.gap) + Digit.gap,
            Digit.nb_pixels_height * (Pixel.height + Digit.gap) + Digit.gap
        )

    def boundingRect(self):
        return QRectF(
            - self.pen.width(),
            - self.pen.width(),
            self.rect.width() + self.pen.width(),
            self.rect.height() + self.pen.width()
        )

    def paint(self, painter, option, widget=0):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawRect(self.rect)

    def display_none(self):
        for pixel in self.pixels:
            pixel.set_light_off()

        self.update()

    def display_number(self, number):
        self.display_none()
        for k in Digit.NUMBER[number]:
            self.pixels[k].set_light_on()

        self.update()
