#
# User's cards drop zone
#
from PyQt5.QtCore import QPointF

from src.Card import Card
from src.Side import Side
from src.Style import Style
from src.variables_globales import userType


class UserSide(Side):
    Type = userType + 3

    def __init__(self, numero, parent=None):
        super().__init__(numero, Style.user_side_color0, Style.user_side_color1, Style.user_side_pen, parent)

    def add_card(self, i):
        pos = QPointF(3, 3 + self.nCard * Card.height * 0.32)
        Side.add_card_to_side(self, i, pos)
        Card.cards[i].setPos(pos)
