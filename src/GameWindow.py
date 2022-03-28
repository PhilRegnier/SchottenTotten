#
# Définition de la fenêtre principale de l'interface
#
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QWidget, QLabel, QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout, \
    QMessageBox, QAction

from src.Card import Card
from src.Game import Game
from src.variables_globales import mainWindow_width, mainWindow_height, N_cards, __version__, card, difficulT, N_rounds


class GameWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(mainWindow_width, mainWindow_height)
        self.setWindowTitle('Schotten Totten')
        self.setWindowIcon(QIcon('resources/images/logo.png'))

        # Setting all the playing cards

        for i in range(N_cards):
            Card.cards.append(Card(i))

        self.create_game()
        self.create_menu()
        self.show()

    def create_menu(self):
        """
        Create menubar and menu action
        """
        # Create actions for file menu
        self.exit_act = QAction(QIcon('resources/images/exit.png'), 'Exit', self)
        self.exit_act.setShortcut('Ctrl+Q')
        self.exit_act.setStatusTip('Quit program')
        self.exit_act.triggered.connect(self.close)

        self.newGame_act = QAction(QIcon('resources/images/logo.png'), 'New game', self)
        self.newGame_act.setShortcut('Ctrl+N')
        self.newGame_act.setStatusTip('Start a new game')
        self.newGame_act.triggered.connect(self.new_game)

        # Create actions for configuration menu
        self.level0 = QAction("stupid boy", self, checkable=True)
        self.level1 = QAction("lightning", self, checkable=True)
        self.level1.setChecked(True)
        self.level0.triggered.connect(self.set_level0)
        self.level1.triggered.connect(self.set_level1)

        self.sound_act = QAction('Play sounds', self, checkable=True)
        self.sound_act.setStatusTip('Play sounds in the game')

        self.round_nb = QAction('Rounds...\t (' + str(N_rounds) + ')', self)
        self.round_nb.triggered.connect(self.set_rounds)
        self.round_nb.setStatusTip('Set the number of rounds for a match')

        # Create actions for help menu
        self.rules_act = QAction(QIcon('resources/images/help.png'), 'Rules', self)
        self.rules_act.setShortcut('F1')
        self.rules_act.setStatusTip('See the rules of Schotten Totten')
        self.rules_act.triggered.connect(self.show_rules)

        self.about_act = QAction(QIcon('resources/images/info.png'),
                                 'About Schotten Totten...', self)
        self.about_act.triggered.connect(self.show_info)

        # Create menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Create file menu and new game actions
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(self.newGame_act)
        file_menu.addAction(self.exit_act)

        # Create configuration menu
        config_menu = menu_bar.addMenu('&Config')
        level = config_menu.addMenu("Level")
        level.addAction(self.level0)
        level.addAction(self.level1)
        config_menu.addAction(self.sound_act)
        config_menu.addAction(self.round_nb)

        # Create help menu
        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(self.rules_act)
        help_menu.addAction(self.about_act)

        # Display info about actions in the status bar
        self.setStatusBar(QStatusBar(self))

    def set_level0(self):
        global difficulT
        self.level0.setChecked(True)
        self.level1.setChecked(False)
        difficulT = 0

    def set_level1(self):
        global difficulT
        self.level0.setChecked(False)
        self.level1.setChecked(True)
        difficulT = 1

    def set_rounds(self):
        self.new_N_rounds = N_rounds

        self.rounds_window = QWidget()

        msg = QLabel("Define how many rounds must be won to take away the game\n", self)

        self.sbox = QSpinBox(self)
        self.sbox.setRange(1, 10)
        self.sbox.setSingleStep(1)
        self.sbox.setValue(N_rounds)
        self.sbox.valueChanged.connect(self.newNRounds)

        okb = QPushButton("Ok", self)
        okb.clicked.connect(self.setNRounds)
        ccb = QPushButton("Cancel", self)
        ccb.clicked.connect(self.rounds_window.close)
        hbox = QHBoxLayout()
        hbox.addWidget(okb)
        hbox.addWidget(ccb)

        vbox = QVBoxLayout()
        vbox.addWidget(msg)
        vbox.addWidget(self.sbox)
        vbox.addLayout(hbox)

        self.rounds_window.setLayout(vbox)
        self.rounds_window.setGeometry(300, 300, 350, 250)
        self.rounds_window.setWindowTitle("Setting number of rounds")
        self.rounds_window.show()

    def new_nrounds(self):
        self.new_N_rounds = self.sbox.value()

    def set_nrounds(self):
        if self.new_N_rounds != N_rounds:
            N_rounds = self.new_N_rounds
        self.rounds_window.close()

    def show_rules(self):
        msg = "Les cartes Clan représentent les membres de votre tribu " \
              "écossaise que vous envoyez sur le terrain pour défendre les " \
              "Bornes. Chaque carte Clan existe en six couleurs différentes " \
              "et possède une force allant de 1 à 9 (1 étant la force la " \
              "plus faible)."

        helpBox = QMessageBox()
        helpBox.setIcon(QMessageBox.Question)
        helpBox.setWindowTitle("Les règles du jeu")
        helpBox.setText(msg)
        helpBox.setStandardButtons(QMessageBox.Ok)
        helpBox.exec_()

    def show_info(self):
        QMessageBox.about(self, "About Schotten Totten",
                          """<b> Schotten Totten</b> v %s
                          <p>Adaptation of the cards game developped
                          by Reiner Knizia et Djib
                          <p>Copyright &copy; 2016-2019 IELLO for the 
                          original cards game.
                          <p>Copyright &copy; 2020 Philippe Régnier for
                          this video game.""" % (__version__))

    def new_game(self):
        """
        Asking before creating a new game
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Are you sure you want to quit the " \
                    "current game and create a new one ?")
        msg.setWindowTitle("Warning !")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)

        returnValue = msg.exec()

        if returnValue == QMessageBox.Yes:
            self.createGame()
        else:
            pass

    def create_game(self):
        """
        Create a new Schotten Totten game
        """
        self.game = Game(self)
        self.setCentralWidget(self.game)

    def keyPressEvent(self, event):
        """
        Hidden short-cut pressed handler
        """
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_A:
                self.game.autoHandView()

    def keyReleaseEvent(self, event):  # NOT WORKING !!!
        """
        Hidden short-cut release handler
        """
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_A:
                self.game.autoHandClose()
