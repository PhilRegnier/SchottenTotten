# ------------------------------------------------------------------------------------------------------
# Deck definition
# ------------------------------------------------------------------------------------------------------
from random import shuffle

from PIL import ImageQt, Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

from src.image_treatment import round_corners
from src.variables_globales import userType, N_cards, card, rBound, card_width, card_height, cadre_color, relief_color2, \
    relief_color


class Deck(QGraphicsPixmapItem):
    Type = userType + 2
    Nc = N_cards

    def __init__(self, parent=None):
        super().__init__(parent)

        self.x1 = 0
        self.y1 = 0

        self.empilement()
        self.empty = False

        # Create a random deck

        liste_cartes = [i for i in range(N_cards)]
        shuffle(liste_cartes)

        self.index = liste_cartes

        for i in range(N_cards):
            card[i].setParentItem(self)
            card[i].setPos(0, 0)
            card[i].setVisible(False)

    def isEmpty(self):
        return self.empty

    def draw(self):
        card = self.index[0]
        del self.index[0]
        self.Nc -= 1
        if self.Nc == 0:
            self.setVisible(False)
            self.empty = True
        else:
            self.empilement()
            self.setPos(self.x1 - self.wi, self.y1 - self.he)

        return card

    def setPosInit(self, x0, y0):
        self.x1 = x0 + self.wi
        self.y1 = y0 + self.he
        self.setPos(x0, y0)

    def empilement(self):
        r = rBound
        t = 1
        ow = 1
        oh = 1
        im = Image.open("images/back.jpg")
        im.thumbnail((card_width - 2 * t, card_height - 2 * t))
        im = round_corners(im, int(r))
        cadre = Image.new('RGBA', (im.width + 2 * t, im.height + 2 * t), cadre_color)
        cadre = round_corners(cadre, int(r + t))
        cadre.paste(im, (t, t), im)
        nc2 = int(self.Nc / 2)
        trame = Image.new('RGBA', (cadre.width + nc2 * ow, cadre.height + nc2 * oh), (0, 0, 0, 0))
        relief1 = Image.new('RGBA', (cadre.width, cadre.height), relief_color2)
        relief1 = round_corners(relief1, int(r + t))
        relief2 = Image.new('RGBA', (cadre.width, cadre.height), relief_color)
        relief2 = round_corners(relief2, int(r + t))

        for i in range(nc2, 1, -2):
            trame.paste(relief1, (i * ow, i * oh), relief1)
            trame.paste(relief2, ((i - 1) * ow, (i - 1) * oh), relief2)

        trame.paste(cadre, (0, 0), cadre)
        image = ImageQt.ImageQt(trame)
        pixmap = QPixmap.fromImage(image)
        self.setPixmap(pixmap)
        self.wi = pixmap.width()
        self.he = pixmap.height()
