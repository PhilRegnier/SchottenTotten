"""
 Lancement du jeu Schotten Totten

    TODO :
        - Mettre un timer sur le round
        - Implémenter les variantes de jeu avec les cartes "spéciales"

"""
import sys

from PyQt5.QtWidgets import QApplication

from src.MainWindow.GameWindow import GameWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    sys.exit(app.exec_())

