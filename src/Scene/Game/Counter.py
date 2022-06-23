from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsLineItem

from src.Scene.Game.Digit import Digit
from src.Style import Pen, GeometryStyle, ManagerStyle
from src.TextInForeground import TextInForeground


class Counter(QGraphicsItem):

    def __init__(self):
        super().__init__()

        # instantiate children items

        self.current_round = Digit()
        self.max_round = Digit()

        self.slash = QGraphicsLineItem()
        self.slash.setPen(Pen())
        self.slash.setParentItem(self)

        self.text = TextInForeground("ROUND", self)

        # geometry

        self.slash.setLine(
            0,
            0,
            self.max_round.boundingRect().width() / 2,
            self.max_round.boundingRect().height()
        )

        marge_width = 5
        marge_height = 5
        width = max(
            (self.max_round.boundingRect().width() + marge_width) * 2 + self.slash.boundingRect().width(),
            self.text.boundingRect().width()
        )
        width += 2 * marge_width
        height = self.max_round.boundingRect().height() + self.text.boundingRect().height() + marge_height * 3

        self.rect = QRectF(0, 0, width, height)

        # positioning

        self.text.setPos((width - self.text.boundingRect().width()) / 2, marge_height)

        y = self.text.boundingRect().height() + 2 * marge_height

        self.current_round.setPos(
            (width - self.slash.boundingRect().width()) / 2 - self.max_round.boundingRect().width() - marge_width,
            y
        )
        self.slash.setPos(
            (width - self.slash.boundingRect().width()) / 2,
            y
        )
        self.max_round.setPos(
            (width + self.slash.boundingRect().width()) / 2 + marge_width,
            y
        )

    def boundingRect(self):
        return QRectF(
            - GeometryStyle.pen_width,
            - GeometryStyle.pen_width,
            self.rect.width() + GeometryStyle.pen_width,
            self.rect.height() + GeometryStyle.pen_width
        )

    def paint(self, painter, option, widget=0):
        painter.setBrush(ManagerStyle.brush)
        painter.setPen(ManagerStyle.pen)
        painter.drawRoundedRect(self.rect, GeometryStyle.r_bound, GeometryStyle.r_bound)
