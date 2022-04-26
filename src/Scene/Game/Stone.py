#
# Stone definition
#
from PIL import Image
from PyQt5.QtCore import QRectF, QRect, QPropertyAnimation, QPointF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsObject

from src.ImageTreatment import ImageTreatment
from src.MainWindow.GameWindow import GameWindow
from src.Style import GeometryStyle


class Stone(QGraphicsObject):

    marge = 4.
    width = (GameWindow.width - 2 * GameWindow.marge - 8 * marge - 40) / 9 - 2 * GameWindow.pen_width
    height = width * 0.58

    def __init__(self, numero, parent=None):
        super().__init__(parent)
        self.numero = numero
        image = Image.open('resources/images/borne' + str(self.numero + 1) + '.jpg')
        image.thumbnail((Stone.width - 1, Stone.height - 1))
        self.pixmap = QPixmap.fromImage(ImageTreatment.enluminure(image, ow=2, oh=2))
        self.winner = None
        self.animation = QPropertyAnimation(self, b"pos")

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
