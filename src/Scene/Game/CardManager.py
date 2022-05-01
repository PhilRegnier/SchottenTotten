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

    # Setting all the instances of playing cards
    @classmethod
    def initialize(cls):
        for numero in range(cls.total_cards):
            valeur = numero % cls.max_value + 1
            couleur = cls.colors[numero // cls.max_value]
            cls.cards.append(Card(numero, valeur, couleur))

    @classmethod
    def set_zmax(cls, zmax):
        cls.zmax = max(cls.zmax, zmax)

    @classmethod
    def get_zmax(cls):
        return cls.zmax

    @classmethod
    def reset_zmax(cls):
        cls.zmax = 0.

    @classmethod
    def get_total_cards(cls):
        return cls.total_cards

    @classmethod
    def set_deck(cls, deck):
        shuffle(cls.cards)
        for card in cls.cards:
            card.setParentItem(deck)
            card.setPos(0, 0)
            card.setVisible(False)

    @classmethod
    def get_a_card(cls):
        return cls.cards[0]
