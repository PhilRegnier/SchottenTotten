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

    card_hover = -1
    card_dx = 0.
    zmax = 0.

    max_value = 9
    cards = []
    total_cards = len(Card.colors) * max_value

    colors = ['jaune', 'vert', 'rouge', 'brun', 'bleu', 'violet']

    shift_card = None
    shift_side = None
    shift_hand = None
    dragged = False
    moved_to_reorganize = False

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
    def select(cls, card, side, hand):
        cls.shift_card = card
        cls.shift_side = side
        cls.shift_hand = hand
        cls.shift_sort = False
        cls.dragged = False

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
    def user_dont_want_to_reorganize(cls):
        cls.moved_to_reorganize = False
        cls.card_hover = -1

    @classmethod
    def user_want_to_reorganize(cls):
        cls.moved_to_reorganize = True

    @classmethod
    def is_moved_to_reorganize(cls):
        return cls.moved_to_reorganize

    @classmethod
    def is_dagged(cls):
        return cls.dragged

    @classmethod
    def set_dragged(cls, flag):
        cls.dragged = flag

    @classmethod
    def set_shift_card(cls, card):
        cls.shift_card = card

    @classmethod
    def set_shift_hand(cls, hand):
        cls.shift_hand = hand

    @classmethod
    def set_shift_side(cls, side):
        cls.shift_side = side

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
