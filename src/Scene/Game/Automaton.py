from random import choice

from PyQt5.QtGui import QColor

from src.Scene.Game.Card import Card
from src.Scene.Game.CardManager import CardManager
from src.Scene.Game.Option import Option
from src.Scene.Game.Player import Player
from src.Scene.Game.Statistics import Statistics
from src.Scene.Game.Umpire import Umpire
from src.SettingsManager import SettingsManager


class Automaton(Player):

    def __init__(self, parent, name):
        super().__init__(name)
        self.settingsManager = SettingsManager()
        self.cardManager = CardManager()
        self.statistics = Statistics(self.cardManager.colors)
        self.board = parent

        # override player's colors style

        self.color.side0 = QColor(70, 23, 0, 90)
        self.color.side1 = QColor(255, 85, 0, 90)
        self.color.hand = QColor(49, 53, 42, 150)
        self.color.hand_pen = QColor(10, 11, 8)
    """
    Ask the automaton to play a card on his side
    """
    def play_a_card(self):

        # select an option

        if self.settingsManager.get_difficulty() == 1:
            self.cervo1()
        else:
            self.cervo0()

        # move the card selected by cervo and draw a new one

        shift_card = self.cardManager.shift_card
        shift_side = self.cardManager.shift_side
        pos = shift_card.anchorPoint
        shift_side.add_card(shift_card)
        pos0 = self.playmat.pos() - shift_side.pos() + pos
        self.cardManager.shift_card.moveTo(pos0, shift_card.anchorPoint)

        if self.board.deck.is_empty():
            self.auto_hand[hand_nb] = -1
            stats.removeAutoHand(hand_nb)
            if sum(self.auto_hand) == -6:
                self.ending = True
        else:
            new_card = self.board.deck.draw()
            new_card.setVisible(True)
            new_card.setParentItem(self.playmat)
            new_card.setAnchorPoint(pos)
            new_card.setPos(pos)
            self.hand.add(new_card)

    """
    Automate 0 : random card and random stone
    """
    def cervo0(self):
        self.cardManager.set_shift_hand(choice(self.statistics.auto_lh()))
        self.cardManager.set_shift_side(choice(self.statistics.auto_ls()))

    """
    Automate 1 : first steps choice
    """
    def cervo1(self):

        # Settings for memorization of relevant combinations

        options = []

        # Setting cards color and valor in lists

        v = [0 for i in range(6)]
        c = ["0" for i in range(6)]

        for i in self.statistics.auto_lh():
            v[i] = self.hand.cards[i].valeur
            c[i] = self.hand.cards[i].couleur

        # 1 Look at the hand

        for i in self.statistics.auto_lh():
            for j in self.statistics.auto_lh():
                if i != j:

                    dvij = v[i] - v[j]

                    # For flush pair(s)

                    if c[i] == c[j] and 3 > dvij > -3:
                        for k in self.statistics.autoLs1():
                            if c[i] == self.cardManager.cards[self.sides[k].index[0]].couleur:
                                dvik = v[i] - self.cardManager.cards[self.sides[k].index[0]].valeur
                                if (dvij == 2 and dvik == 1) \
                                        or (dvij == -2 and dvik == -1) \
                                        or (dvij == 1 and dvik == 2) \
                                        or (dvij == -1 and dvik == -2):
                                    options.append(Option(i, k, Umpire.cote_both))

                    # For pair(s)

                    if dvij == 0:
                        for k in self.statistics.autoLs1():
                            if v[i] == Card.cards[self.sides[k].index[0]].valeur:
                                options.append(Option(i, k, Umpire.cote_brelan))

        # 2 Search into sides with 2 cards

        for i in self.statistics.auto_lh():
            for k in self.statistics.auto_ls2():

                dvij = v[i] - self.sides[k].cards.index[0].valeur
                dvik = v[i] - self.sides[k].cards.index[1].valeur

                lcolor = (c[i] == self.sides[k].cards.index[0].couleur
                          and c[i] == self.sides[k].cards.index[1].couleur)

                lsuite = ((dvij == -1 and dvik == -2)
                          or (dvij == -2 and dvik == -1)
                          or (dvij == 1 and dvik == -1)
                          or (dvij == -1 and dvik == 1)
                          or (dvij == 2 and dvik == 1)
                          or (dvij == 1 and dvik == 2))

                # Test if a card in the hand goes to flush third

                if lcolor and lsuite:
                    options.append(Option(i, k, Umpire.cote_both * 1.5))

                # Test if a card in the hand goes to 3 of a kind

                if dvij == 0 and dvik == 0:
                    options.append(Option(i, k, Umpire.cote_brelan * 1.5))

                # Test if a card in the hand goes to color

                if lcolor:
                    options.append(Option(i, k, Umpire.cote_couleur))

                # Test if a card in the hand goes to suite

                if lsuite:
                    options.append(Option(i, k, Umpire.cote_suite))

        # 3 Search in the sides with 1 card

        for i in self.statistics.auto_lh():
            for k in self.statistics.auto_ls1():

                dvij = v[i] - self.sides[k].cards.index[0].valeur

                lcolor = (c[i] == self.sides[k].cards.index[0].couleur)
                lsuite = (dvij == -1 or dvij == -2 or dvij == 1 or dvij == 2)

                # Test if a card of the hand matchs for flush third

                if lcolor and lsuite:
                    options.append(Option(i, k, Umpire.cote_both))

                # Test if a card of the hand matchs for 3 of a kind

                if dvij == 0:
                    options.append(Option(i, k, Umpire.cote_brelan / 1.5))

                # Test if a card of the hand matchs for color

                if lcolor:
                    options.append(Option(i, k, Umpire.cote_couleur / 1.5))

                # Test if a card of the hand match for suite

                if lsuite:
                    options.append(Option(i, k, Umpire.cote_suite))

        # Choosing the best combination

        if options:
            c = 0.0
            k = 0
            for i in range(len(options)):
                c = max(c, options[i].cote)
                if c == options[i].cote:
                    k = i

            self.cardManager.set_shift_hand(options[k].hand)
            self.cardManager.set_shift_side(options[k].side)
            return

        # 4 Play a random card on a random free side

        if self.statistics.auto_ls0():
            self.cardManager.set_shift_side(choice(self.statistics.auto_ls0()))
            self.cardManager.set_shift_card(choice(self.hand.cards))
            return

        # 5 Last call...

        self.cervo0()
