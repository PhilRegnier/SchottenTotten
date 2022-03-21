#
# Stone definition
#
from PIL import Image
from PyQt5.QtCore import QRectF, QRect, QPropertyAnimation, QPointF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsObject

from src.image_treatment import enluminure
from src.variables_globales import userType, stone_width, stone_height


class Stone(QGraphicsObject):
    Type = userType + 1

    def __init__(self, numero, parent=None):
        super().__init__(parent)
        self.numero = numero
        image = Image.open('../resources/images/borne' + str(self.numero + 1) + '.jpg')
        image.thumbnail((stone_width - 1, stone_height - 1))
        self.pixmap = QPixmap.fromImage(enluminure(image, ow=2, oh=2))
        self.winner = ""

    def boundingRect(self):
        pen_width = 1.0
        return QRectF(-pen_width / 2, -pen_width / 2, stone_width + pen_width, stone_height + pen_width)

    def paint(self, painter, option, widget):
        rect = QRect(-1, -1, int(stone_width), int(stone_height))
        painter.drawPixmap(rect, self.pixmap)

    # Animation for claimed stones

    def moveStoneTo(self, dy):
        self.moveStone = QPropertyAnimation(self, b"pos")
        self.moveStone.setDuration(800)
        self.moveStone.setStartValue(self.pos())
        self.moveStone.setEndValue(QPointF(self.x(), self.y() + dy))
        self.moveStone.start()
