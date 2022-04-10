#
# Définition de la fenêtre principale de l'interface avec ses menus
#
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QStatusBar

from src.GameView import GameView
from src.MainWindow.MenuBar import MenuBar
from src.variables_globales import mainWindow_width, mainWindow_height


class GameWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setFixedSize(mainWindow_width, mainWindow_height)
        self.setWindowTitle('Schotten Totten')
        self.setWindowIcon(QIcon('resources/images/logo.png'))

        # Create a new Schotten Totten game

        self.game_view = GameView(self)
        self.setCentralWidget(self.game_view)

        # Menubar : Instanciation

        menu_bar = MenuBar(self)
        menu_bar.add_menus()

        # Display info about actions in the status bar

        self.setStatusBar(QStatusBar(self))

        # Show the main window

        self.show()

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
