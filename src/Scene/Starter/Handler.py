# ------------------------------------------------------------------------------------------------------
# Slider's button
# ------------------------------------------------------------------------------------------------------

from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtWidgets import QGraphicsItem


class Handler(QGraphicsItem):
    moved = False

    def __init__(self, parent_item):
        super().__init__()
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setParentItem(parent_item)
        self.anchor_point = QPointF()

        self.xmin = self.parentItem().x()
        self.xmax = self.xmin + self.parentItem().boundingRect().width()
        self.clicked = False

    def set_position(self, x, y):
        self.setPos(x, y)
        self.anchor_point = self.pos()

    def hoverEnterEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        if not event.button() == Qt.LeftButton:
            return
        self.clicked = True

    def mouseMoveEvent(self, event):
        if self.clicked:
            xh = event.pos().x()
            yh = self.anchor_point.y()

            if xh < self.xmin:
                xh = self.xmin
            if xh > self.xmax:
                xh = self.xmax

            self.setPos(xh, yh)

    def boundingRect(self):
        from src.Scene.Starter.Slider import Slider

        pen_width = 1.0
        return QRectF(-pen_width / 2,
                      -pen_width / 2,
                      2 * Slider.radius + pen_width,
                      2 * Slider.radius + pen_width)

    def paint(self, painter, option, widget=0):
        from src.Scene.Starter.Slider import Slider

        painter.setPen(Qt.NoPen)
        painter.setBrush(Slider.colorBack)
        r = 2 * int(Slider.radius)
        painter.drawEllipse(0, 0, r, r)
