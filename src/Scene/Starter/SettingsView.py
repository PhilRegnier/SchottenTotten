
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

        self.rounds_slider.set_range(1, 5)

        if self.settings.is_sounds_enabled():
            self.sound_slider.set_position(1)

        if self.settings.get_variant():
            self.variant_slider.set_position(1)

        self.difficulty_slider.set_position(self.settings.get_difficulty())
        self.rounds_slider.set_position(self.settings.get_number_of_rounds() - 1)

        # Set "OK" and "CANCEL" buttons

        self.ok_button = Clickable('ok.png', 50, 50, self, True)
        self.cancel_button = Clickable('cancel.png', 50, 50, self, True)

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

    def mouseReleaseEvent(self, event):

        # TODO : implement variant_slider chosen value
        if self.ok_button.selected:
            self.settings.set_number_of_rounds(self.rounds_slider.value())
            self.settings.set_sounds_enabled(self.sound_slider.value() == 1)
            self.settings.set_difficulty(self.difficulty_slider.value())
            self.ok_button.unselect()
            self.animate_leaving()

        elif self.cancel_button.selected:
            self.cancel_button.unselect()
            self.animate_leaving()

        else:
            Curtain.mouseReleaseEvent(self, event)
