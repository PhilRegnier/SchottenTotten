#
# player's playmat
#
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtWidgets import QGraphicsItem

from src.Scene.Game.Card import Card
from src.Scene.Game.Side import Side
from src.SettingsManager import SettingsManager
from src.Style import GeometryStyle, GradientStyle


class Playmat(QGraphicsItem):

    def __init__(self, color1, color2, color3):
        super().__init__()

        settings_manager = SettingsManager()

        self.gradient = GradientStyle(Side.height, color1, color2)
        self.pen_color = color3

        self.width = 1.0 * (settings_manager.get_max_cards_in_hand()
                            * (Card.width + GeometryStyle.marge)
                            + GeometryStyle.marge)

        self.height = Card.height + GeometryStyle.marge * 2.0

    def boundingRect(self):
        return QRectF(-GeometryStyle.pen_width / 2,
                      -GeometryStyle.pen_width / 2,
                      self.width + GeometryStyle.pen_width,
                      self.height + GeometryStyle.pen_width)

    def paint(self, painter, option, widget=0):
        painter.setBrush(QBrush(self.gradient))
        painter.setPen(QPen(self.pen_color, 1))
        rect = QRectF(0., 0., float(self.width), float(self.height))
        painter.drawRoundedRect(rect, GeometryStyle.r_bound, GeometryStyle.r_bound)
