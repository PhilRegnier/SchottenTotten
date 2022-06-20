#
# Text format
#
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPen
from PyQt5.QtWidgets import QGraphicsSimpleTextItem, QGraphicsDropShadowEffect


class TextInForeground(QGraphicsSimpleTextItem):
    def __init__(self, txt, parent_item):
        super().__init__()
        self.setParentItem(parent_item)
        self.setText(txt)
        self.setFont(QFont("Helvetica [Cronyx]", 28))
        self.setBrush(QColor(0, 114, 114, 255))

        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(67, 66, 37, 255))
        pen.setCapStyle(Qt.SquareCap)
        pen.setJoinStyle(Qt.BevelJoin)
        self.setPen(pen)

        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(31, 21, 17, 255))
        shadow.setBlurRadius(3)
        shadow.setXOffset(1)
        shadow.setYOffset(3)
        self.setGraphicsEffect(shadow)
