#------------------------------------------------------------------------------------------------------
# Shadow on movable or clickable items
#------------------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from src.variables_globales import ombrage_color


class Ombrage(QGraphicsDropShadowEffect):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColor(ombrage_color)
        self.setXOffset(4)
        self.setYOffset(4)
        self.setBlurRadius(3)
        self.setEnabled(False)
