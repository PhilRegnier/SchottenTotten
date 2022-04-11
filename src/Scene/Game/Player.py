from src.Scene.Game.Hand import Hand
from src.Scene.Game.Playmat import Playmat
from src.Scene.Game.Side import Side


class Player:

    def __init__(self, name, gradient_color1, gradient_color2, pen_color):
        self.score = 0
        self.hand = Hand()
        self.sides = [Side(i) for i in range(9)]
        self.playmat = Playmat(gradient_color1, gradient_color2, pen_color)
        self.name = name

