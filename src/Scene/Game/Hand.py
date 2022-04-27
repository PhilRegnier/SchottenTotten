# class Hand to manage user's and automate's hands
from PyQt5.QtWidgets import QGraphicsItem

from src.Scene.Game.Spot import Spot
from src.SettingsManager import SettingsManager


class Hand(QGraphicsItem):

    def __init__(self):
        super().__init__()
        self.nombre_cartes = 0
        self.settingsManager = SettingsManager()

        self.spots = [Spot(True, True) for i in range(self.settingsManager.max_cards_in_hand())]

    def add(self, card):
        if self.nombre_cartes > self.settingsManager.max_cards_in_hand():
            return False
        else:
            self.nombre_cartes += 1
            card.setParentItem(self)
            card.setVisible(True)
            card.setDraggable(True)
            return True

    def lose_a_card(self, card):
        self.nombre_cartes -= 1
        # TODO: gestion erreur si nombre_cartes = 0

    def show(self):
        return self.cards

    def is_empty(self):
        return self.nombre_cartes == 0




