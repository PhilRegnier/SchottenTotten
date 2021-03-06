# ------------------------------------------------------------------------------------------------------
# Deck definition
# ------------------------------------------------------------------------------------------------------

from PIL import ImageQt, Image
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsPixmapItem
from src.Scene.Game.Card import Card
from src.ImageTreatment import ImageTreatment
from src.Scene.Game.CardManager import CardManager
from src.Style import GlobalStyle, MainGeometry


class Deck(QGraphicsPixmapItem):

    def __init__(self):
        super().__init__()

        self.cardManager = CardManager()

        # geometry

        self.x1 = 0
        self.y1 = 0
        self.width = 0
        self.height = 0

        # ask a random deck to the manager and stack it

        self.cards = self.cardManager.get_deck(self)
        self._stack()

    def is_empty(self):
        return len(self.cards) == 0

    def draw(self):
        if self.is_empty != 0:
            drawn_card = self.cards[0]
            self.cards.remove(drawn_card)

            if self.is_empty == 0:
                self.setVisible(False)
            else:
                self._stack()
                self.setPos(self.x1 - self.width, self.y1 - self.height)

            return drawn_card
        else:
            return False

    def set_pos_init(self, x0, y0):
        self.x1 = x0 + self.width
        self.y1 = y0 + self.height
        self.setPos(x0, y0)

    def _stack(self):
        r = MainGeometry.r_bound
        t = 1
        ow = 1
        oh = 1

        image = Image.open("resources/images/cartes/back.jpg")
        image.thumbnail((Card.width - 2 * t, Card.height - 2 * t))
        image = ImageTreatment.round_corners(image, int(r))
        cadre = Image.new('RGBA', (image.width + 2 * t, image.height + 2 * t), GlobalStyle.cadre_color)
        cadre = ImageTreatment.round_corners(cadre, int(r + t))
        cadre.paste(image, (t, t), image)
        nc2 = int(len(self.cards) / 2)
        trame = Image.new('RGBA', (cadre.width + nc2 * ow, cadre.height + nc2 * oh), (0, 0, 0, 0))
        relief1 = Image.new('RGBA', (cadre.width, cadre.height), GlobalStyle.relief_color2)
        relief1 = ImageTreatment.round_corners(relief1, int(r + t))
        relief2 = Image.new('RGBA', (cadre.width, cadre.height), GlobalStyle.relief_color)
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
