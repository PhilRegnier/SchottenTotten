# Shadow on movable or clickable items

from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from src.Style import GlobalStyle


class Shader(QGraphicsDropShadowEffect):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColor(GlobalStyle.ombrage_color)
        self.setXOffset(4)
        self.setYOffset(4)
        self.setBlurRadius(3)
        self.setEnabled(False)
