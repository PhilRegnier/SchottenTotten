#
# Home panel
#
from PIL import Image, ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

from src.Card import Card
from src.Clickable import Clickable
from src.Curtain import Curtain
from src.SettingsView import SettingsView


class Home(Curtain):

    def __init__(self, parent):
        super().__init__(parent)

        # prepare geometry

        ww = self.boundingRect().width()
        wh = self.boundingRect().height()
        cw = 2 * Card.card_height
        ew = 80

        # title

        self.titre = QGraphicsPixmapItem()
        image = Image.open('resources/images/titre.png')
        image.thumbnail((2 * cw, 2 * cw))
        self.titre.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
        self.titre.setParentItem(self)

        # settings and starting buttons

        self.settings_button = Clickable('resources/images/engrenages.jpg', cw, cw, 10, self)
        self.starting_button = Clickable('resources/images/run.jpg', cw, cw, 11, self)

        # settings panel item

        self.settings_view = SettingsView(self)
        self.settings_view.setParentItem(self)
        self.settings_view.setVisible(False)

        # continue geometry

        cw = self.settings_button.boundingRect().width()
        # ch = self.settings_button.boundingRect().height()

        # set the scene

        self.titre.setPos((ww - self.titre.boundingRect().width()) / 2,
                          wh / 2 - ew - self.titre.boundingRect().height())
        self.settings_button.setPos(ww / 2 - ew - cw, wh / 2 + ew)
        self.starting_button.setPos(ww / 2 + ew, wh / 2 + ew)

    def set_values(self):
        self.settings_view.get_values(number_of_rounds, sounds_enabled, difficulty)
        self.settings.set_number_of_rounds(self.rounds_selector.value())
        self.settings.set_sounds_enabled(self.sound_selector.value() == 1)
        self.settings.set_difficulty(self.difficulty_selector.value())
        self.settings_view.animate_leaving()

    def open_settings_view(self):
        self.settingsView.setVisible(True)
        self.settingsView.animate_incoming()
