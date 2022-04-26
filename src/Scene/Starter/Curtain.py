#
# curtain for transition
#
from PyQt5.QtCore import QRectF, QPointF, QPropertyAnimation
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsObject

from src.MainWindow.GameWindow import GameWindow
from src.Scene.Game.Side import Side
from src.Style import GradientStyle, GeometryStyle


class Curtain(QGraphicsObject):

    def __init__(self, parent):
        super().__init__(parent)
        self.gradient = GradientStyle(Side.height, QColor(0, 85, 127, 255), QColor(0, 37, 54, 255))
        self.setVisible(False)
        self.setPos(0, 0)

    def boundingRect(self):
        return QRectF(-GameWindow.pen_width / 2,
                      -GameWindow.pen_width / 2,
                      GameWindow.width + GameWindow.pen_width,
                      GameWindow.height() + GameWindow.pen_width)

    def paint(self, painter, option, widget=0):
        painter.setBrush(QBrush(self.gradient))
        painter.setPen(QPen(QColor(68, 68, 68, 255), 2))
        rect = QRectF(0., 0., float(GameWindow.width), float(GameWindow.height()))
        painter.drawRoundedRect(rect, GeometryStyle.r_bound, GeometryStyle.r_bound)

    def animate_incoming(self):
        anim = QPropertyAnimation(self, b"pos")
        anim.setDuration(800)
        anim.setStartValue(QPointF(0, -self.boundingRect().height()))
        anim.setEndValue(QPointF(0, 0))
        self.setVisible(True)
        anim.start()

    def animate_leaving(self):
        anim = QPropertyAnimation(self, b"pos")
        anim.setDuration(800)
        anim.setStartValue(QPointF(0, 0))
        anim.setEndValue(QPointF(0, -self.boundingRect().height()))
        anim.finished.connect(self.remove)
        anim.start()

    def remove(self):
        self.setVisible(False)
