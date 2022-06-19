#
# Statistics
#
from src.Scene.Game.CardManager import CardManager
from src.Singleton import Singleton


class Statistics:

    def __init__(self, sides):

        # records for indexes available

        self._auto_ls = []  # sides where there is a place or more
        self._auto_ls0 = []  # sides where there is no card
        self._auto_ls1 = []  # sides where there is exactly one only card
        self._auto_ls2 = []  # sides where there are exactly two cards

        self.reset_stat_sides(sides)

        # self._user_lh = [0, 1, 2, 3, 4, 5]
        # self._user_ls = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        # data for cards played

        # self._cjc = [[CardManager().colors[0], 0], [CardManager().colors[1], 0], [CardManager().colors[2], 0],
        #        [CardManager().colors[3], 0], [CardManager().colors[4], 0], [CardManager().colors[5], 0]]
        # self._cjv = [range(9), 0]
        # self._cjn = 0

        # data for cards in the deck or in the other hand

        # self._csc = [[CardManager().colors[0], 9], [CardManager().colors[1], 9], [CardManager().colors[2], 9],
        #              [CardManager().colors[3], 9], [CardManager().colors[4], 9], [CardManager().colors[5], 9]]
        # self._csv = [range(9), 6]
        # self._csn = 54

    def auto_ls(self):
        return self._auto_ls

    def auto_ls0(self):
        return self._auto_ls0

    def auto_ls1(self):
        return self._auto_ls1

    def auto_ls2(self):
        return self._auto_ls2

    def add_card_to_autoside(self, side):
        match len(side.cards):
            case 0:
                self._auto_ls1.append(side)
                self._auto_ls0.remove(side)

            case 1:
                self._auto_ls2.append(side)
                self._auto_ls1.remove(side)

            case 2:
                self._auto_ls.remove(side)
                self._auto_ls2.remove(side)

    def reset_stat_sides(self, sides):
        self._auto_ls.clear()
        self._auto_ls0.clear()
        self._auto_ls1.clear()
        self._auto_ls2.clear()
        for side in sides:
            match len(side.cards):
                case 0:
                    self._auto_ls.append(side)
                    self._auto_ls0.append(side)
                case 1:
                    self._auto_ls.append(side)
                    self._auto_ls1.append(side)
                case 2:
                    self._auto_ls.append(side)
                    self._auto_ls2.append(side)


