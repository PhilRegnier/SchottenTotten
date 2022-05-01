#
# Game definition
#
from math import sqrt

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import QGraphicsView

from src.Style import GlobalStyle


class GameView(QGraphicsView):

    def __init__(self, scene):
        super().__init__(scene)

        # initialize private variables

        self.current_round = 0
        self.items_selected = []
        self.ending = False

        # Set the view with QGraphicsView parent's methods

        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(GlobalStyle.background_color))

        # Prepare a timer

        self.timer = QTimer(self)

    def height(self):
        return self.scene().height
