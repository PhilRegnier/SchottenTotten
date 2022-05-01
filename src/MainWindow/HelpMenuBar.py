from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox
from src.variables_globales import __version__


class HelpMenuBar:

    def __init__(self, window):

        # Create actions for help menu

        self.rules_action = QAction(QIcon('resources/images/help.png'), 'Rules', window)
        self.rules_action.setShortcut('F1')
        self.rules_action.setStatusTip('See the rules of Schotten Totten')
        self.rules_action.triggered.connect(HelpMenuBar._show_rules)

        self.about_action = QAction(
            QIcon('resources/images/info.png'),
            'About Schotten Totten...',
            window
        )
        self.about_action.triggered.connect(lambda: HelpMenuBar._show_info(window))

    def get_rules_action(self):
        return self.rules_action

    def get_about_action(self):
        return self.about_action

    @staticmethod
    def _show_rules():
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
    def _show_info(window):
        QMessageBox.about(
            window,
            "About Schotten Totten",
            """<h2> Schotten Totten</h2> v %s
            <p>Free adaptation of the cards game developped by <strong>Reiner Knizia</strong>
            and <strong>Djib</strong>, but without any agreement of the authors and publisher (Sorry ;-))</p>
            <p>The purposes of this development were:</p>
            <ul>
            <li> To learn new things about <code>PyQt</code>
            and its specific <code>QGraphicsView</code> model.</li>
            <li> To rise in competence on Python and on the Obect Oriented Programmation
            applied to this language.</li>
            </ul>
            <p>Copyright &copy; 2016-2019 IELLO for the original cards game.</p>
            <p>Copyright &copy; 2020-2022 Philippe Régnier for this video game.</p>
            <br>""" % __version__
        )
