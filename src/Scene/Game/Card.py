#
# Card definition
#
from math import sqrt

from PIL import Image
from PyQt5.QtCore import QPointF, QLineF, QPropertyAnimation, QRectF, QRect, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsObject, QGraphicsItem, QApplication

from src.ImageTreatment import ImageTreatment
from src.Scene.Game.Shader import Shader
from src.Scene.Game.ShiftManager import ShiftManager
from src.Scene.Game.Side import Side
from src.Scene.Game.Stone import Stone


class Card(QGraphicsObject):

    HW_RATIO = 1.42
    width = 0
    height = 0

    def __init__(self, numero, valeur, couleur):
        super().__init__()
        self.numero = numero
        self.valeur = valeur
        self.couleur = couleur
        self.anchor_point = QPointF()
        self.index = -1

        if Card.width == 0:
            Card.set_size()

        image = Image.open('resources/images/cartes/' + couleur + '/' + str(valeur) + '.jpg')
        image.thumbnail((Card.width - 2, Card.height - 2))
        self.pixmap = QPixmap.fromImage(ImageTreatment.enluminure(image))

        self.setAcceptHoverEvents(False)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self.shade = Shader()
        self.setGraphicsEffect(self.shade)

        self.shift_manager = ShiftManager()

        self.animation = None
        self.__old_z_value = None

    @classmethod
    def set_size(cls):
        if Stone.width == 0:
            print("ERREUR : Stones must be instanciated before cards for sizing purpose.")
        else:
            cls.width = Stone.width - 4
            cls.height = cls.width * cls.HW_RATIO

    def set_draggable(self, draggable=True):
        self.setFlag(QGraphicsItem.ItemIsMovable, draggable)
        self.setAcceptHoverEvents(draggable)

    def set_anchor_point(self, anchor_point):
        self.anchor_point = anchor_point

    def set_index(self, index):
        self.index = index

    def hoverEnterEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)
        self.setPos(self.x() - 2, self.y() - 2)
        self.shade.setEnabled(True)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.setPos(self.anchor_point)
        self.shade.setEnabled(False)

    def mousePressEvent(self, event):
        if not event.button() == Qt.LeftButton:
            return
        if isinstance(self.parentItem(), Side):
            return

        self.shift_manager.set_starting_pos(event.pos())
        self.setCursor(Qt.ClosedHandCursor)
        self.shade.setEnabled(True)

    def mouseMoveEvent(self, event):

        # Check button pressed, card's origin, and if a minimum move has been done

        if not (event.buttons() == Qt.LeftButton):
            return
        if isinstance(self.parentItem(), Side):
            return
        if (event.pos() - self.shift_manager.starting_pos).manhattanLength() < QApplication.startDragDistance():
            return

        # All staff when a card is dragged from the user's playmat

        if self.shift_manager.card is not self:
            self.shift_manager.set_dragged(True)
            self.shift_manager.set_card(self)
            self.shade.setEnabled(True)
            self.setOpacity(0.9)
            self.setCursor(Qt.ClosedHandCursor)

        # get sure the card dragged is in the foreground

        zvalue = 0.
        col_items = self.collidingItems()
        if col_items:
            for item in col_items:
                if item.zValue() >= zvalue:
                    zvalue = item.zValue() + 0.1

        self.setZValue(zvalue)

        QGraphicsObject.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):

        self.setCursor(Qt.ArrowCursor)
        if self.shift_manager.card is self:

            items = self.collidingItems()

            if items:
                closest_item = None
                shortest_dist = 100000.

                for item in items:
                    if item in self.scene().player.sides:
                        line = QLineF(item.sceneBoundingRect().center(),
                                      self.sceneBoundingRect().center())
                        if line.length() < shortest_dist:
                            shortest_dist = line.length()
                            closest_item = item

                if closest_item is not None and not closest_item.is_full():
                    self.shift_manager.set_side(closest_item)
                    self.set_draggable(False)
                    if not closest_item.is_empty():
                        self.setZValue(closest_item.cards[-1].zValue() + 0.1)

            QGraphicsObject.mouseReleaseEvent(self, event)
            self.shade.setEnabled(False)
            self.setOpacity(1)

    def move_to(self, starting_pos, ending_pos):

        # animation for the move
        # TODO : déclarer l'animation dans le constructeur ou bien faire appel à une méthode/class extérieure ??
        self.animation = QPropertyAnimation(self, b"pos")
        dx = starting_pos.x() - ending_pos.x()
        dy = starting_pos.y() - ending_pos.y()
        duration = int(sqrt(dx ** 2 + dy ** 2) / 1)
        self.animation.setDuration(duration)
        self.animation.setStartValue(starting_pos)
        self.animation.setEndValue(ending_pos)

        self.set_on_top()
        self.animation.finished.connect(self.set_on_ground)

        self.animation.start()

    def set_on_top(self):
        self.__old_z_value = self.zValue()
        self.setZValue(1000)

    def set_on_ground(self):
        self.setZValue(self.__old_z_value)

    def boundingRect(self):
        pen_width = 1.0
        return QRectF(-pen_width / 2, -pen_width / 2, Card.width + pen_width, Side.height + pen_width)

    def paint(self, painter, option, widget=0):
        rect = QRect(-1, -1, int(Card.width), int(Card.height))
        painter.drawPixmap(rect, self.pixmap)
