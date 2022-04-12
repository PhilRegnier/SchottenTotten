#
# Stone definition
#
from PIL import Image
from PyQt5.QtCore import QRectF, QRect, QPropertyAnimation, QPointF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsObject

from src.ImageTreatment import ImageTreatment
from src.MainWindow.GameWindow import GameWindow
from src.variables_globales import userType, stone_width, stone_height


class Stone(QGraphicsObject):
    Type = userType + 1

    marge = 4.
    width = (GameWindow.width - 2 * GameWindow.marge - 8 * marge - 40) / 9 - 2 * GameWindow.pen_width
    height = width * 0.58

    def __init__(self, numero, parent=None):
        super().__init__(parent)
        self.numero = numero
        image = Image.open('resources/images/borne' + str(self.numero + 1) + '.jpg')
        image.thumbnail((stone_width - 1, stone_height - 1))
        self.pixmap = QPixmap.fromImage(ImageTreatment.enluminure(image, ow=2, oh=2))
        self.winner = None
        self.animation = QPropertyAnimation(self, b"pos")

    def boundingRect(self):
        pen_width = 1.0
        return QRectF(-pen_width / 2, -pen_width / 2, stone_width + pen_width, stone_height + pen_width)

    def paint(self, painter, option, widget):
        rect = QRect(-1, -1, int(stone_width), int(stone_height))
        painter.drawPixmap(rect, self.pixmap)

    # Animation for claimed stones

    def move_to(self, dy):
        self.animation.setDuration(800)
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(QPointF(self.x(), self.y() + dy))
        self.animation.start()
