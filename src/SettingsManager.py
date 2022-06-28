
#

from src.Singleton import Singleton


# TODO : loading personal settings saved
# TODO : pointing on player instance instead of using magic number

class SettingsManager(Singleton):

    CONST_PLAYER = 0
    CONST_AUTOMATON = 1

    __max_card_value = 9
    __max_cards_in_hand = 6
    __difficulty = 1
    __number_of_rounds = 2
    __sounds = False
    __variant = False
    __first_player = None
    __timer = 90

    __debug = True

    def __init__(self):
        pass

    @classmethod
    def get_max_card_value(cls):
        return cls.__max_card_value

    @classmethod
    def get_max_cards_in_hand(cls):
        return cls.__max_cards_in_hand

    @classmethod
    def get_number_of_rounds(cls):
        return cls.__number_of_rounds

    @classmethod
    def set_number_of_rounds(cls, number_of_rounds):
        cls.__number_of_rounds = number_of_rounds

    @classmethod
    def get_difficulty(cls):
        return cls.__difficulty

    @classmethod
    def set_difficulty(cls, difficulty):
        if 0 <= difficulty <= 1:
            cls.__difficulty = difficulty

    @classmethod
    def is_sounds_enabled(cls):
        return cls.__sounds

    @classmethod
    def set_sounds_enabled(cls, flag):
        cls.__sounds = flag

    @classmethod
    def max_cards_in_hand(cls):
        return cls.__max_cards_in_hand

    @classmethod
    def switch_first_player(cls):
        if cls.__first_player == cls.CONST_AUTOMATON:
            cls.__first_player = cls.CONST_PLAYER
        else:
            cls.__first_player = cls.CONST_AUTOMATON

    @classmethod
    def get_first_player(cls):
        return cls.__first_player

    @classmethod
    def set_first_player(cls, player):
        cls.__first_player = player

    @classmethod
    def get_variant(cls):
        return cls.__variant

    @classmethod
    def set_variant(cls, variant):
        cls.__variant = variant

    @classmethod
    def set_debug(cls):
        cls.__debug = True

    @classmethod
    def is_debugging(cls):
        return cls.__debug

    @classmethod
    def get_time(cls):
        return cls.__timer
