#
# Generic clickable button
#
from PIL import Image
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

from src.ImageTreatment import ImageTreatment
from src.Scene.Game.Shader import Shader
from src.Style import GlobalStyle
from src.variables_globales import clicked


class Clickable(QGraphicsPixmapItem):

    def __init__(self, file, width, height, num, parent, back=False):
        super().__init__()

        image = Image.open('resources/images/' + file)
        if back:
            back_img = Image.new("RGB", (image.size[0], image.size[1]), (222, 222, 222))
            image = Image.composite(image, back_img, image)

        image.thumbnail((width, height))
        self.setPixmap(QPixmap.fromImage(ImageTreatment.enluminure(image)))
        self.setParentItem(parent)
        self.setAcceptHoverEvents(True)

        self.ombrage = Shader()
        self.setGraphicsEffect(self.ombrage)
        self.anchor_point = None
        self.clicked = False
        self.selected = False
        self.handled = False

    def reset(self):
        self.anchor_point = None
        self.clicked = False
        self.selected = False
        self.handled = False

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
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked = True

    def mouseReleaseEvent(self, event):
        if self.clicked:
            self.ombrage.setColor(GlobalStyle.ombrage_color_bt)
            self.clicked = False
            self.selected = True

    def width(self):
        return self.boundingRect().width()

    def height(self):
        return self.boundingRect().height()

    def set_handled(self, flag):
        self.handled = flag

    def unselect(self):
        self.selected = False
