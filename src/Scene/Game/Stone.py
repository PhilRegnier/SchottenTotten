#
# Stone definition
#
from PIL import Image
from PyQt5.QtCore import QRectF, QRect, QPropertyAnimation, QPointF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsObject

from src.ImageTreatment import ImageTreatment
from src.Style import GeometryStyle


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
        self.animation = QPropertyAnimation(self, b"pos")

    def claim(self, player_somme, automaton_somme):
        from src.Scene.Game.Side import Side

        if player_somme > automaton_somme:
            self.winner = "user"
            self.moveStoneTo(Side.height + 6 + Stone.height)
        elif player_somme < automaton_somme:
            self.winner = "auto"
            self.moveStoneTo(- Side.height - 6 - Stone.height)
        else:
            self.winner = "equal"

    def boundingRect(self):
        return QRectF(-GeometryStyle.pen_width / 2,
                      -GeometryStyle.pen_width / 2,
                      Stone.width + GeometryStyle.pen_width,
                      Stone.height + GeometryStyle.pen_width)

    def paint(self, painter, option, widget=0):
        rect = QRect(-1, -1, int(Stone.width), int(Stone.height))
        painter.drawPixmap(rect, self.pixmap)

    # Animation for claimed stones

    def move_to(self, dy):
        self.animation.setDuration(800)
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(QPointF(self.x(), self.y() + dy))
        self.animation.start()

    @classmethod
    def set_size(cls):
        cls.width = int(
            (GeometryStyle.main_width
             - 2 * GeometryStyle.main_marge
             - 8 * cls.marge - 40)
            / 9 - 2 * GeometryStyle.pen_width
        )
        cls.height = cls.width * cls.HW_RATIO
