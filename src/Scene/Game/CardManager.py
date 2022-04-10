"""""
    manager for the playing cards

    Responsabilities:
        - holding all the instances of cards
        - manage action with the cards

"""

from src.Scene.Game.Card import Card
from src.Singleton import Singleton


class CardManager(Singleton):

    card_hover = -1
    card_dx = 0.
    zmax = 0.

    max_value = 9
    cards = []
    total_cards = len(Card.colors) * max_value

    card = None
    side = None
    hand = None
    dragged = False
    moved_to_reorganize = False

    def __init__(self):
        pass

    # Setting all the playing cards
    @classmethod
    def initialize(cls):
        for i in range(cls.total_cards):
            cls.cards.append(Card(i, cls.max_value))

    @classmethod
    def select(cls, card, side, hand):
        cls.card = card
        cls.side = side
        cls.hand = hand
        cls.sort = False
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
    def dragged(cls):
        cls.dragged = True

    @classmethod
    def undragged(cls):
        cls.dragged = False

    @classmethod
    def set_card_id(cls, card_id):
        cls.card_id = card_id

    @classmethod
    def card_id(cls):
        return cls.card_id

    @classmethod
    def set_hand_id(cls, hand_id):
        cls.__hand_id = hand_id

    @classmethod
    def hand_id(cls):
        return cls.hand_id

    @classmethod
    def set_side_id(cls, side_id):
        cls.__side_id = side_id

    @classmethod
    def side_id(cls):
        return cls.side_id
