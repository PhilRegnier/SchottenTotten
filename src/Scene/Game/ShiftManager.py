from src.Singleton import Singleton


class ShiftManager(Singleton):

    card = None
    side = None
    hand = None
    card_hover = None

    dragged = False
    moved_to_reorganize = False
    sort = False

    def __init__(self):
        pass

    @classmethod
    def set_card(cls, card):
        cls.card = card
        cls.dragged = True

    @classmethod
    def set_hand(cls, hand):
        cls.hand = hand

    @classmethod
    def set_side(cls, side):
        cls.side = side

    @classmethod
    def select(cls, card, side, hand):
        cls.card = card
        cls.side = side
        cls.hand = hand
        cls.sort = False
        cls.dragged = False

    @classmethod
    def reset(cls):
        cls.card.set_dragged(False)
        cls.card = None
        cls.side = None
        cls.hand = None

    @classmethod
    def user_dont_want_to_reorganize(cls):
        cls.moved_to_reorganize = False
        cls.card_hover = None

    @classmethod
    def user_want_to_reorganize(cls):
        cls.moved_to_reorganize = True

    @classmethod
    def is_moved_to_reorganize(cls):
        return cls.moved_to_reorganize

    @classmethod
    def is_dragged(cls):
        return cls.dragged

    @classmethod
    def set_dragged(cls, flag):
        cls.dragged = flag
