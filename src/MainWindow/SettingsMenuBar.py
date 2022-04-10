from PyQt5.QtWidgets import QAction, QWidget, QLabel, QSpinBox, QPushButton, QHBoxLayout, QVBoxLayout

from src.SettingsManager import SettingsManager


class SettingsMenuBar:

    def __init__(self, window):

        self.settings = SettingsManager()

        # Create actions

        # TODO: class pour level et OOP du choix

        self.level0 = QAction('stupid boy', self)
        self.level0.setCheckable(True)
        self.level0.triggered.connect(self.set_level0)

        self.level1 = QAction('lightning', self)
        self.level1.setCheckable(True)
        self.level1.setChecked(True)
        self.level1.triggered.connect(self.set_level1)

        self.sound_act = QAction('Play sounds', self)
        self.sound_act.setCheckable(True)
        self.sound_act.setStatusTip('Play sounds in the game')

        self.round_nb = QAction('Rounds...\t (' + str(self.settings.get_number_of_rounds()) + ')', self)
        self.round_nb.triggered.connect(self.set_rounds)
        self.round_nb.setStatusTip('Set the number of rounds for a match')

        # Prepare the window used to choose the number of rounds

        self.rounds_window = QWidget()

    def set_level0(self):
        self.level0.setChecked(True)
        self.level1.setChecked(False)
        self.settings.set_difficulty(0)

    def set_level1(self):
        self.level0.setChecked(False)
        self.level1.setChecked(True)
        self.settings.set_difficulty(1)

    def set_rounds(self):

        msg = QLabel("Define how many rounds must be won to take away the game\n", self)

        sbox = QSpinBox()
        sbox.setRange(1, 10)
        sbox.setSingleStep(1)
        sbox.setValue(self.settings.get_number_of_rounds())

        ok_button = QPushButton("&Ok", self)
        ok_button.clicked.connect(lambda: self.set_nrounds(sbox.value))
        cancel_button = QPushButton("&Cancel", self)
        cancel_button.clicked.connect(self.rounds_window.close)

        hbox = QHBoxLayout()
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)

        vbox = QVBoxLayout()
        vbox.addWidget(msg)
        vbox.addWidget(sbox)
        vbox.addLayout(hbox)

        self.rounds_window.setLayout(vbox)
        self.rounds_window.setGeometry(300, 300, 350, 250)
        self.rounds_window.setWindowTitle("Setting number of rounds")
        self.rounds_window.show()

    def set_nrounds(self, value):
        self.settings.set_number_of_rounds(value)
        self.rounds_window.close()
