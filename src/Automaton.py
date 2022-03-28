from random import choice

from src.Player import Player
from src.Settings import Settings
from src.Statistics import Statistics


class Automaton(Player):

    def __init__(self):
        super().__init__()
        self.statistics = Statistics()

    # Ask the automaton to play a card on his side

    def play_a_card(self):
        if Settings.get_difficulty() == 1:
            self.cervo1()
        else:
            self.cervo0()

        # move the card and draw a new one

        ms = MovingCard.side_id()
        mh = MovingCard.hand_id()
        MovingCard.set_card_id(self.auto_hand[mh])
        mc = MovingCard.card_id()

        pos = Card.cards[mc].anchorPoint
        self.side[ms].addCard(mc)
        self.statistics.add_card_to_autoside()
        pos0 = self.auto_deck.pos() - self.auto_side[ms].pos() + pos
        Card.cards[mc].moveTo(pos0, Card.cards[mc].anchorPoint)

        if self.deck.isEmpty():
            self.auto_hand[mh] = -1
            self.statistics.remove_auto_hand(mh)
            if sum(self.auto_hand) == -6:
                self.ending = True
        else:
            self.auto_hand[mh] = self.deck.draw()
            Card.cards[self.auto_hand[mh]].setVisible(True)
            Card.cards[self.auto_hand[mh]].setParentItem(self.auto_deck)
            Card.cards[self.auto_hand[mh]].setAnchorPoint(pos)
            Card.cards[self.auto_hand[mh]].setPos(pos)

    # Automate 0 : random card and random stone

    def cervo0(self):
        MovingCard.set_hand_id(choice(self.statistics.auto_lh()))
        MovingCard.set_side_id(choice(self.statistics.auto_ls()))

    # Automate 1 : first steps choice

    def cervo1(self):
        # Settings for memorization of relevant combinations

        memo = []

        # Setting cards color and valor in lists

        v = [0 for i in range(6)]
        c = ["0" for i in range(6)]

        for i in self.statistics.auto_lh():
            v[i] = Card.cards[self.auto_hand[i]].valeur
            c[i] = Card.cards[self.auto_hand[i]].couleur

        # 1 Looking in the hand

        for i in self.statistics.auto_lh():
            for j in self.statistics.auto_lh():
                if i != j:

                    dvij = v[i] - v[j]

                    # For flush pair(s)

                    if c[i] == c[j] and 3 > dvij > -3:
                        for k in Statistics.autoLs1():
                            if c[i] == Card.cards[self.auto_side[k].index[0]].couleur:
                                dvik = v[i] - Card.cards[self.auto_side[k].index[0]].valeur
                                if (dvij == 2 and dvik == 1) \
                                        or (dvij == -2 and dvik == -1) \
                                        or (dvij == 1 and dvik == 2) \
                                        or (dvij == -1 and dvik == -2):
                                    memo.append(Memo(i, k, cote_both))

                    # For pair(s)

                    if dvij == 0:
                        for k in Statistics.autoLs1():
                            if v[i] == Card.cards[self.auto_side[k].index[0]].valeur:
                                memo.append(Memo(i, k, cote_brelan))

        # 2 Search in the sides with 2 cards

        for i in self.statistics.auto_lh():
            for k in self.statistics.auto_ls2():

                dvij = v[i] - Card.cards[self.auto_side[k].index[0]].valeur
                dvik = v[i] - Card.cards[self.auto_side[k].index[1]].valeur

                lcolor = (c[i] == Card.cards[self.auto_side[k].index[0]].couleur
                          and c[i] == Card.cards[self.auto_side[k].index[1]].couleur)

                lsuite = ((dvij == -1 and dvik == -2)
                          or (dvij == -2 and dvik == -1)
                          or (dvij == 1 and dvik == -1)
                          or (dvij == -1 and dvik == 1)
                          or (dvij == 2 and dvik == 1)
                          or (dvij == 1 and dvik == 2))

                # Test if a card in the hand goes to flush third

                if lcolor and lsuite:
                    memo.append(Memo(i, k, cote_both * 1.5))

                # Test if a card in the hand goes to 3 of a kind

                if dvij == 0 and dvik == 0:
                    memo.append(Memo(i, k, cote_brelan * 1.5))

                # Test if a card in the hand goes to color

                if lcolor:
                    memo.append(Memo(i, k, cote_couleur))

                # Test if a card in the hand goes to suite

                if lsuite:
                    memo.append(Memo(i, k, cote_suite))

        # 3 Search in the sides with 1 card

        for i in self.statistics.auto_lh():
            for k in self.statistics.auto_ls1():

                dvij = v[i] - Card.cards[self.auto_side[k].index[0]].valeur

                lcolor = (c[i] == Card.cards[self.auto_side[k].index[0]].couleur)
                lsuite = (dvij == -1 or dvij == -2 or dvij == 1 or dvij == 2)

                # Test if a card of the hand matchs for flush third

                if lcolor and lsuite:
                    memo.append(Memo(i, k, cote_both))

                # Test if a card of the hand matchs for 3 of a kind

                if dvij == 0:
                    memo.append(Memo(i, k, cote_brelan / 1.5))

                # Test if a card of the hand matchs for color

                if lcolor:
                    memo.append(Memo(i, k, cote_couleur / 1.5))

                # Test if a card of the hand match for suite

                if lsuite:
                    memo.append(Memo(i, k, cote_suite))

        # Choosing the best combination

        if memo:
            c = 0.0
            k = 0
            for i in range(len(memo)):
                c = max(c, memo[i].cote)
                if c == memo[i].cote:
                    k = i

            MovingCard.set_hand_id(memo[k].hand)
            MovingCard.set_side_id(memo[k].side)
            return

        # 4 Play a random card on a random free side

        if self.statistics.auto_ls0():
            MovingCard.set_side_id(choice(self.statistics.auto_ls0()))
            MovingCard.set_hand_id(choice(self.statistics.auto_lh()))
            return

        # 5 Last call...

        self.cervo0()
