from PyQt5.QtWidgets import QAction, QWidget, QLabel, QSpinBox, QPushButton, QHBoxLayout, QVBoxLayout

from src.SettingsManager import SettingsManager


class SettingsMenuBar:

    def __init__(self, window):

        self.settings = SettingsManager()

        # Create actions

        # TODO: class pour level et OOP du choix

        self.level0_action = QAction('stupid boy', self)
        self.level0_action.setCheckable(True)
        self.level0_action.triggered.connect(self._set_level0)

        self.level1_action = QAction('lightning', self)
        self.level1_action.setCheckable(True)
        self.level1_action.setChecked(True)
        self.level1_action.triggered.connect(self._set_level1)

        self.sound_action = QAction('Play sounds', self)
        self.sound_action.setCheckable(True)
        self.sound_action.setStatusTip('Play sounds in the game')

        self.round_nb_action = QAction('Rounds...\t (' + str(self.settings.get_number_of_rounds()) + ')', self)
        self.round_nb_action.triggered.connect(self._set_rounds)
        self.round_nb_action.setStatusTip('Set the number of rounds for a match')

        # Prepare the window used to choose the number of rounds

        self.rounds_window = QWidget()

    def get_level0_action(self):
        return self.level0_action

    def get_level1_action(self):
        return self.level1_action

    def get_sound_action(self):
        return self.sound_action

    def get_round_nb_action(self):
        return self.round_nb_action

    def _set_level0(self):
        self.level0_action.setChecked(True)
        self.level1_action.setChecked(False)
        self.settings.set_difficulty(0)

    def _set_level1(self):
        self.level0_action.setChecked(False)
        self.level1_action.setChecked(True)
        self.settings.set_difficulty(1)

    def _set_rounds(self):

        msg = QLabel("Define how many rounds must be won to take away the game\n", self)

        sbox = QSpinBox()
        sbox.setRange(1, 10)
        sbox.setSingleStep(1)
        sbox.setValue(self.settings.get_number_of_rounds())

        ok_button = QPushButton("&Ok", self)
        ok_button.clicked.connect(lambda: self._set_nrounds(sbox.value))
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

    def _set_nrounds(self, value):
        self.settings.set_number_of_rounds(value)
        self.rounds_window.close()
