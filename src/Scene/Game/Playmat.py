#
# player's playmat
#
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtWidgets import QGraphicsItem

from src.Scene.Game.Card import Card
from src.Scene.Game.Spot import Spot
from src.SettingsManager import SettingsManager
from src.Style import MainGeometry, GradientStyle


class Playmat(QGraphicsItem):

    width = 0
    height = 0

    def __init__(self, colors):
        super().__init__()

        if Playmat.width == 0:
            Playmat.set_size()

        self.gradient = GradientStyle(Playmat.height, colors.side0, colors.side1)
        self.pen_color = colors.side_pen

        self.spots = []
        for i in range(SettingsManager.max_cards_in_hand()):
            spot = Spot(i, True, self)
            spot.setPos((i + 1) * MainGeometry.spot_marge + i * Card.width, MainGeometry.spot_marge)
            spot.setVisible(True)
            self.spots.append(spot)

        self.cards = []

    def boundingRect(self):
        return QRectF(-MainGeometry.pen_width / 2,
                      -MainGeometry.pen_width / 2,
                      Playmat.width + MainGeometry.pen_width,
                      Playmat.height + MainGeometry.pen_width)

    def paint(self, painter, option, widget=0):
        painter.setBrush(QBrush(self.gradient))
        painter.setPen(QPen(self.pen_color, 1))
        rect = QRectF(0., 0., float(Playmat.width), float(Playmat.height))
        painter.drawRoundedRect(rect, MainGeometry.r_bound, MainGeometry.r_bound)

    def add(self, card, draggable=False, index=None):
        # TODO : Animation du déplacement de la carte
        if len(self.cards) > SettingsManager.max_cards_in_hand():
            print("Playmat.add: impossible d'ajouter une carte (main complète)",
                  len(self.cards),
                  SettingsManager.max_cards_in_hand())
            return False
        else:
            card.setParentItem(self)
            if index is None:
                for spot in self.spots:
                    if spot.free:
                        card.setPos(spot.pos())
                        card.set_index(spot.index)
                        spot.set_free(False)
                        break

            elif 0 <= index <= SettingsManager.max_cards_in_hand():
                if self.spots[index].free:
                    card.setPos(self.spots[index].pos())
                    card.set_index(index)
                else:
                    print("Playmat.add: spot occupé !")
                    return False
            else:
                print("Playmat.add: impossible d'ajouter une carte")
                return False

            card.setVisible(True)
            card.set_draggable(draggable)
            card.set_anchor_point(card.pos())
            self.cards.append(card)

            return True

    def remove(self, card):
        self.cards.remove(card)
        self.spots[card.index].set_free(True)
        # TODO: gestion erreur si nombre_cartes = 0

    def show(self):
        return self.cards

    def is_empty(self):
        return len(self.cards) == 0

    @classmethod
    def set_size(cls):
        from src.SettingsManager import SettingsManager
        from src.Scene.Game.Card import Card

        settings_manager = SettingsManager()

        cls.width = 1.0 * (
                settings_manager.get_max_cards_in_hand()
                * (Card.width + MainGeometry.spot_marge)
                + MainGeometry.spot_marge
        )
        cls.height = Card.height + MainGeometry.spot_marge * 2.0

