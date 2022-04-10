from PyQt5.QtWidgets import QMenuBar

from src.MainWindow.FileMenuBar import FileMenuBar
from src.MainWindow.HelpMenuBar import HelpMenuBar
from src.MainWindow.SettingsMenuBar import SettingsMenuBar


class MenuBar(QMenuBar):

    def __init__(self, window):
        super().__init__()

        self.fileMenuBar = FileMenuBar(window)
        self.settingsMenuBar = SettingsMenuBar(window)
        self.helpMenuBar = HelpMenuBar(window)
