#
# Generic clickable button
#
from PIL import Image
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

from src.Ombrage import Ombrage
from src.image_treatment import enluminure
from src.variables_globales import ombrage_color_bt, clicked, selected


class Clickable(QGraphicsPixmapItem):

    def __init__(self, file, width, height, num, parent_item=None, back=False):
        super().__init__()

        image = Image.open('resources/images/' + file)
        if back:
            back_img = Image.new("RGB", (image.size[0], image.size[1]), (222, 222, 222))
            image = Image.composite(image, back_img, image)

        image.thumbnail((width, height))
        self.setPixmap(QPixmap.fromImage(enluminure(image)))
        self.id = num
        self.setParentItem(parent_item)
        self.setAcceptHoverEvents(True)

        self.ombrage = Ombrage()
        self.setGraphicsEffect(self.ombrage)

    def hoverEnterEvent(self, event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.anchorPoint = self.pos()
        self.setPos(self.x() - 2, self.y() - 2)
        self.ombrage.setEnabled(True)

    def hoverLeaveEvent(self, event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.setPos(self.anchorPoint)
        self.ombrage.setEnabled(False)

    def mousePressEvent(self, event):
        global clicked
        if not event.button() == QtCore.Qt.LeftButton:
            return

        clicked = True

    def mouseReleaseEvent(self, event):
        global selected
        if clicked:
            selected = self.id
            self.ombrage.setColor(ombrage_color_bt)

    def width(self):
        return self.boundingRect().width()

    def height(self):
        return self.boundingRect().height()
