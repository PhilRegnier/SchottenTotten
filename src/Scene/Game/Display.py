from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsItem

from src.Style import GeometryStyle, DisplayStyle
from src.TextInForeground import TextInForeground


class Display(QGraphicsItem):

    max_width = 0
    marge_width = 8
    marge_height = 8

    def __init__(self):
        super(Display, self).__init__()
        if Display.max_width == 0:
            Display.set_size()
        self.rect = None

    def boundingRect(self):
        return QRectF(
            - GeometryStyle.pen_width,
            - GeometryStyle.pen_width,
            self.rect.width() + GeometryStyle.pen_width,
            self.rect.height() + GeometryStyle.pen_width
        )

    def paint(self, painter, option, widget=0):
        painter.setBrush(DisplayStyle.brush)
        painter.setPen(DisplayStyle.pen)
        painter.drawRoundedRect(self.rect, GeometryStyle.r_bound, GeometryStyle.r_bound)

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
        cls.max_width = GeometryStyle.main_width * GeometryStyle.width_display_ratio

    @staticmethod
    def centered(pos0, total_width, effective_width):
        # TODO : test if total > effective...
        return pos0 + (total_width - effective_width) / 2
