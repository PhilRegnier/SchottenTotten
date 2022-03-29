#
# Generic clickable button
#
from PIL import Image
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

from src.ImageTreatment import ImageTreatment
from src.Shader import Shader
from src.Style import Style
from src.variables_globales import clicked, selected


class Clickable(QGraphicsPixmapItem):

    def __init__(self, file, width, height, num, parent_item=None, back=False):
        super().__init__()

        image = Image.open('resources/images/' + file)
        if back:
            back_img = Image.new("RGB", (image.size[0], image.size[1]), (222, 222, 222))
            image = Image.composite(image, back_img, image)

        image.thumbnail((width, height))
        self.setPixmap(QPixmap.fromImage(ImageTreatment.enluminure(image)))
        self.id = num
        self.setParentItem(parent_item)
        self.setAcceptHoverEvents(True)

        self.ombrage = Shader()
        self.setGraphicsEffect(self.ombrage)
        self.anchor_point = None

    def hoverEnterEvent(self, event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.anchor_point = self.pos()
        self.setPos(self.x() - 2, self.y() - 2)
        self.ombrage.setEnabled(True)

    def hoverLeaveEvent(self, event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.setPos(self.anchor_point)
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
            self.ombrage.setColor(Style.ombrage_color_bt)

    def width(self):
        return self.boundingRect().width()

    def height(self):
        return self.boundingRect().height()
