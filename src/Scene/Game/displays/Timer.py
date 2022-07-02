from PyQt6.QtCore import QRectF, QTimer, pyqtSignal, QObject, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPen, QBrush
from PyQt6.QtWidgets import QGraphicsRectItem

from src.Scene.Game.displays.Digit import Digit
from src.Scene.Game.displays.Display import Display
from src.Style import MainGeometry, WarningStyle, DisplayStyle
from src.TextInForeground import TextInForeground


class TimeOut(QObject):
    signal = pyqtSignal()

    def __init__(self):
        super(TimeOut, self).__init__()


class Timer(Display):

    def __init__(self, function):
        super().__init__("TIMER")
        self.time_left = None

        self.countdown = QTimer()
        self.countdown.setInterval(1000)
        self.countdown.timeout.connect(self.set_time)
        self.time_out = TimeOut()
        self.time_out.signal.connect(function)

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
        self.sep.setPos(self.unit_min.x() + self.unit_min.boundingRect().width() + self.marge_width, y - 10)
        self.ten_sec.setPos(self.sep.x() + self.sep.boundingRect().width() + self.marge_width, y)
        self.unit_sec.setPos(self.ten_sec.x() + self.ten_sec.boundingRect().width() + self.marge_width, y)

        # prepare animation for warning

        self.warning = None

    def set_time(self):
        self.time_left -= 1
        self.unit_min.display_number(self.time_left // 60)
        self.ten_sec.display_number((self.time_left % 60) // 10)
        self.unit_sec.display_number((self.time_left % 60) % 10)

        if self.time_left == 10:
            self.set_warning()

        if self.time_left == 0:
            self.time_out.signal.emit()

    def start(self, max_time):
        self.set_normal()
        self.time_left = max_time + 1
        self.set_time()
        self.countdown.start()

    def set_warning(self):
        self.brush = WarningStyle.brush
        self.pen = WarningStyle.pen
        self.update()
        self.warning = QPropertyAnimation(self, b"opacity")
        self.warning.setKeyValueAt(0., 0.9)
        self.warning.setKeyValueAt(0.5, 0.5)
        self.warning.setKeyValueAt(1., 0.9)
        self.warning.setDuration(1000)
        self.warning.setEasingCurve(QEasingCurve.Type.InOutExpo)
        self.warning.setLoopCount(-1)
        self.warning.start()

    def set_normal(self):
        if self.warning is not None:
            self.warning.stop()
        self.brush = DisplayStyle.brush
        self.pen = DisplayStyle.pen
        self.setOpacity(1.)
        self.update()

