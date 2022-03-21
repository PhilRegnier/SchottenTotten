#
# curtain for transition
#
from PyQt5.QtCore import QRectF, QPointF, QPropertyAnimation
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsObject

from src.variables_globales import side_height, mainWindow_width, mainWindow_height, rBound


class Curtain(QGraphicsObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVisible(False)
        self.setPos(0, 0)

    def boundingRect(self):
        pen_width = 2.0
        return QRectF(-pen_width / 2, -pen_width / 2, mainWindow_width + pen_width, mainWindow_height + pen_width)

    def paint(self, painter, option, widget):
        gradient = QLinearGradient(0., side_height, 0., 0.)
        gradient.setSpread(QLinearGradient.ReflectSpread)
        gradient.setColorAt(0, QColor(0, 85, 127, 255))
        gradient.setColorAt(1, QColor(0, 37, 54, 255))
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(68, 68, 68, 255), 2))
        rect = QRectF(0., 0., float(mainWindow_width), float(mainWindow_height))
        painter.drawRoundedRect(rect, rBound, rBound)

    def animate_incoming(self):
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(800)
        self.anim.setStartValue(QPointF(0, -self.boundingRect().height()))
        self.anim.setEndValue(QPointF(0, 0))
        self.setVisible(True)
        self.anim.start()

    def animate_leaving(self):
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(800)
        self.anim.setStartValue(QPointF(0, 0))
        self.anim.setEndValue(QPointF(0, -self.boundingRect().height()))
        self.anim.finished.connect(self.remove)
        self.anim.start()

    def remove(self):
        self.setVisible(False)
