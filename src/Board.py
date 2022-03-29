from PyQt5.QtWidgets import QGraphicsScene

from src.variables_globales import mainWindow_width, mainWindow_height


class Board(QGraphicsScene):

    def __init__(self, parent):
        super().__init__(parent)

        self.setSceneRect(0, 0, mainWindow_width - 40, mainWindow_height - 60)