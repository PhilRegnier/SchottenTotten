
from src.Clickable import Clickable
from src.Curtain import Curtain
from src.SettingsManager import SettingsManager
from src.Slider import Slider
from src.TextInForeground import TextInForeground


class SettingsView(Curtain):

    def __init__(self, parent=None):
        super().__init__(parent)

        # get the instance of SettingsManager

        settings = SettingsManager()

        # prepare geometry

        ww = self.boundingRect().width()
        # wh = self.boundingRect().height()
        lw = int(ww / 4)
        mh = 20

        # Set title

        self.title = TextInForeground("SETTINGS", self)

        # Set selectors

        self.sound_slider = Slider(self, 'Sound')
        self.variant_slider = Slider(self, 'Variant')
        self.difficulty_slider = Slider(self, 'Difficulty', 2, ['dumb', 'spicy'])
        self.rounds_slider = Slider(self, 'Number of rounds', 5, ['1', '2', '3', '4', '5'])

        self.rounds_slider.setRange(1, 5)

        if settings.__sounds:
            self.sound_slider.setSliderPosition(1)

        if settings.__variant:
            self.variant_selector.setSliderPosition(1)

        self.difficulty_selector.setSliderPosition(Settings.__difficulty)
        self.rounds_selector.setSliderPosition(Settings.__number_of_rounds - 1)

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

    def set_values(self):
        Settings.__number_of_rounds = self.rounds_selector.value()
        Settings.__sounds = self.sound_selector.value() == 1
        Settings.__difficulty = self.difficulty_selector.value()