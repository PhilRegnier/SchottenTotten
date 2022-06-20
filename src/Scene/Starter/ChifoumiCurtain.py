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
from src.Scene.Curtain import Curtain
from src.SettingsManager import SettingsManager
from src.TextInForeground import TextInForeground
from src.ImageTreatment import ImageTreatment


class Chifoumi(Curtain):

    FIRST_TITLE = "Play Chifoumi to set who play first..."
    REPLAY_TITLE = "It's tie !! Play again..."
    PLAYER_WON = "YOU ARE FIRST PLAYER !!"
    BOT_WON = "AUTOMATON IS FIRST PLAYER !!"

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
        image = Image.open('resources/images/chifoumi/interrogation.jpg')
        image.thumbnail((cw, cw))
        self.guess = QPixmap.fromImage(ImageTreatment.enluminure(image))
        self.interro.setPixmap(self.guess)
        self.interro.setParentItem(self)

        self.pierre = Clickable('chifoumi/pierre.jpg', cw, cw, self)
        self.ciseaux = Clickable('chifoumi/ciseaux.jpg', cw, cw, self)
        self.feuille = Clickable('chifoumi/feuille.jpg', cw, cw, self)

        self.sep = QGraphicsLineItem()
        self.sep.setPen(QPen(QColor(68, 68, 68, 255), 2))
        self.sep.setParentItem(self)

        self.text0 = TextInForeground(Chifoumi.FIRST_TITLE, self)
        self.text1 = TextInForeground("Select your hand !", self)

        # continue geometry

        cw = self.feuille.width()
        ch = self.feuille.height()
        lw = 3 * (ew + cw)
        lh = 2 * ew

        # set the scene

        player_hand_y = wh / 2 + lh

        self.sep.setLine((ww - lw) / 2, wh / 2, (ww + lw) / 2, wh / 2)
        self.interro.setPos((ww - cw) / 2, wh / 2 - ch - lh)
        self.pierre.setPos((ww - 3 * cw) / 2 - ew, player_hand_y)
        self.ciseaux.setPos((ww - cw) / 2, player_hand_y)
        self.feuille.setPos((ww + cw) / 2 + ew, player_hand_y)

        self.text0.setPos((ww - self.text0.boundingRect().width()) / 2, lh)
        self.text1.setPos(
            (ww - self.text1.boundingRect().width()) / 2,
            (player_hand_y + cw + wh - self.text1.boundingRect().height()) / 2
        )

    def start(self):
        self.text1.setVisible(True)
        self.interro.setPixmap(self.guess)
        self.pierre.reset()
        self.ciseaux.reset()
        self.feuille.reset()

    """
        When the player has chosen his hand, this method
        compare it with a randomly chosen hand. 
    """
    def mouseReleaseEvent(self, event):

        super(Chifoumi, self).mouseReleaseEvent(event)

        if self.feuille.selected or self.ciseaux.selected or self.pierre.selected:

            self.text1.setVisible(False)

            # automaton's choice (0=feuille, 1=ciseaux, 2=pierre)

            autoc = randint(0, 2)
            tie = False

            if autoc == 0:
                self.interro.setPixmap(self.feuille.pixmap())
                if self.feuille.selected:
                    tie = True
            elif autoc == 1:
                self.interro.setPixmap(self.ciseaux.pixmap())
                if self.ciseaux.selected:
                    tie = True
            else:
                self.interro.setPixmap(self.pierre.pixmap())
                if self.pierre.selected:
                    tie = True

            if tie:
                self.change_text(self.text0, Chifoumi.REPLAY_TITLE)
                QTimer.singleShot(3000, self.start)
                return

            # verdict if not equality

            if (self.feuille.selected and autoc == 2) \
                    or (self.ciseaux.selected and autoc == 0) \
                    or (self.pierre.selected == 2 and autoc == 1):
                self.settings.set_first_player(self.settings.CONST_PLAYER)
                self.change_text(self.text0, Chifoumi.PLAYER_WON)
            else:
                self.settings.set_first_player(self.settings.CONST_AUTOMATON)
                self.change_text(self.text0, Chifoumi.BOT_WON)

            self.pierre.setAcceptHoverEvents(False)
            self.ciseaux.setAcceptHoverEvents(False)
            self.feuille.setAcceptHoverEvents(False)
            QTimer.singleShot(3000, self.leave)

    def leave(self):
        self.animate_leaving()
        self.scene().start_new_round()


