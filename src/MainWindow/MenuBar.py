from PyQt6.QtWidgets import QMenuBar

from src.MainWindow.FileMenuBar import FileMenuBar
from src.MainWindow.HelpMenuBar import HelpMenuBar
from src.MainWindow.SettingsMenuBar import SettingsMenuBar


class MenuBar(QMenuBar):

    # Prepare the menus

    def __init__(self, window):
        super().__init__(window)

        self.fileMenuBar = FileMenuBar(window)
        self.settingsMenuBar = SettingsMenuBar(window)
        self.helpMenuBar = HelpMenuBar(window)

        self.setNativeMenuBar(False)

    # Add menus

    def add_menus(self):
        file_menu = self.addMenu('&File')
        file_menu.addAction(self.fileMenuBar.get_new_game_action())
        file_menu.addAction(self.fileMenuBar.get_exit_action())

        settings_menu = self.addMenu('&Config')
        level = settings_menu.addMenu("Difficulty level")
        level.addAction(self.settingsMenuBar.get_level0_action())
        level.addAction(self.settingsMenuBar.get_level1_action())
        settings_menu.addAction(self.settingsMenuBar.get_sound_action())
        settings_menu.addAction(self.settingsMenuBar.get_round_nb_action())

        help_menu = self.addMenu('&Help')
        help_menu.addAction(self.helpMenuBar.get_rules_action())
        help_menu.addAction(self.helpMenuBar.get_about_action())
