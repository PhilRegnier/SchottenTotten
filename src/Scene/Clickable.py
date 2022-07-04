#
# Generic clickable button
#
from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem

from src.ImageTreatment import ImageTreatment
from src.Scene.effects.Shader import Shader
from src.Style import GlobalStyle


class Clickable(QGraphicsPixmapItem):

    instance_hover = None
    instance_clicked = None

    def __init__(self, file, width, height, parent_item, back=False):
        super().__init__(parent_item)

        image = Image.open('resources/images/' + file)
        if back:
            back_img = Image.new("RGB", (image.size[0], image.size[1]), (222, 222, 222))
            image = Image.composite(image, back_img, image)

        image.thumbnail((width, height))
        self.setPixmap(QPixmap.fromImage(ImageTreatment.enluminure(image)))
        self.setParentItem(parent_item)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.ombrage = Shader()
        self.setGraphicsEffect(self.ombrage)
        self.anchor_point = None
        self.clicked = False
        self.selected = False

    def reset(self):
        self.clicked = False
        self.selected = False

    def hoverEnterEvent(self, event):
        Clickable.instance_hover = self
        self.anchor_point = self.pos()
        self.setPos(self.x() - 2, self.y() - 2)
        self.ombrage.setEnabled(True)

    def hoverLeaveEvent(self, event):
        Clickable.instance_hover = None
        self.setPos(self.anchor_point)
        self.ombrage.setEnabled(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked = True
        else:
            QGraphicsPixmapItem.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self.clicked:
            self.ombrage.setColor(GlobalStyle.ombrage_color_bt)
            self.clicked = False
            self.selected = True
            self.parentItem().mouseReleaseEvent(event)

    def width(self):
        return self.boundingRect().width()

    def height(self):
        return self.boundingRect().height()

    def unselect(self):
        self.selected = False
