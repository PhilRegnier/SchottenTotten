#
# Generic slider
#
from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QBrush, QFont, QColor, QPen
from PyQt6.QtWidgets import QGraphicsSimpleTextItem, QGraphicsItem

from src.Scene.Starter.Handler import Handler
from src.Style import MainGeometry


class Slider(QGraphicsItem):
    mini = 0
    maxi = 1
    nStep = 1
    singleStep = 1
    sliderPosition = 0
    relief_offset = 3.
    radius = 5.

    colorBack = QColor(53, 53, 43, 255)
    colorLeft = QColor(170, 28, 0, 255)
    colorRight = QColor(110, 157, 0, 255)
    brush = QColor(255, 85, 0, 255)
    pen = QColor(21, 11, 127, 255)

    def __init__(self, parent_item, title, npos=2, legend=None):
        super().__init__()

        if legend is None:
            legend = ['off', 'on']
        self.nStep = npos
        self.sliderHeight = 15.
        self.stepWidth = 40.
        self.sliderWidth = self.stepWidth * (npos - 1) + 2 * Slider.radius
        self.setParentItem(parent_item)
        self.setAcceptHoverEvents(True)
        self.clicked = False

        self.xpos = [self.stepWidth * i for i in range(npos)]

        # legend

        font = QFont("Helvetica [Cronyx]", 15)
        font.setStretch(150)

        self.legend = [QGraphicsSimpleTextItem(legend[i]) for i in range(npos)]

        for i in range(npos):
            self.legend[i].setFont(font)
            self.legend[i].setBrush(self.brush)
            self.legend[i].setPen(self.pen)
            self.legend[i].setParentItem(self)

        if npos > 2:
            ym = self.y() - self.legend[0].boundingRect().height() - Slider.radius
            for i in range(npos):
                xm = self.x() + i * self.stepWidth - self.legend[i].boundingRect().width()
                self.legend[i].setPos(xm, ym)
        else:
            ym = self.y()
            xm = self.x() - self.legend[0].boundingRect().width() - Slider.radius
            self.legend[0].setPos(xm, ym)
            xm = self.x() + self.boundingRect().width() + Slider.radius
            self.legend[1].setPos(xm, ym)

        # title

        font = QFont("Helvetica [Cronyx]", 25)
        font.setStretch(150)

        self.title = QGraphicsSimpleTextItem(title)
        self.title.setFont(font)
        self.title.setBrush(self.brush)
        self.title.setPen(self.pen)
        self.title.setParentItem(self)
        xm = (self.boundingRect().width() - self.title.boundingRect().width()) / 2
        ym = -self.legend[0].boundingRect().height() - 20 - self.title.boundingRect().height()
        self.title.setPos(xm, ym)

        # handler

        self.handler = Handler(self)

        # Setting non focus opacity

        self.setOpacity(0.8)

        # dimensions

        wl = self.legend[npos - 1].x() + self.legend[npos - 1].boundingRect().width() - self.legend[0].x()

        self.width = max(wl, self.title.boundingRect().width())
        self.height = self.boundingRect().height() - ym

    def set_position(self, i):
        self.sliderPosition = i
        x = self.x() + i * self.stepWidth
        y = self.y() + 3
        self.handler.set_position(x, y)

    def set_range(self, i, j):
        self.mini = i
        self.maxi = j
        self.set_single_step()

    def set_single_step(self):
        self.singleStep = (self.maxi - self.mini) / self.nStep

    def value(self):
        return self.mini + self.sliderPosition * self.singleStep

    def boundingRect(self):
        return QRectF(
            -MainGeometry.pen_width / 2,
            -MainGeometry.pen_width / 2,
            self.sliderWidth + MainGeometry.pen_width,
            self.sliderHeight + MainGeometry.pen_width)

    def paint(self, painter, option, widget=0):
        # assembly of 3 roundedRects

        painter.setBrush(QBrush(self.colorBack))
        painter.setPen(QPen(self.pen, 1))
        rect = QRectF(0., 0., float(self.sliderWidth), float(self.sliderHeight))
        painter.drawRoundedRect(rect, Slider.radius, Slider.radius)

        painter.setBrush(QBrush(self.colorLeft))
        painter.setPen(Qt.PenStyle.NoPen)
        rect = QRectF(self.relief_offset, self.relief_offset, self.handler.x() + self.handler.boundingRect().width(),
                      float(self.sliderHeight))
        painter.drawRoundedRect(rect, Slider.radius, Slider.radius)

        painter.setBrush(QBrush(self.colorRight))
        painter.setPen(Qt.PenStyle.NoPen)
        rect = QRectF(self.handler.x(), 0., float(self.sliderWidth), float(self.sliderHeight))
        painter.drawRoundedRect(rect, Slider.radius, Slider.radius)

    #    def setOn(self):
    # Brighter and colorful button if "on" chosen in "on/off" case

    def hoverEnterEvent(self, event):
        # Highlight the button if mouse's incoming or rectangle plus clair...
        self.setOpacity(1.0)

    def hoverLeaveEvent(self, event):
        # Normal rendering if mouse's leaving
        self.setOpacity(0.8)

    def mousePressEvent(self, event):
        # valide le click
        if not event.button() == Qt.MouseButton.LeftButton:
            return
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        self.clicked = True

    def mouseReleaseEvent(self, event):
        # et renvoie cette position dans sliderPosition
        # if on/off case, change state on click

        if self.clicked:

            # set the position to the nearest slot

            released_position = self.pos().x()
            anchor_position = self.xpos[0]

            delta = abs(released_position - anchor_position)

            for x in self.xpos:
                new_delta = abs(released_position - x)
                if new_delta < delta:
                    delta = new_delta
                    anchor_position = x
                else:
                    break

            self.handler.set_position(anchor_position, self.handler.pos().y())
            self.clicked = False
