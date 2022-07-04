from PyQt6.QtWidgets import QGraphicsDropShadowEffect

from src.Style import GlobalStyle


class Shadow(QGraphicsDropShadowEffect):
    def __init__(self, x_offset=1, y_offset=3):
        super().__init__()
        self.setColor(GlobalStyle.shadow_color)
        self.setBlurRadius(3)
        self.setXOffset(x_offset)
        self.setYOffset(y_offset)
