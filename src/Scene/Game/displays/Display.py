from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsItem

from src.Style import MainGeometry, DisplayStyle
from src.TextInForeground import TextInForeground


class Display(QGraphicsItem):

    max_width = 0
    marge_width = 8
    marge_height = 8
    ext_marge_height = 20

    def __init__(self, name):
        super(Display, self).__init__()
        if Display.max_width == 0:
            Display.set_size()
        self.title = self.text_displayed(name, self.max_width - 2 * self.marge_width)
        self.rect = None

    def boundingRect(self):
        return QRectF(
            - MainGeometry.pen_width,
            - MainGeometry.pen_width,
            self.rect.width() + MainGeometry.pen_width,
            self.rect.height() + MainGeometry.pen_width
        )

    def paint(self, painter, option, widget=0):
        painter.setBrush(DisplayStyle.brush)
        painter.setPen(DisplayStyle.pen)
        painter.drawRoundedRect(self.rect, MainGeometry.r_bound, MainGeometry.r_bound)

    def text_displayed(self, string, max_width):
        touch = False
        text = TextInForeground(string, self)
        while text.boundingRect().width() > max_width:
            string = string[:len(string) - 1]
            touch = True
            text.setText(string)

        if touch:
            string += "."

        text.setText(string)
        return text

    @classmethod
    def set_size(cls):
        cls.max_width = MainGeometry.width * MainGeometry.width_display_ratio

