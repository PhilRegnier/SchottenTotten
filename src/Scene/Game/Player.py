from random import choice

from src.Scene.Game.Playmat import Playmat
from src.Scene.Game.ShiftManager import ShiftManager
from src.Scene.Game.Side import Side
from src.Scene.Game.Statistics import Statistics


class Player:

    def __init__(self, name, colors, accept_hover_event=False):
        self.round_score = 0
        self.total_score = 0
        self.name = name
        self.colors = colors
        self.sides = [Side(i, self.colors, self, accept_hover_event) for i in range(9)]
        self.playmat = Playmat(self.colors)
        self.shift_manager = ShiftManager()
        self.statistics = Statistics(self.sides)


