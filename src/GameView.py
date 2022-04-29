#
# Game definition
#
from math import sqrt

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import QGraphicsView

from src.Scene.GameScene import GameScene
from src.SettingsManager import SettingsManager
from src.Style import GlobalStyle


class GameView(QGraphicsView):

    def __init__(self, parent, width):
        super().__init__(parent)

        # initialize private variables

        self.current_round = 0
        self.items_selected = []
        self.ending = False

        # Preset the scene and the view

        self.settings_manager = SettingsManager()
        self.board = GameScene(self)

        # Set the view with QGraphicsView parent's methods

        self.parent = parent
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setBackgroundBrush(QBrush(GlobalStyle.background_color))
        self.setScene(self.board)

        # Prepare a timer

        self.timer = QTimer(self)

    def height(self):
        return self.board.height()
