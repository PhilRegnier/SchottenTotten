from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QGraphicsItem


class Pixel(QGraphicsItem):

    color_on = QColor(0, 114, 114, 255)
    color_off = QColor(31, 21, 17, 255)
    width = 6
    height = 5

    def __init__(self):
        super().__init__()
        self.color = Pixel.color_off
        self.brush = QBrush()
        pass

    def set_light_off(self):
        self.color = Pixel.color_off

    def set_light_on(self):
        self.color = Pixel.color_on

    def boundingRect(self):
        return QRectF(0, 0, Pixel.width, Pixel.height)

    def paint(self, painter, option, widget=0):
        self.brush.setColor(self.color)
        painter.setBrush(self.brush)
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, Pixel.width, Pixel.height)
