#
# Text format
#
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QGraphicsSimpleTextItem

from src.variables_globales import mainWindow_width, mainWindow_height


class TextInForeground(QGraphicsSimpleTextItem):
    def __init__(self, txt, parent_item):
        super().__init__()
        self.setText(txt)
        self.setFont(QFont("Helvetica [Cronyx]", 25))
        self.setBrush(QColor(255, 85, 0, 140))
        self.setPen(QColor(21, 11, 127, 90))
        self.setParentItem(parent_item)
        xm = (mainWindow_width - self.boundingRect().width()) / 2
        ym = (mainWindow_height - self.boundingRect().height()) / 2
        self.setPos(xm, ym)
