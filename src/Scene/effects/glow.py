from PyQt6.QtWidgets import QGraphicsDropShadowEffect

from src.Style import GlobalStyle


class Glow(QGraphicsDropShadowEffect):
    def __init__(self, parent):
        super().__init__(parent)
        self.setColor(GlobalStyle.glow_color)
        self.setXOffset(0)
        self.setYOffset(0)
        self.setBlurRadius(10)
        self.setEnabled(False)

