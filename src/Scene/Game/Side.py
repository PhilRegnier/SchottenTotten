#
# Common side definitions
#
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QLinearGradient, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsItem

from src.Scene.Game.Card import Card
from src.Scene.Game.Stone import Stone
from src.Style import GeometryStyle, GradientStyle


class Side(QGraphicsItem):

    height = Card.height * 1.667

    def __init__(self, numero, color1, color2, color3, parent):
        super().__init__(parent)
        self.numero = numero
        self.cards = []
        self.somme = 0
        self.gradient = GradientStyle(Side.height, color1, color2)
        self.pen_color = color3
        self.setFlag(QGraphicsItem.ItemDoesntPropagateOpacityToChildren)
        self.light_off()

    def boundingRect(self):
        return QRectF(-GeometryStyle.pen_width / 2,
                      -GeometryStyle.pen_width / 2,
                      Stone.width + GeometryStyle.pen_width,
                      Side.height + GeometryStyle.pen_width)

    def paint(self, painter, option, widget=0):
        painter.setBrush(QBrush(self.gradient))
        painter.setPen(QPen(self.pen_color, 1))
        rect = QRectF(0., 0., float(Stone.width), float(Side.height))
        painter.drawRoundedRect(rect, GeometryStyle.r_bound, GeometryStyle.r_bound)

    def add_card(self, card):
        pos = QPointF(3, 3 + len(self.cards) * card.height * 0.32)
        card.setAnchorPoint(pos)
        card.setParentItem(self)
        card.setIndex(-1)
        self.cards.append(card)
        self.somme += card.valeur
        card.setPos(pos)

    def light_on(self):
        self.setOpacity(1.0)

    def light_off(self):
        self.setOpacity(0.5)

    def is_full(self):
        return len(self.cards) == 3
