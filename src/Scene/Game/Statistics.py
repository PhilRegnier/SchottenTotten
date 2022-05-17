#
# Statistics
#


class Statistics:

    def __init__(self, colors):

        # record for indexes avaiable

        self._auto_lh = [0, 1, 2, 3, 4, 5]               # index where there is a card in the hand
        self._auto_ls = [0, 1, 2, 3, 4, 5, 6, 7, 8]      # index where there is a place or more in the side
        self._auto_ls0 = [0, 1, 2, 3, 4, 5, 6, 7, 8]     # index where there is no card in the side
        self._user_lh = [0, 1, 2, 3, 4, 5]
        self._user_ls = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        self._auto_ls1 = []                              # index where there is one only card in the side
        self._auto_ls2 = []                              # index where there are two cards in the side

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

    def auto_lh(self):
        return self._auto_lh

    def auto_ls(self):
        return self._auto_ls

    def auto_ls0(self):
        return self._auto_ls0

    def auto_ls1(self):
        return self._auto_ls1

    def auto_ls2(self):
        return self._auto_ls2

    def remove_from_hand(self, index):
        for i in range(len(self._auto_lh)):
            if self._auto_lh[i] == index:
                del self._auto_lh[i]
                break

    def add_card_to_autoside(self, side):
        if side.nCard == 1:
            self._auto_ls1.append(side.numero)
            self._auto_ls1.sort()
            for i in range(len(self._auto_ls0)):
                if self._auto_ls0[i] == side.numero:
                    del self._auto_ls0[i]
                    break

        elif side.nCard == 2:
            for i in range(len(self._auto_ls1)):
                if self._auto_ls1[i] == side.numero:
                    del self._auto_ls1[i]
                    break

            self._auto_ls2.append(side.numero)
            self._auto_ls2.sort()

        else:
            for i in range(len(self._auto_ls)):
                if self._auto_ls[i] == side.numero:
                    del self._auto_ls[i]
                    break

            for i in range(len(self._auto_ls2)):
                if self._auto_ls2[i] == side.numero:
                    del self._auto_ls2[i]
                    break
