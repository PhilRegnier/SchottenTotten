#
# Control panel
#
from src.Clickable import Clickable
from src.Curtain import Curtain
from src.Slider import Slider
from src.TextInForeground import TextInForeground
from src.variables_globales import variant, N_rounds, sounds, difficulT


class Settings(Curtain):

    __max_value = 9
    number_max_of_cards_in_hand = 6
    __difficulty = 1
    __rounds_nb = 1
    __sounds = False
    __variant = False
    __first_player = 0  # O=user (default); 1=automate

    def __init__(self, parent=None):
        super().__init__(parent)

        # prepare geometry

        ww = self.boundingRect().width()
        # wh = self.boundingRect().height()
        lw = int(ww / 4)
        mh = 20

        # Set title

        self.title = TextInForeground("SETTINGS", self)

        # Set selectors

        self.sound_selector = Slider(self, 'Sound')
        self.variant_selector = Slider(self, 'Variant')
        self.difficulty_selector = Slider(self, 'Difficulty', 2, ['dumb', 'spicy'])
        self.rounds_selector = Slider(self, 'Number of rounds', 5, ['1', '2', '3', '4', '5'])

        self.rounds_selector.setRange(1, 5)

        if Settings.__sounds:
            self.sound_selector.setSliderPosition(1)

        if variant:
            self.variant_selector.setSliderPosition(1)

        self.difficulty_selector.setSliderPosition(Settings.__difficulty)
        self.rounds_selector.setSliderPosition(Settings.__rounds_nb - 1)

        # Set "OK" and "CANCEL" buttons

        self.ok = Clickable('ok.png', 50, 50, 20, self, True)
        self.cancel = Clickable('cancel.png', 50, 50, 21, self, True)

        # Set the scene

        y = mh
        self.title.setPos(lw, y)
        y += mh + self.title.boundingRect().height() + 60
        self.sound_selector.setPos(lw, y)
        y += mh + self.sound_selector.height
        self.difficulty_selector.setPos(lw, y)
        y += mh + self.difficulty_selector.height
        self.rounds_selector.setPos(lw, y)
        y += mh + self.rounds_selector.height
        self.variant_selector.setPos(lw, y)
        y += mh + self.variant_selector.height
        self.ok.setPos(lw, y)
        self.cancel.setPos(lw + self.difficulty_selector.width, y)

    @staticmethod
    def setValues(self):
        Settings.__rounds_nb = self.rounds_selector.value()
        Settings.__sounds = self.sound_selector.value() == 1
        Settings.__difficulty = self.difficulty_selector.value()

    @staticmethod
    def get_rounds_nb():
        return Settings.__rounds_nb

    @staticmethod
    def get_difficulty():
        return Settings.__difficulty

    @staticmethod
    def get_sounds():
        return Settings.__sounds

    @staticmethod
    def get_hand_nb():
        return Settings.__hand_nb

    @staticmethod
    def switch_first_player():
        if Settings.__first_player == 1:
            Settings.__first_player = 0
        else:
            Settings.__first_player = 1

    @staticmethod
    def get_first_player():
        return Settings.__first_player




