#
# Automate's cards zone
#
from PyQt5.QtCore import QPointF

from src import Statistics
from src.Side import Side
from src.variables_globales import auto_side_color0, auto_side_color1, auto_side_pen, card_height, userType


class AutoSide(Side):
    Type = userType + 4

    def __init__(self, numero, parent=None):
        super().__init__(numero, auto_side_color0, auto_side_color1, auto_side_pen, parent)

    def addCard(self, i):
        pos = QPointF(3, 3 + (2 - self.nCard) * card_height * 0.32)
        # card[i].moveTo(card[i].pos(),pos)
        Side.addCard(self, i, pos)
        Statistics.addCardToAutoSide(self)