from PyQt6.QtCore import QRectF

from src.Scene.Game.displays.Digit import Digit
from src.Scene.Game.displays.Display import Display
from src.Style import MainGeometry


class Scorer(Display):

    def __init__(self, name_left, name_right):
        super(Scorer, self).__init__("SCORE")

        # instantiate children items

        self.text_left = self.text_displayed(name_left, self.max_width / 2 - 2 * self.marge_width)
        self.text_right = self.text_displayed(name_right, self.max_width / 2 - 2 * self.marge_width)
        self.ten_digit_left = Digit(self)
        self.unit_digit_left = Digit(self)
        self.ten_digit_right = Digit(self)
        self.unit_digit_right = Digit(self)

        # set geometry

        width = self.max_width

        height = self.ten_digit_left.boundingRect().height()\
                 + self.text_left.boundingRect().height()\
                 + self.title.boundingRect().height()\
                 + 3 * self.marge_height

        self.rect = QRectF(0, 0, width, height)

        # position items

        self.title.setPos(
            MainGeometry.centered(
                0,
                width,
                self.title.boundingRect().width()
            ),
            0
        )

        y = self.title.boundingRect().height() + self.marge_height

        self.text_left.setPos(
            MainGeometry.centered(
                self.marge_width,
                width / 2 - self.marge_width,
                self.text_left.boundingRect().width()
            ),
            y
        )
        self.text_right.setPos(
            MainGeometry.centered(
                width / 2 + self.marge_width,
                width / 2 - self.marge_width,
                self.text_right.boundingRect().width()
            ),
            y
        )

        y += self.text_left.boundingRect().height() + self.marge_height

        two_digits_width = self.ten_digit_left.boundingRect().width() * 2 + self.marge_width

        self.ten_digit_left.setPos(
            MainGeometry.centered(
                self.marge_width,
                width / 2 - self.marge_width,
                two_digits_width
            ),
            y
        )
        self.unit_digit_left.setPos(
            MainGeometry.centered(
                2 * self.marge_width + self.ten_digit_left.boundingRect().width(),
                width / 2 - self.marge_width,
                two_digits_width
            ),
            y
        )
        self.ten_digit_right.setPos(
            MainGeometry.centered(
                width / 2 + self.marge_width,
                width / 2 - self.marge_width,
                two_digits_width
            ),
            y
        )
        self.unit_digit_right.setPos(
            MainGeometry.centered(
                width / 2 + 2 * self.marge_width + self.ten_digit_left.boundingRect().width(),
                width / 2 - self.marge_width,
                two_digits_width
            ),
            y
        )

    def set_score_left(self, number):
        self.ten_digit_left.display_number(number // 10)
        self.unit_digit_left.display_number(number % 10)

    def set_score_right(self, number):
        self.ten_digit_right.display_number(number // 10)
        self.unit_digit_right.display_number(number % 10)


