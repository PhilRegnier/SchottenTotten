from PyQt6.QtWidgets import QGraphicsItem

from src.Scene.Game.Display import Display


class Timer(Display):

    def __init__(self):
        super(Timer, self).__init__()

        # instantiate children items
