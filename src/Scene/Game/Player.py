from src.Scene.Game.Playmat import Playmat
from src.Scene.Game.Side import Side


class Player:

    def __init__(self, name, colors):
        self.round_score = 0
        self.total_score = 0
        self.name = name
        self.colors = colors
        self.sides = [Side(i, self.colors, self) for i in range(9)]
        self.playmat = Playmat(self.colors)

