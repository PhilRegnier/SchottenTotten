"""
 Lancement du jeu Schotten Totten

    TODO :
        - Mettre un timer sur le round
        - Afficher le score
        - compter les points par round en suivant les règles du jeu
        - Implémenter la variante de jeu avec les cartes "spéciales"
        - ScrollingBar pour la fenêtre des règles du jeu


"""
import sys

from PyQt5.QtWidgets import QApplication

from src.MainWindow.GameWindow import GameWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    sys.exit(app.exec_())

