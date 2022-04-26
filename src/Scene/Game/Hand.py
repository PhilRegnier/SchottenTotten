# class Hand to manage user's and automate's hands
from PyQt5.QtWidgets import QGraphicsItem

from src.Scene.Game.Spot import Spot
from src.SettingsManager import SettingsManager


class Hand(QGraphicsItem):

    def __init__(self):
        self.nombre_cartes = 0
        self.settingsManager = SettingsManager()

        self.spots = [Spot(true, true) for i in range(self.settingsManager.max_cards_in_hand())]

    def add(self, card):
        if self.nombre_cartes > self.settingsManager.max_cards_in_hand():
            return False
        else:
            card.setParentItem(self)
            self.nombre_cartes += 1
            return True

    def remove(self, card):
        self.cards.remove(card)

    def get_card_at(self, index):
        return self.cards[index]

    def show(self):
        return self.cards

    def is_empty(self):
        return not self.cards




