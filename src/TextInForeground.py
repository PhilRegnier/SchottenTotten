#
# Text format
#
from PyQt6.QtWidgets import QGraphicsSimpleTextItem

from src.Scene.effects.Shadow import Shadow
from src.Style import Pen, GlobalStyle


class TextInForeground(QGraphicsSimpleTextItem):

    def __init__(self, txt, parent_item):
        super().__init__()
        self.setParentItem(parent_item)
        self.setText(txt)
        self.setFont(GlobalStyle.text_font)
        self.setBrush(GlobalStyle.text_color)
        self.setPen(Pen())
        self.setGraphicsEffect(Shadow())

