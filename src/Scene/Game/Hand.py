# class Hand to manage user's and automaton's hands

from PyQt5.QtWidgets import QGraphicsItem

from src.Scene.Game.Spot import Spot
from src.SettingsManager import SettingsManager


class Hand(QGraphicsItem):

    def __init__(self):
        super().__init__()
        self.cards = []
        self.spots = [Spot(True, True) for i in range(SettingsManager.max_cards_in_hand())]

    def add(self, card):
        if len(self.cards) > SettingsManager.max_cards_in_hand():
            return False
        else:
            self.cards.append(card)
            card.setParentItem(self)
            card.setVisible(True)
            card.set_draggable(True)
            return True

    def remove(self, card):
        self.cards.remove(card)
        # TODO: gestion erreur si nombre_cartes = 0

    def show(self):
        return self.cards

    def is_empty(self):
        return len(self.cards) == 0




