#
# Generic slider
#
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QFont, QColor, QPen
from PyQt5.QtWidgets import QGraphicsSimpleTextItem, QGraphicsItem

from src.Handler import Handler
from src.variables_globales import pen_width


class Slider(QGraphicsItem):
    mini = 0
    maxi = 1
    nStep = 1
    singleStep = 1
    sliderPosition = 0
    relief_offset = 3.
    r = 5.

    colorBack = QColor(53, 53, 43, 255)
    colorLeft = QColor(170, 28, 0, 255)
    colorRight = QColor(110, 157, 0, 255)
    brush = QColor(255, 85, 0, 255)
    pen = QColor(21, 11, 127, 255)

    def __init__(self, parentItem, title, npos=2, legend=['off', 'on']):
        super().__init__()

        self.nStep = npos
        self.sliderHeight = 15.
        self.stepWidth = 40.
        self.sliderWidth = self.stepWidth * (npos - 1) + 2 * self.r
        self.setParentItem(parentItem)
        self.setAcceptHoverEvents(True)

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
            ym = self.y() - self.legend[0].boundingRect().height() - self.r
            for i in range(npos):
                xm = self.x() + i * self.stepWidth - self.legend[i].boundingRect().width()
                self.legend[i].setPos(xm, ym)
        else:
            ym = self.y()
            xm = self.x() - self.legend[0].boundingRect().width() - self.r
            self.legend[0].setPos(xm, ym)
            xm = self.x() + self.boundingRect().width() + self.r
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

    def setSliderPosition(self, i):
        self.sliderPosition = i
        x = self.x() + i * self.stepWidth
        y = self.y() + 3
        self.handler.setPosition(x, y)

    def setRange(self, i, j):
        self.mini = i
        self.maxi = j
        self.setSingleStep()

    def setSingleStep(self):
        self.singleStep = (self.maxi - self.mini) / self.nStep

    def value(self):
        return self.mini + self.sliderPosition * self.singleStep

    def boundingRect(self):
        return QRectF(-pen_width / 2, -pen_width / 2, self.sliderWidth + pen_width, self.sliderHeight + pen_width)

    def paint(self, painter, option, widget):
        # assembly of 3 roundedRects

        painter.setBrush(QBrush(self.colorBack))
        painter.setPen(QPen(self.pen, 1))
        rect = QRectF(0., 0., float(self.sliderWidth), float(self.sliderHeight))
        painter.drawRoundedRect(rect, self.r, self.r)

        painter.setBrush(QBrush(self.colorLeft))
        painter.setPen(Qt.NoPen)
        rect = QRectF(self.relief_offset, self.relief_offset, self.handler.x() + self.handler.boundingRect().width(),
                      float(self.sliderHeight))
        painter.drawRoundedRect(rect, self.r, self.r)

        painter.setBrush(QBrush(self.colorRight))
        painter.setPen(Qt.NoPen)
        rect = QRectF(self.handler.x(), 0., float(self.sliderWidth), float(self.sliderHeight))
        painter.drawRoundedRect(rect, self.r, self.r)

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
        global clicked
        if not event.button() == Qt.LeftButton:
            return
        self.setCursor(Qt.ClosedHandCursor)
        clicked = True

    def mouseReleaseEvent(self, event):
        # et renvoie cette position dans sliderPosition
        # if on/off case, change state on click
        global clicked

        if clicked:

            # set the position to the nearest slot

            xh = self.pos().x()

            dx1 = abs(xh - self.xpos[0])
            for i in range(self.nStep - 1):
                dx2 = abs(xh - self.xpos[i + 1])
                if dx1 > dx2:
                    self.handler.setPosition(self.xpos[i], self.handler.pos().y())
                    break
                else:
                    self.handler.setPosition(self.xpos[i + 1], self.handler.pos().y())
                    break

                dx1 = dx2

            clicked = False
