#
# Définition de la fenêtre principale de l'interface avec ses menus
#
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QStatusBar

from src.GameView import GameView
from src.MainWindow.MenuBar import MenuBar
from src.Scene.Game.Card import Card
from src.Scene.Game.Stone import Stone


class GameWindow(QMainWindow):

    width = 1200
    marge = 20
    pen_width = 1.

    def __init__(self):
        super().__init__()

        # Create a new Schotten Totten game

        self.game_view = GameView(self)

        # Create the main window

        self.setFixedSize(GameWindow.width, self.get_GameWindow_height())
        self.setWindowTitle('Schotten Totten')
        self.setWindowIcon(QIcon('resources/images/logo.png'))
        self.setCentralWidget(self.game_view)

        # Menubar : Instanciation

        menu_bar = MenuBar(self)
        menu_bar.add_menus()

        # Display info about actions in the status bar

        self.setStatusBar(QStatusBar(self))

        # Show the main window

        self.show()

    @classmethod
    def get_height(cls):
        return int(4 * Stone.height + 4.33 * Card.height
                   + cls.marge * 2 + 8 * cls.pen_width + 4 * Stone.marge + 40)

    def new_game(self):
        self.game_view.close()
        self.game_view = GameView(self)
        self.setCentralWidget(self.game_view)

    # Hidden short-cut pressed handler

    def keyPressEvent(self, event):
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_A:
                self.gameview.show_automaton_hand_view()

    # Hidden short-cut release handler

    def keyReleaseEvent(self, event):
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_A:
                self.game_view.hide_automaton_hand_view()
