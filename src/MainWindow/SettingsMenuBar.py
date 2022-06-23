from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QLabel, QSpinBox, QPushButton, QHBoxLayout, QVBoxLayout

from src.SettingsManager import SettingsManager


class SettingsMenuBar:

    def __init__(self, window):

        self.settings = SettingsManager()

        # Create actions

        # TODO: class pour level et OOP du choix

        self.level0_action = QAction('stupid boy', window)
        self.level0_action.setStatusTip("The easiest and dumbest one !")
        self.level0_action.setCheckable(True)
        self.level0_action.triggered.connect(self._set_level0)

        self.level1_action = QAction('lightning', window)
        self.level1_action.setStatusTip("A smarter one...")
        self.level1_action.setCheckable(True)
        self.level1_action.setChecked(True)
        self.level1_action.triggered.connect(self._set_level1)

        self.sound_action = QAction('Play sounds', window)
        self.sound_action.setCheckable(True)
        self.sound_action.setStatusTip('Play sounds in the game')

        self.round_nb_action = QAction('Rounds...\t (' + str(self.settings.get_number_of_rounds()) + ')', window)
        self.round_nb_action.triggered.connect(lambda: self._set_rounds(window))
        self.round_nb_action.setStatusTip('Set the number of rounds for a match')

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

    def _set_rounds(self, window):

        widget = QWidget()

        msg = QLabel("Define how many rounds must be won to take away the game\n", window)

        sbox = QSpinBox()
        sbox.setRange(1, 10)
        sbox.setSingleStep(1)
        sbox.setValue(self.settings.get_number_of_rounds())

        ok_button = QPushButton("&Ok")
        ok_button.clicked.connect(lambda: self._set_nrounds(sbox.value(), widget))
        cancel_button = QPushButton("&Cancel")
        cancel_button.clicked.connect(widget.close)

        hbox = QHBoxLayout()
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)

        vbox = QVBoxLayout()
        vbox.addWidget(msg)
        vbox.addWidget(sbox)
        vbox.addLayout(hbox)

        widget.setLayout(vbox)
        widget.setGeometry(300, 300, 350, 250)
        widget.setWindowTitle("Setting number of rounds")
        widget.show()

    def _set_nrounds(self, value, widget):
        self.settings.set_number_of_rounds(value)
        self.round_nb_action.setText('Rounds...\t (' + str(value) + ')')
        widget.close()
