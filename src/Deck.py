# ------------------------------------------------------------------------------------------------------
# Deck definition
# ------------------------------------------------------------------------------------------------------
from random import shuffle

from PIL import ImageQt, Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

from src.Card import Card
from src.ImageTreatment import ImageTreatment
from src.Style import Style
from src.variables_globales import userType, rBound


class Deck(QGraphicsPixmapItem):
    Type = userType + 2

    def __init__(self, parent=None):
        super().__init__(parent)

        # geometry

        self.x1 = 0
        self.y1 = 0
        self.width = 0
        self.height = 0

        self.__stack()
        self.empty = False

        self.nc = Card.total_cards

        # making a random deck

        liste_cartes = [i for i in range(self.nc)]
        shuffle(liste_cartes)

        self.index = liste_cartes

        for i in range(Card.total_cards):
            Card.cards[i].setParentItem(self)
            Card.cards[i].setPos(0, 0)
            Card.cards[i].setVisible(False)

    def is_empty(self):
        return self.empty

    def draw(self):
        card = self.index[0]
        del self.index[0]
        self.nc -= 1
        if self.nc == 0:
            self.setVisible(False)
            self.empty = True
        else:
            self.__stack()
            self.setPos(self.x1 - self.width, self.y1 - self.height)

        return card

    def set_pos_init(self, x0, y0):
        self.x1 = x0 + self.width
        self.y1 = y0 + self.height
        self.setPos(x0, y0)

    def __stack(self):
        r = rBound
        t = 1
        ow = 1
        oh = 1
        im = Image.open("resources/images/back.jpg")
        im.thumbnail((Card.width - 2 * t, Card.height - 2 * t))
        im = ImageTreatment.round_corners(im, int(r))
        cadre = Image.new('RGBA', (im.width + 2 * t, im.height + 2 * t), Style.cadre_color)
        cadre = ImageTreatment.round_corners(cadre, int(r + t))
        cadre.paste(im, (t, t), im)
        nc2 = int(self.nc / 2)
        trame = Image.new('RGBA', (cadre.width + nc2 * ow, cadre.height + nc2 * oh), (0, 0, 0, 0))
        relief1 = Image.new('RGBA', (cadre.width, cadre.height), Style.relief_color2)
        relief1 = ImageTreatment.round_corners(relief1, int(r + t))
        relief2 = Image.new('RGBA', (cadre.width, cadre.height), Style.relief_color)
        relief2 = ImageTreatment.round_corners(relief2, int(r + t))

        for i in range(nc2, 1, -2):
            trame.paste(relief1, (i * ow, i * oh), relief1)
            trame.paste(relief2, ((i - 1) * ow, (i - 1) * oh), relief2)

        trame.paste(cadre, (0, 0), cadre)
        image = ImageQt.ImageQt(trame)
        pixmap = QPixmap.fromImage(image)

        self.setPixmap(pixmap)
        self.width = pixmap.width()
        self.height = pixmap.height()
