from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsLineItem

from src.Scene.Game.Digit import Digit
from src.Scene.Game.Display import Display
from src.Style import Pen
from src.TextInForeground import TextInForeground


class Counter(Display):

    def __init__(self):
        super(Counter, self).__init__()

        # instantiate children items

        self.current_round = Digit(self)
        self.max_round = Digit(self)

        self.slash = QGraphicsLineItem()
        self.slash.setPen(Pen())
        self.slash.setParentItem(self)

        self.text = self.text_displayed("ROUND", self.max_width - 2 * self.marge_width)

        # set geometry

        self.slash.setLine(
            self.max_round.boundingRect().width() / 2,
            0,
            0,
            self.max_round.boundingRect().height()
        )

        width = max(
            self.max_round.boundingRect().width() * 2 + self.slash.boundingRect().width() + 4 * self.marge_width,
            self.text.boundingRect().width() + 2 * self.marge_width
        )
        height = self.max_round.boundingRect().height() + self.text.boundingRect().height() + self.marge_height * 2

        self.rect = QRectF(0, 0, width, height)

        # position items

        self.text.setPos(
            Display.centered(
                self.marge_width,
                width - 2 * self.marge_width,
                self.text.boundingRect().width()
            ),
            0
        )

        y = self.text.boundingRect().height() + self.marge_height

        self.current_round.setPos(
            (width - self.slash.boundingRect().width()) / 2 - self.max_round.boundingRect().width() - self.marge_width,
            y
        )
        self.slash.setPos(
            (width - self.slash.boundingRect().width()) / 2,
            y - 1
        )
        self.max_round.setPos(
            (width + self.slash.boundingRect().width()) / 2 + self.marge_width,
            y
        )
