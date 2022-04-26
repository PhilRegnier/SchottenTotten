#
# chifoumi to know who's beggining
#
from random import randint

from PIL import Image
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QPen, QColor
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsLineItem

from src.Scene.Game.Card import Card
from src.Scene.Clickable import Clickable
from src.Scene.Starter.Curtain import Curtain
from src.SettingsManager import SettingsManager
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

        # get the instance of SettingsManager

        self.settings = SettingsManager()

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
        self.pierre.reset()
        self.ciseaux.reset()
        self.feuille.reset()
        QTimer.singleShot(3000, self.restart_countdown)

    def restart_countdown(self):
        self.text2.setVisible(False)
        self.start()

    """
        When the player has chosen his hand, this method
        compare it with a randomly chosen hand. 
    """
    def mouseReleaseEvent(self, event):

        if (self.feuille.selected and not self.feuille.handled) \
                or (self.ciseaux.selected and not self.ciseaux.handled) \
                or (self.pierre.selected and not self.pierre.handled):

            self.text1.setVisible(False)
            self.text2.setVisible(False)

            # automaton's choice (0=feuille, 1=ciseaux, 2=pierre)

            autoc = randint(0, 2)

            if autoc == 0:
                self.interro.setPixmap(self.feuille.pixmap())
                if self.feuille.selected:
                    self.settings.set_first_player(None)
            elif autoc == 1:
                self.interro.setPixmap(self.ciseaux.pixmap())
                if self.ciseaux.selected:
                    self.settings.set_first_player(None)
            else:
                self.interro.setPixmap(self.pierre.pixmap())
                if self.pierre.selected:
                    self.settings.set_first_player(None)

            # verdict if not equality

            if (self.feuille.selected and autoc == 2) \
                    or (self.ciseaux.selected and autoc == 0) \
                    or (self.pierre.selected == 2 and autoc == 1):
                self.settings.set_first_player(self.settings.CONST_PLAYER)
            else:
                self.settings.set_first_player(self.settings.CONST_AUTOMATON)

            # terminate by setting the choice handled

            self.feuille.set_handled(True)
            self.ciseaux.set_handled(True)
            self.pierre.set_handled(True)

    def freeze(self):
        self.pierre.setAcceptHoverEvents(False)
        self.ciseaux.setAcceptHoverEvents(False)
        self.feuille.setAcceptHoverEvents(False)


