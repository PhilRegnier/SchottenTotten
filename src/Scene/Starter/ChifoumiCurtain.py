#
# chifoumi to know who's beggining
#
from random import randint

from PIL import Image
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QPen, QColor
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsLineItem

from src.Scene.Game.Card import Card
from src.Scene.Clickable import Clickable
from src.Scene.Starter.Curtain import Curtain
from src.TextInForeground import TextInForeground
from src.ImageTreatment import ImageTreatment
from src.variables_globales import selected


class Chifoumi(Curtain):

    def __init__(self, parent=None):
        super().__init__(parent)

        # prepare geometry

        ww = self.boundingRect().width()
        wh = self.boundingRect().height()
        cw = Card.height
        ew = 20

        # set the items

        self.interro = QGraphicsPixmapItem()
        image = Image.open('resources/images/interrogation.jpg')
        image.thumbnail((cw, cw))
        self.guess = QPixmap.fromImage(ImageTreatment.enluminure(image))
        self.interro.setPixmap(self.guess)
        self.interro.setParentItem(self)

        self.pierre = Clickable('pierre.jpg', cw, cw, 2, self)
        self.ciseaux = Clickable('ciseaux.jpg', cw, cw, 1, self)
        self.feuille = Clickable('feuille.jpg', cw, cw, 0, self)

        self.sep = QGraphicsLineItem()
        self.sep.setPen(QPen(QColor(68, 68, 68, 255), 2))
        self.sep.setParentItem(self)

        self.text1 = TextInForeground("Choose your hand !", self)
        self.text1.setVisible(False)
        self.text2 = TextInForeground("Tie !!\n\n", self)
        self.text2.setVisible(False)

        # continue geometry

        cw = self.feuille.width()
        ch = self.feuille.height()
        lw = 3 * (ew + cw)
        lh = 2 * ew

        # set the scene

        self.sep.setLine((ww - lw) / 2, wh / 2, (ww + lw) / 2, wh / 2)
        self.interro.setPos((ww - cw) / 2, wh / 2 - ch - lh)
        self.pierre.setPos((ww - 3 * cw) / 2 - ew, wh / 2 + lh)
        self.ciseaux.setPos((ww - cw) / 2, wh / 2 + lh)
        self.feuille.setPos((ww + cw) / 2 + ew, wh / 2 + lh)

    def start(self):
        self.text1.setVisible(True)

    def restart(self):
        self.text2.setVisible(True)
        self.interro.setPixmap(self.guess)
        QTimer.singleShot(3000, self.restart_countdown)

    def restart_countdown(self):
        self.text2.setVisible(False)
        self.start()

    def choose_player(self):

        # User's choice

        self.text1.setVisible(False)
        self.text2.setVisible(False)

        autoc = randint(0, 2)

        # showing auto's choice

        if autoc == 0:
            self.interro.setPixmap(self.feuille.pixmap())
        elif autoc == 1:
            self.interro.setPixmap(self.ciseaux.pixmap())
        else:
            self.interro.setPixmap(self.pierre.pixmap())

        # verdict

        if selected == autoc:
            return -1
        elif (selected == 0 and autoc == 2) \
                or (selected == 1 and autoc == 0) \
                or (selected == 2 and autoc == 1):
            return 0
        else:
            return 1

    def freeze(self):
        self.pierre.setAcceptHoverEvents(False)
        self.ciseaux.setAcceptHoverEvents(False)
        self.feuille.setAcceptHoverEvents(False)
