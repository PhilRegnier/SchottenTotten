#
# Home panel
#
from PIL import Image, ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

from src.Scene.Starter.ChifoumiCurtain import Chifoumi
from src.Scene.Clickable import Clickable
from src.Scene.Curtain import Curtain
from src.Scene.Starter.SettingsView import SettingsView
from src.SettingsManager import SettingsManager


class HomeCurtain(Curtain):

    def __init__(self, parent=None):
        super().__init__(parent)

        # get the instance of SettingsManager

        self.settings = SettingsManager()

        # prepare geometry

        ww = self.boundingRect().width()
        wh = self.boundingRect().height()
        cw = 0.15 * ww
        ew = 0.1 * ww

        # local items

        self.titre = QGraphicsPixmapItem()
        image = Image.open('resources/images/titre.png')
        image.thumbnail((2 * cw, 2 * cw))
        self.titre.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
        self.titre.setParentItem(self)

        # settings and starting buttons

        self.settings_button = Clickable('engrenages.jpg', cw, cw, self)
        self.starting_button = Clickable('run.jpg', cw, cw, self)

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

        super(HomeCurtain, self).mouseReleaseEvent(event)

        print("home: mouseRelease")
        if self.starting_button.selected:
            self.chifoumi.animate_incoming()
            self.chifoumi.start()
            return

        if self.settings_button.selected:
            self.settings_button.reset()
            self.settings_view.animate_incoming()
            return

    def leave(self):
        self.animate_leaving()

