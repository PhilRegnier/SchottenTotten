#
# Common side definitions
#
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtWidgets import QGraphicsItem

from src.Scene.Game.Stone import Stone
from src.Style import GeometryStyle, GradientStyle

# TODO : change to QGraphicsObect to directly handle mouse EnterEvent and DropEvent


class Side(QGraphicsItem):

    HCARD_RATIO = 1.667
    width = 0
    height = 0

    def __init__(self, numero, colors, parent):
        super().__init__()
        self.numero = numero
        self.parent = parent
        self.cards = []
        self.somme = 0
        if Side.width == 0:
            Side.set_size()

        self.gradient = GradientStyle(Side.height, colors.side0, colors.side1)
        self.pen_color = colors.side_pen
        self.setFlag(QGraphicsItem.ItemDoesntPropagateOpacityToChildren)
        self.light_off()

    @classmethod
    def set_size(cls):
        from src.Scene.Game.Card import Card

        if Stone.width == 0 or Card.height == 0:
            print("ERREUR : Stones and cards must be instanciated before sides for sizing purpose.")
        cls.width = Stone.width
        cls.height = Card.height * cls.HCARD_RATIO

    def boundingRect(self):
        return QRectF(-GeometryStyle.pen_width / 2,
                      -GeometryStyle.pen_width / 2,
                      Side.width + GeometryStyle.pen_width,
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
