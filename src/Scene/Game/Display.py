from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsItem

from src.Style import GeometryStyle, DisplayStyle
from src.TextInForeground import TextInForeground


class Display(QGraphicsItem):

    max_width = 0
    marge_width = 5
    marge_height = 5

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

        flag = True
        text = TextInForeground(string, self)
        while flag:
            if text.boundingRect().width() > max_width:
                string = string[:len(string) - 1]
                text.setText(string)
            else:
                flag = False

        text.setText(string)
        return text

    @classmethod
    def set_size(cls):
        cls.max_width = GeometryStyle.main_width * GeometryStyle.width_display_ratio
