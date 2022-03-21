#
# Common side definitions
#
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QLinearGradient, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsItem

from src.variables_globales import stone_width, side_height, rBound, card


class Side(QGraphicsItem):

    def __init__(self, numero, color0, color1, pen, parent=None):
        super().__init__(parent)
        self.numero = numero
        self.nCard = 0
        self.index = []
        self.somme = 0
        self.setFlag(QGraphicsItem.ItemDoesntPropagateOpacityToChildren)
        self.setOpacity(0.5)
        self.color0 = color0
        self.color1 = color1
        self.pen = pen

    def boundingRect(self):
        penWidth = 1.0
        return QRectF(-penWidth / 2, -penWidth / 2, stone_width + penWidth, side_height + penWidth)

    def paint(self, painter, option, widget):
        gradient = QLinearGradient(0., side_height, 0., 0.)
        gradient.setSpread(QLinearGradient.ReflectSpread)
        gradient.setColorAt(0, self.color0)
        gradient.setColorAt(1, self.color1)
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(self.pen, 1))
        rect = QRectF(0., 0., float(stone_width), float(side_height))
        painter.drawRoundedRect(rect, rBound, rBound)

    def addCard(self, i, pos):
        self.index.append(i)
        card[i].setAnchorPoint(pos)
        card[i].setParentItem(self)
        card[i].setIndex(-1)
        self.nCard += 1
        self.somme += card[i].valeur
