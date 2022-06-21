#
# Text format
#
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QGraphicsSimpleTextItem

from src.Style import Pen, Shadow


class TextInForeground(QGraphicsSimpleTextItem):
    def __init__(self, txt, parent_item):
        super().__init__()
        self.setParentItem(parent_item)
        self.setText(txt)
        self.setFont(QFont("Helvetica [Cronyx]", 28))
        self.setBrush(QColor(0, 114, 114, 255))
        self.setPen(Pen())
        self.setGraphicsEffect(Shadow())
