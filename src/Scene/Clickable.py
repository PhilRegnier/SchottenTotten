#
# Generic clickable button
#
from PIL import Image
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem

from src.ImageTreatment import ImageTreatment
from src.Scene.Game.Shader import Shader
from src.Style import GlobalStyle


class Clickable(QGraphicsPixmapItem):

    instance_hover = None
    instance_clicked = None

    def __init__(self, file, width, height, parent, back=False):
        super().__init__()

        image = Image.open('resources/images/' + file)
        if back:
            back_img = Image.new("RGB", (image.size[0], image.size[1]), (222, 222, 222))
            image = Image.composite(image, back_img, image)

        image.thumbnail((width, height))
        self.setPixmap(QPixmap.fromImage(ImageTreatment.enluminure(image)))
        self.setParentItem(parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

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
        print("clickable: hoverEnter")
        Clickable.instance_hover = self
        self.anchor_point = self.pos()
        self.setPos(self.x() - 2, self.y() - 2)
        self.ombrage.setEnabled(True)

    def hoverLeaveEvent(self, event):
        print("clickable: hoverLeave")
        Clickable.instance_hover = None
        self.setPos(self.anchor_point)
        self.ombrage.setEnabled(False)

    def mousePressEvent(self, event):
        print("clickable: mousePress")
        if event.button() == Qt.LeftButton:
            self.clicked = True

    def mouseReleaseEvent(self, event):
        print("clickable: mouseRelease")
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
