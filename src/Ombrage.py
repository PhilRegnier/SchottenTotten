#------------------------------------------------------------------------------------------------------
# Shadow on movable or clickable items
#------------------------------------------------------------------------------------------------------
class Ombrage(QGraphicsDropShadowEffect):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColor(ombrage_color)
        self.setXOffset(4)
        self.setYOffset(4)
        self.setBlurRadius(3)
        self.setEnabled(False)
