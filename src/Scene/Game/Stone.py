#
# Stone definition
#
from PIL import Image
from PyQt6.QtCore import QRectF, QRect, QPropertyAnimation, QPointF
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsObject

from src.ImageTreatment import ImageTreatment
from src.Style import MainGeometry


class Stone(QGraphicsObject):

    HW_RATIO = 0.58
    marge = 4.
    width = 0
    height = 0

    def __init__(self, numero, parent=None):
        super().__init__(parent)
        self.numero = numero
        if Stone.width == 0:
            Stone.set_size()

        image = Image.open('resources/images/bornes/' + str(self.numero + 1) + '.jpg')
        image.thumbnail((Stone.width - 1, Stone.height - 1))
        self.pixmap = QPixmap.fromImage(ImageTreatment.enluminure(image, ow=2, oh=2))
        self.winner = None
        self.first_to_play_the_third_card = None
        self.animation = QPropertyAnimation(self, b"pos")
        self.y0 = None

    # Memorize the player who put a third card first for this stone

    def put_a_third_card(self, player):
        if self.first_to_play_the_third_card is None:
            self.first_to_play_the_third_card = player

    # Claim the stone and move it on the winner's side

    def claim(self, player, automa):
        from src.Scene.Game.Side import Side

        if player.sides[self.numero].somme > automa.sides[self.numero].somme:
            self.winner = player
        elif player.sides[self.numero].somme < automa.sides[self.numero].somme:
            self.winner = automa
        else:
            self.winner = self.first_to_play_the_third_card

        delta_height = Side.height + 6 + Stone.height
        if self.winner == automa:
            delta_height = - delta_height

        self.y0 = self.y()

        self.move_to(delta_height)

    # position stone at the frontier zone

    def reset(self):
        if self.y0 is not None:
            self.move_to(self.y0 - self.y())

    # Animate the claimed stone

    def move_to(self, dy):
        self.animation.setDuration(800)
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(QPointF(self.x(), self.y() + dy))
        self.animation.start()

    # define the geometry of the stone

    def boundingRect(self):
        return QRectF(-MainGeometry.pen_width / 2,
                      -MainGeometry.pen_width / 2,
                      Stone.width + MainGeometry.pen_width,
                      Stone.height + MainGeometry.pen_width)

    def paint(self, painter, option, widget=0):
        rect = QRect(-1, -1, int(Stone.width), int(Stone.height))
        painter.drawPixmap(rect, self.pixmap)

    @classmethod
    def set_size(cls):
        cls.width = int(
            (MainGeometry.width - 250
                - 2 * MainGeometry.marge
                - 8 * cls.marge - 40)
            / 9 - 2 * MainGeometry.pen_width
        )
        cls.height = cls.width * cls.HW_RATIO
