#
# Automate's cards zone
#
from PyQt5.QtCore import QPointF

from src.Scene.Game import Statistics
from src.Scene.Game.Card import Card
from src.Scene.Game.Side import Side
from src.Style import Style
from src.variables_globales import userType


class AutoSide(Side):
    Type = userType + 4

    def __init__(self, numero, parent=None):
        super().__init__(numero, Style.auto_side_color0, Style.auto_side_color1, Style.auto_side_pen, parent)

    def add_card(self, i):
        pos = QPointF(3, 3 + (2 - self.nCard) * Card.height * 0.32)
        # card[i].moveTo(card[i].pos(),pos)
        Side.add_card_to_side(self, i, pos)
        Statistics.add_cardToAutoSide(self)
