#
# Statistics
#
from src.variables_globales import colors


class Statistics:
    auto_lh = []  # index where there is a card in the hand
    auto_ls = []  # index where there is a place or more in the side
    auto_ls0 = []  # index where there is no card in the side
    auto_ls1 = []  # index where there is one only card in the side
    auto_ls2 = []  # index where there are two cards in the side
    user_lh = []
    user_ls = []

    def __init__(cls):
        # record for indexes avaiable

        cls.auto_lh = [0, 1, 2, 3, 4, 5]
        cls.auto_ls = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        cls.auto_ls0 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        cls.user_lh = [0, 1, 2, 3, 4, 5]
        cls.user_ls = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        # data for cards played

        cls.cjc = [[colors[0], 0], [colors[1], 0], [colors[2], 0],
                    [colors[3], 0], [colors[4], 0], [colors[5], 0]]

        cls.cjv = [range(9), 0]
        cls.cjn = 0

        # data for cards in the deck or in the other hand

        cls.csc = [[colors[0], 9], [colors[1], 9], [colors[2], 9],
                    [colors[3], 9], [colors[4], 9], [colors[5], 9]]
        cls.csv = [range(9), 6]
        cls.csn = 54

    @classmethod
    def autoLh(cls):
        return cls.auto_lh

    @classmethod
    def autoLs(cls):
        return cls.auto_ls

    @classmethod
    def autoLs0(cls):
        return cls.auto_ls0

    @classmethod
    def autoLs1(cls):
        return cls.auto_ls1

    @classmethod
    def autoLs2(cls):
        return cls.auto_ls2

    @classmethod
    def removeAutoHand(cls, index):
        for i in range(len(cls.auto_lh)):
            if cls.auto_lh[i] == index:
                del cls.auto_lh[i]
                break

    @classmethod
    def addCardToAutoSide(cls, side):

        if side.nCard == 1:
            cls.auto_ls1.append(side_nb)
            cls.auto_ls1.sort()
            for i in range(len(cls.auto_ls0)):
                if cls.auto_ls0[i] == side_nb:
                    del cls.auto_ls0[i]
                    break

        elif side.nCard == 2:
            for i in range(len(cls.auto_ls1)):
                if cls.auto_ls1[i] == side_nb:
                    del cls.auto_ls1[i]
                    break

            cls.auto_ls2.append(side_nb)
            cls.auto_ls2.sort()

        else:
            for i in range(len(cls.auto_ls)):
                if cls.auto_ls[i] == side_nb:
                    del cls.auto_ls[i]
                    break

            for i in range(len(cls.auto_ls2)):
                if cls.auto_ls2[i] == side_nb:
                    del cls.auto_ls2[i]
                    break
