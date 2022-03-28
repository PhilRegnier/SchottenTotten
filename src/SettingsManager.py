
#

from src.Singleton import Singleton


class SettingsManager(Singleton):

    __max_card_value = 9
    __max_cards_in_hand = 6
    __difficulty = 1
    __number_of_rounds = 1
    __sounds = False
    __variant = False
    __first_player = None

    def __init__(self):
        # TODO : loading personal settings saved
        pass

    @classmethod
    def get_number_of_rounds(cls):
        return cls.__number_of_rounds

    @classmethod
    def get_difficulty(cls):
        return cls.__difficulty

    @classmethod
    def set_difficulty(cls, difficulty):
        if 0 <= difficulty <= 1:
            cls.__difficulty = difficulty

    @classmethod
    def is_sounds_activate(cls):
        return cls.__sounds

    @classmethod
    def get_max_cards_in_hand(cls):
        return cls.__max_cards_in_hand

    @classmethod
    def switch_first_player(cls):
        if cls.__first_player == 1:
            cls.__first_player = 0
        else:
            cls.__first_player = 1

    @classmethod
    def get_first_player(cls):
        return cls.__first_player




