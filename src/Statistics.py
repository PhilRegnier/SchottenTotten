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

    def __init__(self):
        global auto_lh, auto_ls, auto_ls0, auto_ls1, auto_ls2, user_lh, user_ls

        # record for indexes avaiable

        auto_lh = [0, 1, 2, 3, 4, 5]
        auto_ls = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        auto_ls0 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        auto_ls1 = []
        auto_ls2 = []
        user_lh = [0, 1, 2, 3, 4, 5]
        user_ls = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        # data for cards played

        self.cjc = [[colors[0], 0], [colors[1], 0], [colors[2], 0],
                    [colors[3], 0], [colors[4], 0], [colors[5], 0]]

        self.cjv = [range(9), 0]
        self.cjn = 0

        # data for cards in the deck or in the other hand

        self.csc = [[colors[0], 9], [colors[1], 9], [colors[2], 9],
                    [colors[3], 9], [colors[4], 9], [colors[5], 9]]
        self.csv = [range(9), 6]
        self.csn = 54

    def autoLh(self):
        global auto_lh
        return auto_lh

    def autoLs(self):
        global auto_ls
        return auto_ls

    def autoLs0(self):
        global auto_ls0
        return auto_ls0

    def autoLs1(self):
        global auto_ls1
        return auto_ls1

    def autoLs2(self):
        global auto_ls2
        return auto_ls2

    def removeAutoHand(self, index):
        global auto_lh
        for i in range(len(auto_lh)):
            if auto_lh[i] == index:
                del auto_lh[i]
                break

    def addCardToAutoSide(self, side):
        global side_nb, auto_ls, auto_ls0, auto_ls1, auto_ls2

        if side.nCard == 1:
            auto_ls1.append(side_nb)
            auto_ls1.sort()
            for i in range(len(auto_ls0)):
                if auto_ls0[i] == side_nb:
                    del auto_ls0[i]
                    break

        elif side.nCard == 2:
            for i in range(len(auto_ls1)):
                if auto_ls1[i] == side_nb:
                    del auto_ls1[i]
                    break

            auto_ls2.append(side_nb)
            auto_ls2.sort()

        else:
            for i in range(len(auto_ls)):
                if auto_ls[i] == side_nb:
                    del auto_ls[i]
                    break

            for i in range(len(auto_ls2)):
                if auto_ls2[i] == side_nb:
                    del auto_ls2[i]
                    break
