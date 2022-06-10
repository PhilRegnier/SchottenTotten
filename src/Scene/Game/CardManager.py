"""""
    manager for the playing cards

    Responsabilities:
        - holding all the instances of cards
        - manage action with the cards
        - manage cards' shifts

"""
from random import shuffle

from src.Scene.Game.Card import Card
from src.Singleton import Singleton


class CardManager(Singleton):

    card_dx = 0.
    zmax = 0.

    max_value = 9
    cards = []
    colors = ['jaune', 'vert', 'rouge', 'brun', 'bleu', 'violet']

    total_cards = len(colors) * max_value

    def __init__(self):
        pass

    def set_zmax(self, zmax):
        self.zmax = max(self.zmax, zmax)

    def get_zmax(self):
        return self.zmax

    def reset_zmax(self):
        self.zmax = 0.

    # Setting all the instances of playing cards
    @classmethod
    def initialize(cls):
        for numero in range(cls.total_cards):
            valeur = numero % cls.max_value + 1
            couleur = cls.colors[numero // cls.max_value]
            cls.cards.append(Card(numero, valeur, couleur))

    @classmethod
    def get_total_cards(cls):
        return cls.total_cards

    @classmethod
    def get_deck(cls, deck):
        shuffle(cls.cards)
        for card in cls.cards:
            card.setParentItem(deck)
            card.setPos(0, 0)
            card.setVisible(False)

        return cls.cards

    @classmethod
    def pick_up_cards(cls, cards):
        cls.cards.extend(cards)

    @classmethod
    def reset_cards(cls):
        for card in cls.cards:
            card.set_draggable(False)
            card.setZValue(0.0)

