from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox
from src.variables_globales import __version__


class HelpMenuBar:

    def __init__(self, window):

        # Create actions for help menu

        self.rules_act = QAction(QIcon('resources/images/help.png'), 'Rules', self)
        self.rules_act.setShortcut('F1')
        self.rules_act.setStatusTip('See the rules of Schotten Totten')
        self.rules_act.triggered.connect(self.show_rules)

        self.about_act = QAction(
            QIcon('resources/images/info.png'),
            'About Schotten Totten...',
            self
        )
        self.about_act.triggered.connect(lambda: self.show_info(window))

    @staticmethod
    def show_rules(self):
        msg = "Les cartes Clan représentent les membres de votre tribu " \
              "écossaise que vous envoyez sur le terrain pour défendre les " \
              "Bornes. Chaque carte Clan existe en six couleurs différentes " \
              "et possède une force allant de 1 à 9 (1 étant la force la " \
              "plus faible)."

        help_box = QMessageBox()
        help_box.setIcon(QMessageBox.Question)
        help_box.setWindowTitle("Les règles du jeu")
        help_box.setText(msg)
        help_box.setStandardButtons(QMessageBox.Ok)
        help_box.exec_()

    @staticmethod
    def show_info(self, window):
        QMessageBox.about(window, "About Schotten Totten",
                          """<b> Schotten Totten</b> v %s
                          <p>Adaptation of the cards game developped
                          by Reiner Knizia et Djib
                          <p>Copyright &copy; 2016-2019 IELLO for the 
                          original cards game.
                          <p>Copyright &copy; 2020 Philippe Régnier for
                          this video game.""" % __version__)
