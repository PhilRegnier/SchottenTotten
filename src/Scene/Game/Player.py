from src.Scene.Game.Hand import Hand
from src.Scene.Game.Side import Side


class Player:

    def __init__(self, name):
        self.score = 0
        self.hand = Hand()
        self.side = [Side(i) for i in range(9)]
        self.name = name
