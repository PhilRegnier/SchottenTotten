#
# Home panel
#
from PIL import Image, ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

from src.Scene.Game.Card import Card
from src.Scene.Starter.ChifoumiCurtain import Chifoumi
from src.Scene.Clickable import Clickable
from src.Scene.Starter.Curtain import Curtain
from src.Scene.Starter.SettingsCurtain import SettingsView


class HomeCurtain(Curtain):

    def __init__(self, parent = None):
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

    def mouseReleaseEvent(self, event):

            self.chifoumi = Chifoumi()
            self.board.addItem(self.chifoumi)
            self.chifoumi.animate_incoming()
            self.chifoumi.start()

            # ... Chifoumi

        if selected < 3:
            self.chifoumi.choosePlayer()

            if Settings.get_first_player() == -1:
                self.chifoumi.restart()
            else:
                if Settings.get_first_player() == 0:
                    self.text = TextInForeground("YOU ARE FIRST PLAYER !!", self.chifoumi)
                else:
                    self.text = TextInForeground("AUTOMATE IS FIRST PLAYER !!", self.chifoumi)

                self.text.setVisible(True)
                self.chifoumi.freeze()
                QTimer.singleShot(3000, self.letsGo)

            # ... Settings

        if selected == 20:
            self.home.setValues()

        if selected == 21:
            self.home.closeSettings()

        clicked = False
        selected = -1

        # Leave chifoumi curtain and launch the game

    def letsGo(self):
        self.text.setVisible(False)
        self.chifoumi.animate_leaving()
        self.home.animate_leaving()
        self.__new_round()
