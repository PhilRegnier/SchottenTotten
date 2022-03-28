#
# player's playmat
#
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QLinearGradient, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsItem

from src.Card import Card
from src.SettingsManager import Settings
from src.variables_globales import marge, pen_width, side_height, rBound


class PlayerDeck(QGraphicsItem):

    def __init__(self, color1, color2, color3, parent=None):
        super().__init__(parent)
        self.gcolor1 = color1
        self.gcolor2 = color2
        self.pcolor = color3
        self.width = 1.0 * (Settings.get_hand_nb() * (Card.width + marge) + marge)
        self.height = Card.height + marge * 2.0

    def boundingRect(self):
        return QRectF(-pen_width / 2, -pen_width / 2, self.width + pen_width, self.height + pen_width)

    def paint(self, painter, option, widget):
        gradient = QLinearGradient(0., side_height, 0., 0.)
        gradient.setSpread(QLinearGradient.ReflectSpread)
        gradient.setColorAt(0, self.gcolor1)
        gradient.setColorAt(1, self.gcolor2)
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(self.pcolor, 1))
        rect = QRectF(0., 0., float(self.width), float(self.height))
        painter.drawRoundedRect(rect, rBound, rBound)
