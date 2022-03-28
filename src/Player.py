from src.Deck import Deck
from src.Hand import Hand
from src.Side import Side


class Player:

    def __init__(self, name):
        self.score = 0
        self.hand = Hand()
        self.side = Side()
        self.name = name
