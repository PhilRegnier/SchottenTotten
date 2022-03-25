#
# Card definition
#
import sys
from math import sqrt

from PIL import Image
from PyQt5.QtCore import QPointF, QLineF, QPropertyAnimation, QRectF, QRect, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsObject, QGraphicsItem, QApplication

from src import UserSide, AutoSide
from src.ImageTreatment import ImageTreatment
from src.MovingCard import MovingCard
from src.Ombrage import Ombrage
from src.variables_globales import max_value, colors, side_height, stone_width


class Card(QGraphicsObject):

    cards = []
    total_cards = len(colors) * max_value
    width = stone_width - 4
    height = width * 1.42

    def __init__(self, numero, parent=None):
        if numero < 0 or numero > Card.total_cards - 1:
            print("Card number must be into [0, 53]. Program stopped")
            sys.exit(0)

        super().__init__(parent)
        self.parent = parent
        self.numero = numero
        self.index = -1
        self.anchorPoint = QPointF()
        self.valeur = numero % max_value + 1
        self.couleur = colors[numero // max_value]

        image = Image.open('resources/images/' + self.couleur + str(self.valeur) + '.jpg')
        image.thumbnail((Card.width - 2, Card.height - 2))
        self.pixmap = QPixmap.fromImage(ImageTreatment.enluminure(image))

        self.setAcceptHoverEvents(False)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self.ombrage = Ombrage()
        self.setGraphicsEffect(self.ombrage)

    def setDraggable(self, draggable=True):
        if draggable:
            self.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.setAcceptHoverEvents(True)
        else:
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.setAcceptHoverEvents(False)

    def setAnchorPoint(self, anchorPoint):
        self.anchorPoint = anchorPoint

    def setIndex(self, index):
        self.index = index

    def hoverEnterEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)
        self.setPos(self.x() - 2, self.y() - 2)
        self.ombrage.setEnabled(True)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.setPos(self.anchorPoint)
        self.ombrage.setEnabled(False)

    def mousePressEvent(self, event):
        if not event.button() == Qt.LeftButton:
            return
        if self.parentItem().Type == UserSide.Type or self.parentItem().Type == AutoSide.Type:
            return

        self.dragStartPosition = event.pos()
        self.setCursor(Qt.ClosedHandCursor)
        self.ombrage.setEnabled(True)

    def mouseMoveEvent(self, event):

        # Check button pressed, card's origin, and that a minimum move has been done

        if not (event.buttons() == Qt.LeftButton):
            return
        if self.parentItem().Type == UserSide.Type or self.parentItem().Type == AutoSide.Type:
            return
        if (event.pos() - self.dragStartPosition).manhattanLength() < QApplication.startDragDistance():
            return

        # All staff when a card is dragged from the user's hand

        MovingCard.dragged()
        card_nb = self.numero
        QGraphicsObject.mouseMoveEvent(self, event)
        self.ombrage.setEnabled(True)
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

    def setCardOnSide(self, item):
        if item.Type == UserSide.Type:
            if item.nCard < 3:
                MovingCard.set_side_id(item.numero)
                self.setDraggable(False)

                # get sure that the card dropped is in the foreground

                if item.nCard > 0:
                    self.setZValue(Card.cards[item.index[len(item.index) - 1]].zValue() + 0.1)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        if MovingCard.dragged():
            col_items = self.collidingItems()
            if col_items:
                closest_item = col_items[0]
                shortest_dist = 100000.

                for item in col_items:
                    line = QLineF(item.sceneBoundingRect().center(),
                                  self.sceneBoundingRect().center())
                    if line.length() < shortest_dist:
                        shortest_dist = line.length()
                        closest_item = item

                if closest_item.parentItem():
                    self.setCardOnSide(closest_item.parentItem())
                else:
                    self.setCardOnSide(closest_item)

            QGraphicsObject.mouseReleaseEvent(self, event)
            self.ombrage.setEnabled(False)
            self.setOpacity(1)

    def moveTo(self, pos1, pos2):

        # animation for the move

        self.moveCard = QPropertyAnimation(self, b"pos")
        dx = pos1.x() - pos2.x()
        dy = pos1.y() - pos2.y()
        duration = int(sqrt(dx ** 2 + dy ** 2) / 1)
        self.moveCard.setDuration(duration)
        self.moveCard.setStartValue(pos1)
        self.moveCard.setEndValue(pos2)

        self.setOnTop()
        self.moveCard.finished.connect(self.setOnGround)

        self.moveCard.start()

    def setOnTop(self):
        self.z_old = self.zValue()
        self.setZValue(1000)

    def setOnGround(self):
        self.setZValue(self.z_old)

    def boundingRect(self):
        pen_width = 1.0
        return QRectF(-pen_width / 2, -pen_width / 2, Card.width + pen_width, side_height + pen_width)

    def paint(self, painter, option, widget):
        rect = QRect(-1, -1, int(Card.width), int(Card.height))
        painter.drawPixmap(rect, self.pixmap)
