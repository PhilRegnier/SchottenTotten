from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMessageBox, QApplication


class FileMenuBar:

    def __init__(self, window):

        # Create actions for file menu

        self.exit_action = QAction(QIcon('resources/images/exit.png'), '&Exit', window)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip('Quit program')
        self.exit_action.triggered.connect(QApplication.instance().quit)

        self.newGame_action = QAction(QIcon('resources/images/logo.png'), 'New game', window)
        self.newGame_action.setShortcut('Ctrl+N')
        self.newGame_action.setStatusTip('Start a new game')
        self.newGame_action.triggered.connect(lambda: FileMenuBar.new_game(window))

    def get_new_game_action(self):
        return self.newGame_action

    def get_exit_action(self):
        return self.exit_action

    @staticmethod
    def new_game(window):

        # Ask before creating a new game

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("Are you sure you want to quit the current game and create a new one ?")
        msg.setWindowTitle("Warning !")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            window.new_game()
        else:
            pass
