#
# curtain for transition
#
from PyQt5.QtCore import QRectF, QPointF, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsObject

from src.Style import GradientStyle, GeometryStyle


class Curtain(QGraphicsObject):

    def __init__(self, parent):
        from src.Scene.GameScene import GameScene

        super().__init__(parent)
        self.gradient = GradientStyle(GameScene.height, QColor(0, 85, 127, 255), QColor(0, 37, 54, 255))
        self.setVisible(False)
        self.setPos(0, 0)
        self.anim = None

    def boundingRect(self):
        from src.Scene.GameScene import GameScene

        return QRectF(-GeometryStyle.pen_width / 2,
                      -GeometryStyle.pen_width / 2,
                      GameScene.width + GeometryStyle.pen_width,
                      GameScene.height + GeometryStyle.pen_width
                      )

    def paint(self, painter, option, widget=0):
        from src.Scene.GameScene import GameScene

        painter.setBrush(QBrush(self.gradient))
        painter.setPen(QPen(QColor(68, 68, 68, 255), 2))
        rect = QRectF(0., 0., float(GameScene.width), float(GameScene.height))
        painter.drawRoundedRect(rect, GeometryStyle.r_bound, GeometryStyle.r_bound)

    def animate_incoming(self, z_value=None):
        if z_value is not None:
            self.setZValue(z_value)
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setEasingCurve(QEasingCurve.OutBounce)
        self.anim.setDuration(800)
        self.anim.setStartValue(QPointF(0, -self.boundingRect().height()))
        self.anim.setEndValue(QPointF(0, 0))
        self.setVisible(True)
        self.anim.start()

    def animate_leaving(self, z_value=None):
        if z_value is not None:
            self.setZValue(z_value)
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setEasingCurve(QEasingCurve.InCubic)
        self.anim.setDuration(800)
        self.anim.setStartValue(QPointF(0, 0))
        self.anim.setEndValue(QPointF(0, -self.boundingRect().height()))
        self.anim.finished.connect(self.remove)
        self.anim.start()

    def remove(self):
        self.setVisible(False)


