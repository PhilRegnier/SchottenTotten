#
# User's cards drop zone
#
from PyQt5.QtCore import QPointF

from src.Side import Side
from src.variables_globales import userType, user_side_color0, user_side_color1, user_side_pen, card_height, card


class UserSide(Side):
    Type = userType + 3

    def __init__(self, numero, parent=None):
        super().__init__(numero, user_side_color0, user_side_color1, user_side_pen, parent)

    def addCard(self, i):
        pos = QPointF(3, 3 + self.nCard * card_height * 0.32)
        Side.addCard(self, i, pos)
        card[i].setPos(pos)