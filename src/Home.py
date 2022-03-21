#
# Home panel
#
from PIL import Image, ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

from src.Clickable import Clickable
from src.Curtain import Curtain
from src.Settings import Settings
from src.variables_globales import card_height


class Home(Curtain):

    def __init__(self, parent=None):
        super().__init__(parent)

        # prepare geometry

        ww = self.boundingRect().width()
        wh = self.boundingRect().height()
        cw = 2 * card_height
        ew = 80

        # title

        self.titre = QGraphicsPixmapItem()
        image = Image.open('resources/images/titre.png')
        image.thumbnail((2 * cw, 2 * cw))
        self.titre.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
        self.titre.setParentItem(self)

        # settings and starting buttons

        self.settings = Clickable('engrenages.jpg', cw, cw, 10, self)
        self.starting = Clickable('run.jpg', cw, cw, 11, self)

        # settings panel item

        self.settings_panel = Settings()
        self.settings_panel.setParentItem(self)
        self.settings_panel.setVisible(False)

        # continue geometry

        cw = self.settings.boundingRect().width()
        # ch = self.settings.boundingRect().height()

        # set the scene

        self.titre.setPos((ww - self.titre.boundingRect().width()) / 2,
                          wh / 2 - ew - self.titre.boundingRect().height())
        self.settings.setPos(ww / 2 - ew - cw, wh / 2 + ew)
        self.starting.setPos(ww / 2 + ew, wh / 2 + ew)

    def setValues(self):
        self.settings_panel.setValues()
        self.closeSettings()

    def closeSettings(self):
        self.settings_panel.animate_leaving()

    def openSettings(self):
        self.settings_panel.setVisible(True)
        self.settings_panel.animate_incoming()
