#
# Définition de la fenêtre principale de l'interface avec ses menus
#
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QStatusBar

from src.GameView import GameView
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

        menu_bar = self.MenuBar()
        menu_bar.setNativeMenuBar(False)

        # Menubar : Add file menu and new game actions

        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(self.newGame_act)
        file_menu.addAction(self.exit_act)

        # Menubar : Add settings menu

        config_menu = menu_bar.addMenu('&Config')
        level = config_menu.addMenu("Level")
        level.addAction(self.level0)
        level.addAction(self.level1)
        config_menu.addAction(self.sound_act)
        config_menu.addAction(self.round_nb)

        # Menubar : Add help menu

        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(self.rules_act)
        help_menu.addAction(self.about_act)

        # Display info about actions in the status bar

        self.setStatusBar(QStatusBar(self))

        # Show the main window

        self.show()

    def new_game(self):
        self.game_view.close()
        self.game_view = GameView()
        self.setCentralWidget(self.game_view)

    # Hidden short-cut pressed handler

    def keyPressEvent(self, event):
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_A:
                self.game.show_automaton_hand_view()

    # Hidden short-cut release handler

    def keyReleaseEvent(self, event):
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_A:
                self.game.hide_automaton_hand_view()
