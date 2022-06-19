from src.Singleton import Singleton


class ShiftManager(Singleton):

    card = None
    side = None
    card_hover = None

    dragged = False
    moved_to_reorganize = False
    sort = False

    starting_pos = None

    def __init__(self):
        pass

    @classmethod
    def set_starting_pos(cls, pos):
        cls.starting_pos = pos

    @classmethod
    def set_card(cls, card):
        cls.card = card
        cls.dragged = True

    @classmethod
    def set_side(cls, side):
        cls.side = side

    @classmethod
    def select(cls, card, side):
        cls.card = card
        cls.side = side
        cls.sort = False
        cls.dragged = False

    @classmethod
    def reset(cls):
        cls.dragged = False
        cls.card = None
        cls.side = None

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

