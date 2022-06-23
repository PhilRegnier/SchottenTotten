#
# Game definition
#

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QBrush
from PyQt6.QtWidgets import QGraphicsView

from src.Style import GlobalStyle


class GameView(QGraphicsView):

    # Init the view with QGraphicsView parent's methods
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(GlobalStyle.background_color))

    def height(self):
        return self.scene().height
