# class Hand to manage user's and automate's hands
from src.SettingsManager import SettingsManager


class Hand:

    def __init__(self):
        self.cards = []
        self.settingsManager = SettingsManager()

    def add(self, card):
        if len(self.cards) > self.settingsManager.get_max_cards_in_hand():
            return False
        else:
            self.cards.append(card)
            return True

    def remove(self, card):
        self.cards.remove(card)

    def get(self, index):
        return self.cards[index]

    def show(self):
        return self.cards

    def is_empty(self):
        return not self.cards




