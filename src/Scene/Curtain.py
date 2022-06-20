#
# curtain for transition
#
from PyQt5.QtCore import QRectF, QPointF, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsObject

from src.Style import GradientStyle, GeometryStyle


class Curtain(QGraphicsObject):

    def __init__(self, parent=None, alpha=255):
        from src.Scene.GameScene import GameScene

        super().__init__(parent)
        self.alpha = alpha
        self.brush = QBrush(
            GradientStyle(
                GameScene.height,
                QColor(0, 85, 127, self.alpha),
                QColor(0, 37, 54, self.alpha)
            )
        )
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

        painter.setBrush(self.brush)
        painter.setPen(QPen(QColor(68, 68, 68, self.alpha), 2))
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

    @staticmethod
    def change_text(text_item, text):
        old_x = text_item.x()
        old_w = text_item.boundingRect().width()
        text_item.setText(text)
        new_w = text_item.boundingRect().width()
        text_item.setX(old_x + (old_w - new_w) / 2)


