#
# player's playmat
#
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtWidgets import QGraphicsItem

from src.Style import GeometryStyle, GradientStyle


class Playmat(QGraphicsItem):

    width = 0
    height = 0

    def __init__(self, colors):
        super().__init__()

        if Playmat.width == 0:
            Playmat.set_size()

        self.gradient = GradientStyle(Playmat.height, colors.side0, colors.side1)
        self.pen_color = colors.side_pen

    def boundingRect(self):
        return QRectF(-GeometryStyle.pen_width / 2,
                      -GeometryStyle.pen_width / 2,
                      Playmat.width + GeometryStyle.pen_width,
                      Playmat.height + GeometryStyle.pen_width)

    def paint(self, painter, option, widget=0):
        painter.setBrush(QBrush(self.gradient))
        painter.setPen(QPen(self.pen_color, 1))
        rect = QRectF(0., 0., float(Playmat.width), float(Playmat.height))
        painter.drawRoundedRect(rect, GeometryStyle.r_bound, GeometryStyle.r_bound)

    @classmethod
    def set_size(cls):
        from src.SettingsManager import SettingsManager
        from src.Scene.Game.Card import Card

        settings_manager = SettingsManager()

        cls.width = 1.0 * (
                settings_manager.get_max_cards_in_hand()
                * (Card.width + GeometryStyle.marge)
                + GeometryStyle.marge
        )
        cls.height = Card.height + GeometryStyle.marge * 2.0
