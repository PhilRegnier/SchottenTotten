from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QBrush, QPen
from PyQt6.QtWidgets import QGraphicsItem


class Pixel(QGraphicsItem):

    color_on = QColor(0, 114, 114, 255)
    color_off = QColor(31, 21, 17, 255)
    width = 6
    height = 5

    def __init__(self):
        super().__init__()
        self.color = Pixel.color_off
        self.brush = QBrush(self.color, Qt.BrushStyle.SolidPattern)
        self.setVisible(True)

    def set_light_off(self):
        self.color = Pixel.color_off
        self.update()

    def set_light_on(self):
        self.color = Pixel.color_on
        self.update()

    def boundingRect(self):
        return QRectF(0, 0, Pixel.width, Pixel.height)

    def paint(self, painter, option, widget=0):
        self.brush.setColor(self.color)
        painter.setBrush(self.brush)
        painter.setPen(QPen(self.color, 1))
        painter.drawRect(0, 0, Pixel.width, Pixel.height)
