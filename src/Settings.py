#
# Control panel
#
from src.Clickable import Clickable
from src.Curtain import Curtain
from src.Slider import Slider
from src.TextInForeground import TextInForeground
from src.variables_globales import variant, N_rounds, sounds, difficulT


class Settings(Curtain):

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

        if sounds:
            self.sound_selector.setSliderPosition(1)

        if variant:
            self.variant_selector.setSliderPosition(1)

        self.difficulty_selector.setSliderPosition(difficulT)
        self.rounds_selector.setSliderPosition(N_rounds - 1)

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

    def setValues(self):
        global N_rounds, sounds, difficulT
        N_rounds = self.rounds_selector.value()
        sounds = self.sound_selector.value() == 1
        difficulT = self.difficulty_selector.value()
