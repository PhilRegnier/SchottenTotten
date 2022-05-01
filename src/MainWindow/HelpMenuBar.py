from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox
from src.variables_globales import __version__


class HelpMenuBar:

    def __init__(self, window):

        # Create actions for help menu

        self.rules_action = QAction(QIcon('resources/images/help.png'), 'Rules', window)
        self.rules_action.setShortcut('F1')
        self.rules_action.setStatusTip('See the rules of Schotten Totten')
        self.rules_action.triggered.connect(self._show_rules)

        self.about_action = QAction(
            QIcon('resources/images/info.png'),
            'About Schotten Totten...',
            window
        )
        self.about_action.triggered.connect(lambda: self._show_info(window))

    def get_rules_action(self):
        return self.rules_action

    def get_about_action(self):
        return self.about_action

    @staticmethod
    def _show_rules(self):
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
    def _show_info(self, window):
        QMessageBox.about(window, "About Schotten Totten",
                          """<b> Schotten Totten</b> v %s
                          <p>Adaptation of the cards game developped
                          by Reiner Knizia et Djib
                          <p>Copyright &copy; 2016-2019 IELLO for the 
                          original cards game.
                          <p>Copyright &copy; 2020 Philippe Régnier for
                          this video game.""" % __version__)
