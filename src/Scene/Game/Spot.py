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
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QGraphicsObject

from src.Scene.Game.Card import Card
from src.Style import GeometryStyle


class Spot(QGraphicsObject):

    def __init__(self, fillable, free):
        super().__init__()
        self.fillable = fillable
        self.free = free

    def boundingRect(self):
        return Card.boundingRect()

    def paint(self, painter, option, widget=0):
        painter.setBrush(QBrush(Qt.cyan))
        painter.setOpacity(0.3)
        rect = QRect(-1, -1, int(Card.width), int(Card.height))
        painter.drawRoundedRect(rect, GeometryStyle.r_bound, GeometryStyle.r_bound)
