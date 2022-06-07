from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox, QScrollArea, QWidget, QVBoxLayout, QLabel, QDialog, QPushButton

from src.Style import GeometryStyle
from src.variables_globales import __version__


class HelpMenuBar:

    def __init__(self, window):

        # Create actions for help menu

        self.rules_action = QAction(QIcon('resources/images/help.png'), 'Rules', window)
        self.rules_action.setShortcut('F1')
        self.rules_action.setStatusTip('See the rules of Schotten Totten')
        self.rules_action.triggered.connect(lambda: HelpMenuBar._show_rules(window))

        self.about_action = QAction(
            QIcon('resources/images/info.png'),
            'About Schotten Totten...',
            window
        )
        self.about_action.triggered.connect(lambda: HelpMenuBar._show_about(window))

    def get_rules_action(self):
        return self.rules_action

    def get_about_action(self):
        return self.about_action

    @staticmethod
    def _show_rules(window):

        with open('resources/html/rules.html', 'r') as file:
            msg = file.read()

        dialog = QDialog(window)

        dialog.setWindowTitle("Les règles du jeu")
        dialog.setMinimumSize(int(0.6*GeometryStyle.main_width), int(0.6*GeometryStyle.main_height))

        scroll = QScrollArea(dialog)

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)

        widget = QWidget(scroll)
        scroll.setWidget(widget)

        w_layout = QVBoxLayout()
        dialog.setLayout(w_layout)
        w_layout.addWidget(scroll)

        r_layout = QVBoxLayout(widget)
        widget.setLayout(r_layout)

        texte = QLabel(msg)
        texte.setWordWrap(True)
        button = QPushButton("Fermer")
        button.setToolTip("Ferme la fenêtre")
        button.clicked.connect(dialog.close)

        r_layout.addWidget(texte)
        w_layout.addWidget(button, alignment=Qt.AlignCenter)

        dialog.exec_()

    @staticmethod
    def _show_about(window):

        with open('resources/html/about.html', 'r') as file:
            msg = file.read()

        QMessageBox.about(
            window,
            "About Schotten Totten",
            msg % __version__
        )

