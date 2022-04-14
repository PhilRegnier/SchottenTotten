from src.Scene.Game.Hand import Hand
from src.Scene.Game.Playmat import Playmat
from src.Scene.Game.Side import Side
from src.Style import ColorStyle


class Player:

    def __init__(self, name):
        self.score = 0
        self.color = ColorStyle()
        self.hand = Hand()
        self.sides = [Side(i, self.color) for i in range(9)]
        self.playmat = Playmat(self.color)
        self.name = name

