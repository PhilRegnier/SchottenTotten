from src.Scene.Game.Hand import Hand
from src.Scene.Game.Playmat import Playmat
from src.Scene.Game.Side import Side


class Player:

    def __init__(self, name, colors):
        self.score = 0
        self.colors = colors
        self.hand = Hand()
        self.sides = [Side(i, self.colors, self) for i in range(9)]
        self.playmat = Playmat(self.colors)
        self.name = name

