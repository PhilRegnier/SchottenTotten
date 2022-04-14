#
# Common side definitions
#
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QLinearGradient, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsItem

from src.Scene.Game.Card import Card
from src.Scene.Game.Stone import Stone
from src.variables_globales import rBound


class Side(QGraphicsItem):

    height = Card.height * 1.667

    def __init__(self, numero, color0, color1, pen, parent):
        super().__init__(parent)
        self.numero = numero
        self.cards = []
        self.somme = 0
        self.color0 = color0
        self.color1 = color1
        self.pen = pen
        self.setFlag(QGraphicsItem.ItemDoesntPropagateOpacityToChildren)
        self.setOpacity(0.5)

    def boundingRect(self):
        pen_width = 1.0
        return QRectF(-pen_width / 2, -pen_width / 2, Stone.width + pen_width, Side.height + pen_width)

    def paint(self, painter, option, widget):
        gradient = QLinearGradient(0., Side.height, 0., 0.)
        gradient.setSpread(QLinearGradient. ReflectSpread)
        gradient.setColorAt(0, self.color0)
        gradient.setColorAt(1, self.color1)
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(self.pen, 1))
        rect = QRectF(0., 0., float(Stone.width), float(Side.height))
        painter.drawRoundedRect(rect, rBound, rBound)

    def add_card(self, card):
        pos = QPointF(3, 3 + len(self.cards) * card.height * 0.32)
        card.setAnchorPoint(pos)
        card.setParentItem(self)
        card.setIndex(-1)
        self.cards.append(card)
        self.somme += card.valeur
        card.setPos(pos)
