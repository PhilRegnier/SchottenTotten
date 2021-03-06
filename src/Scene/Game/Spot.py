"""
    Spot where a card can be moved.
    A spot has a fixed position, relative to its <code>parentItem</code>,
    is <code>fillable</code> or not,
    is <code>free</code> or not.

    If a spot is free and fillable, it is highlighting
    when a card is moved over it to indicate the drop
    is possible.

    Spot gets the same boundingRect and paint methods as Card.

"""
from PyQt6.QtCore import QRect, QRectF
from PyQt6.QtGui import QBrush, QColorConstants
from PyQt6.QtWidgets import QGraphicsObject

from src.Style import MainGeometry


class Spot(QGraphicsObject):

    def __init__(self, index, fillable, parent_item):
        super().__init__()
        self.index = index
        self.fillable = fillable
        self.setParentItem(parent_item)
        self.free = True

    def set_free(self, flag):
        self.free = flag

    def boundingRect(self):
        from src.Scene.Game.Card import Card
        from src.Scene.Game.Side import Side
        pen_width = 1.0
        return QRectF(-pen_width / 2, -pen_width / 2, Card.width + pen_width, Side.height + pen_width)

    def paint(self, painter, option, widget=0):
        from src.Scene.Game.Card import Card
        painter.setBrush(QBrush(QColorConstants.Cyan))
        painter.setOpacity(0.3)
        rect = QRect(-1, -1, int(Card.width), int(Card.height))
        painter.drawRoundedRect(rect, MainGeometry.r_bound, MainGeometry.r_bound)
