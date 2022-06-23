#
# Définition de la fenêtre principale de l'interface avec ses menus
#
from PyQt6.QtCore import Qt

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QStatusBar

from src.GameView import GameView
from src.MainWindow.MenuBar import MenuBar
from src.Scene.GameScene import GameScene
from src.Style import GeometryStyle


class GameWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Create a new Schotten Totten game (scene & view)

        self.board = GameScene()
        self.game_view = GameView(self.board)

        # Create the main window

        self.set_height()
        self.setFixedSize(GeometryStyle.main_width, GeometryStyle.main_height)
        self.setWindowTitle('Schotten Totten')
        self.setWindowIcon(QIcon('resources/images/logo.png'))
        self.setCentralWidget(self.game_view)

        # Menubar : Instanciation

        menu_bar = MenuBar(self)
        menu_bar.add_menus()
        self.setMenuBar(menu_bar)

        # Display info about actions in the status bar

        self.setStatusBar(QStatusBar(self))

        # Show the main window

        self.show()

    def set_height(self):
        GeometryStyle.main_height = self.game_view.height() + 60

    def new_game(self):
        self.game_view.close()
        self.game_view = GameView(self)
        self.setCentralWidget(self.game_view)

    # Hidden short-cuts pressed handler

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_A:
                self.board.show_automaton_playmat()

            if event.key() == Qt.Key.Key_G:
                self.board.start_new_round()

    # Hidden short-cut release handler

    def keyReleaseEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_A:
                self.board.hide_automaton_playmat()
