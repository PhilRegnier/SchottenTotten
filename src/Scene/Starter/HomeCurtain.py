#
# Home panel
#
from PIL import Image, ImageQt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

from src.Scene.Game.Card import Card
from src.Scene.Starter.ChifoumiCurtain import Chifoumi
from src.Scene.Clickable import Clickable
from src.Scene.Starter.Curtain import Curtain
from src.Scene.Starter.SettingsView import SettingsView
from src.SettingsManager import SettingsManager
from src.TextInForeground import TextInForeground


class HomeCurtain(Curtain):

    def __init__(self, parent=None):
        super().__init__(parent)

        # get the instance of SettingsManager

        self.settings = SettingsManager()

        # prepare geometry

        ww = self.boundingRect().width()
        wh = self.boundingRect().height()
        cw = 2 * Card.height
        ew = 80

        # local items

        self.titre = QGraphicsPixmapItem()
        image = Image.open('resources/images/titre.png')
        image.thumbnail((2 * cw, 2 * cw))
        self.titre.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
        self.titre.setParentItem(self)

        self.text = None

        # settings and starting buttons

        self.settings_button = Clickable('resources/images/engrenages.jpg', cw, cw, 10, self)
        self.starting_button = Clickable('resources/images/run.jpg', cw, cw, 11, self)

        # settings panel item

        self.settings_view = SettingsView(self)
        self.settings_view.setParentItem(self)
        self.settings_view.setVisible(False)

        # starter panel item

        self.chifoumi = Chifoumi(self)
        self.chifoumi.setParentItem(self)
        self.chifoumi.setVisible(False)

        # continue geometry

        cw = self.settings_button.boundingRect().width()
        # ch = self.settings_button.boundingRect().height()

        # set the scene

        self.titre.setPos((ww - self.titre.boundingRect().width()) / 2,
                          wh / 2 - ew - self.titre.boundingRect().height())
        self.settings_button.setPos(ww / 2 - ew - cw, wh / 2 + ew)
        self.starting_button.setPos(ww / 2 + ew, wh / 2 + ew)

    def mouseReleaseEvent(self, event):

        if self.starting_button.selected:
            if not self.starting_button.handled:
                self.starting_button.set_handled(True)
                self.chifoumi.setVisible(True)
                self.chifoumi.animate_incoming()
                self.chifoumi.start()

            else:
                self.starting_button.unselect()
                if self.settings.get_first_player() is None:
                    self.chifoumi.restart()
                else:
                    if self.settings.get_first_player() == self.settings.CONST_PLAYER:
                        self.text = TextInForeground("YOU ARE FIRST PLAYER !!", self.chifoumi)
                    else:
                        self.text = TextInForeground("AUTOMATE IS FIRST PLAYER !!", self.chifoumi)

                    self.text.setVisible(True)
                    self.chifoumi.freeze()
                    QTimer.singleShot(3000, self.start_the_game)

        if self.settings_button.selected:
            if not self.settings_button.handled:
                self.settings_button.set_handled(True)
                self.settings_view.setVisible(True)
                self.settings_view.animate_incoming()

            else:
                self.settings_button.unselect()
                if self.settings_view.ok_button.selected or self.settings_view.cancel_button.selected:
                    self.settings_view.animate_leaving()

    def start_the_game(self):
        self.text.setVisible(False)
        self.chifoumi.animate_leaving()
        self.home.animate_leaving()
        self.__new_round()
