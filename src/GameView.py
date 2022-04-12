#
# Game definition
#
from math import sqrt

from PyQt5.QtCore import QPropertyAnimation, QLineF, QTimer, QParallelAnimationGroup
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import QGraphicsView

from src.Scene.Game import UserSide
from src.Scene.GameScene import GameScene
from src.Scene.Game.Card import Card
from src.Scene.Starter.ChifoumiCurtain import Chifoumi
from src.Scene.Starter.Curtain import Curtain
from src.SettingsManager import SettingsManager
from src.Style import Style
from src.TextInForeground import TextInForeground
from src.variables_globales import stone_height, cote_both, cote_brelan, cote_couleur, cote_suite


class GameView(QGraphicsView):

    def __init__(self, parent):
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
        self.setBackgroundBrush(QBrush(Style.background_color))
        self.setScene(self.board)

        # Prepare a timer

        self.timer = QTimer(self)
