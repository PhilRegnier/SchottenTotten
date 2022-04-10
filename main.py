#
# Lancement du jeu Schotten Totten
#
import sys

from PyQt5.QtWidgets import QApplication

from src.MainWindow.GameWindow import GameWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    sys.exit(app.exec_())

