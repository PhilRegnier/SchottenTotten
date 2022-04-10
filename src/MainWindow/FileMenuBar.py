from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, qApp, QMessageBox


class FileMenuBar:

    def __init__(self, window):

        # Menubar : Create actions for file menu

        self.exit_act = QAction(QIcon('resources/images/exit.png'), '&Exit', self)
        self.exit_act.setShortcut('Ctrl+Q')
        self.exit_act.setStatusTip('Quit program')
        self.exit_act.triggered.connect(qApp.quit)

        self.newGame_act = QAction(QIcon('resources/images/logo.png'), 'New game', self)
        self.newGame_act.setShortcut('Ctrl+N')
        self.newGame_act.setStatusTip('Start a new game')
        self.newGame_act.triggered.connect(lambda: self.new_game(window))

    @staticmethod
    def new_game(self, window):

        # Ask before creating a new game

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Are you sure you want to quit the current game and create a new one ?")
        msg.setWindowTitle("Warning !")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)

        if msg.exec() == QMessageBox.Yes:
            window.new_game()
        else:
            pass
