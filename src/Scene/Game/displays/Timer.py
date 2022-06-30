from PyQt6.QtCore import QRectF, QTimer

from src.Scene.Game.displays.Digit import Digit
from src.Scene.Game.displays.Display import Display
from src.Style import MainGeometry
from src.TextInForeground import TextInForeground


class Timer(Display):

    def __init__(self):
        super(Timer, self).__init__("TIMER")

        self.time_left = None

        self.countdown = QTimer(self)
        self.countdown.setInterval(1000)

        # instantiate children items

        self.unit_min = Digit(self)
        self.ten_sec = Digit(self)
        self.unit_sec = Digit(self)
        self.sep = TextInForeground(":", self)

        # set geometry

        width = max(
            self.title.boundingRect().width() + 2 * self.marge_width,
            self.ten_sec.boundingRect().width() * 3 + self.sep.boundingRect().width() + self.marge_width * 6
        )
        height = self.title.boundingRect().height() + self.unit_min.boundingRect().height() + 2 * self.marge_height

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

        self.unit_min.setPos(
            MainGeometry.centered(
                0,
                width,
                (self.ten_sec.boundingRect().width() + self.marge_width) * 3 + self.sep.boundingRect().width()
            ),
            y
        )
        self.sep.setPos(self.unit_min.x() + self.unit_min.boundingRect().width() + self.marge_width, y)
        self.ten_sec.setPos(self.sep.x() + self.sep.boundingRect().width() + self.marge_width, y)
        self.unit_sec.setPos(self.ten_sec.x() + self.ten_sec.boundingRect().width() + self.marge_width, y)

    def set_time(self):
        self.time_left -= 1
        self.unit_min.display_number(self.time_left // 60)
        self.ten_sec.display_number((self.time_left % 60) // 10)
        self.unit_sec.display_number((self.time_left % 60) % 10)

    def start(self, max_time):
        self.time_left = max_time + 1
        self.set_time()
        self.countdown.timeout.connect(self.set_time)
        self.countdown.start(max_time)
