# ------------------------------------------------------------------------------------------------------
# Slider's button
# ------------------------------------------------------------------------------------------------------
from PyQt5 import Qt
from PyQt5.QtCore import QRectF, QPointF
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
        self.anchorPoint = QPointF()

        self.r = self.parentItem().r
        self.xmin = self.parentItem().x()
        self.xmax = self.xmin + self.parentItem().boundingRect().width()

    def setPosition(self, x, y):
        self.setPos(x, y)
        self.anchorPoint = self.pos()

    def hoverEnterEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        global clicked
        if not event.button() == Qt.LeftButton:
            return
        clicked = True

    def mouseMoveEvent(self, event):
        # ensure it's a legal move
        if clicked:
            xh = event.pos().x()
            yh = self.anchorPoint.y()

            if xh < self.xmin:
                xh = self.xmin
            if xh > self.xmax:
                xh = self.xmax

            self.setPos(xh, yh)

    def boundingRect(self):
        pen_width = 1.0
        return QRectF(-pen_width / 2, -pen_width / 2, 2 * self.r + pen_width, 2 * self.r + pen_width)

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.parentItem().colorBack)
        r = 2 * int(self.r)
        painter.drawEllipse(0, 0, r, r)
