
from src.Scene.Clickable import Clickable
from src.Scene.Starter.Curtain import Curtain
from src.SettingsManager import SettingsManager
from src.Scene.Starter.Slider import Slider
from src.TextInForeground import TextInForeground


class SettingsView(Curtain):

    def __init__(self, parent):
        super().__init__(parent)

        # get the instance of SettingsManager

        self.settings = SettingsManager()

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

        if self.settings.is_sounds_enabled():
            self.sound_slider.setSliderPosition(1)

        if self.settings.get_variant():
            self.variant_slider.setSliderPosition(1)

        self.difficulty_slider.setSliderPosition(self.settings.get_difficulty())
        self.rounds_slider.setSliderPosition(self.settings.get_number_of_rounds() - 1)

        # Set "OK" and "CANCEL" buttons

        self.ok_button = Clickable('reources/images/ok.png', 50, 50, 20, self, True)
        self.cancel_button = Clickable('resources/images/cancel.png', 50, 50, 21, self, True)

        # Set the scene

        y = mh
        self.title.setPos(lw, y)
        y += mh + self.title.boundingRect().height() + 60
        self.sound_slider.setPos(lw, y)
        y += mh + self.sound_slider.height
        self.difficulty_slider.setPos(lw, y)
        y += mh + self.difficulty_slider.height
        self.rounds_slider.setPos(lw, y)
        y += mh + self.rounds_slider.height
        self.variant_slider.setPos(lw, y)
        y += mh + self.variant_slider.height

        self.ok_button.setPos(lw, y)
        self.cancel_button.setPos(lw + self.difficulty_slider.width, y)

    def get_number_of_rounds_selected(self):
        return self.rounds_slider.value()

    def get_sounds_enabled_selected(self):
        return self.sound_slider.value() == 1

    def get_difficulty_selected(self):
        return self.difficulty_slider.value()

    def get_variant_selected(self):
        return self.variant_slider.value()
