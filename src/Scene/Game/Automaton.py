from random import choice

from src.Scene.Game.Card import Card
from src.Scene.Game.CardManager import CardManager
from src.Scene.Game.Option import Option
from src.Scene.Game.Player import Player
from src.Scene.Game.ShiftManager import ShiftManager
from src.Scene.Game.Statistics import Statistics
from src.Scene.Game.Umpire import Umpire
from src.SettingsManager import SettingsManager


class Automaton(Player):

    def __init__(self, name, colors, parent):
        super().__init__(name, colors)
        self.settingsManager = SettingsManager()
        self.cardManager = CardManager()
        self.statistics = Statistics(self.cardManager.colors)
        self.board = parent

    """
    Ask the automaton to play a card on his side
    """
    def play_a_card(self):

        # select an option (card + side)

        if self.settingsManager.get_difficulty() == 1:
            self.cervo1()
        else:
            self.cervo0()

        # move the selected card on the selected side

        shift_manager = ShiftManager()
        shift_manager.card.setVisible(True)

    """
    Automate 0 : random card and random stone
    """
    def cervo0(self):
        shift_manager = ShiftManager()
        shift_manager.set_hand(choice(self.statistics.auto_lh()))
        shift_manager.set_side(choice(self.statistics.auto_ls()))

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
            v[i] = self.playmat.cards[i].valeur
            c[i] = self.playmat.cards[i].couleur

        # 1 Look at the hand

        for i in self.statistics.auto_lh():
            for j in self.statistics.auto_lh():
                if i != j:

                    dvij = v[i] - v[j]

                    # For flush pair(s)

                    if c[i] == c[j] and 3 > dvij > -3:
                        for k in self.statistics.auto_ls1():
                            if c[i] == self.cardManager.cards[self.sides[k].index[0]].couleur:
                                dvik = v[i] - self.cardManager.cards[self.sides[k].index[0]].valeur
                                if (dvij == 2 and dvik == 1) \
                                        or (dvij == -2 and dvik == -1) \
                                        or (dvij == 1 and dvik == 2) \
                                        or (dvij == -1 and dvik == -2):
                                    options.append(Option(i, k, Umpire.COTE_BOTH))

                    # For pair(s)

                    if dvij == 0:
                        for k in self.statistics.auto_ls1():
                            if v[i] == Card.cards[self.sides[k].index[0]].valeur:
                                options.append(Option(i, k, Umpire.COTE_BRELAN))

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
                    options.append(Option(i, k, Umpire.COTE_BOTH * 1.5))

                # Test if a card in the hand goes to 3 of a kind

                if dvij == 0 and dvik == 0:
                    options.append(Option(i, k, Umpire.COTE_BRELAN * 1.5))

                # Test if a card in the hand goes to color

                if lcolor:
                    options.append(Option(i, k, Umpire.COTE_COULEUR))

                # Test if a card in the hand goes to suite

                if lsuite:
                    options.append(Option(i, k, Umpire.COTE_SUITE))

        # 3 Search in the sides with 1 card

        for i in self.statistics.auto_lh():
            for k in self.statistics.auto_ls1():

                dvij = v[i] - self.sides[k].cards.index[0].valeur

                lcolor = (c[i] == self.sides[k].cards.index[0].couleur)
                lsuite = (dvij == -1 or dvij == -2 or dvij == 1 or dvij == 2)

                # Test if a card of the hand matchs for flush third

                if lcolor and lsuite:
                    options.append(Option(i, k, Umpire.COTE_BOTH))

                # Test if a card of the hand matchs for 3 of a kind

                if dvij == 0:
                    options.append(Option(i, k, Umpire.COTE_BRELAN / 1.5))

                # Test if a card of the hand matchs for color

                if lcolor:
                    options.append(Option(i, k, Umpire.COTE_COULEUR / 1.5))

                # Test if a card of the hand match for suite

                if lsuite:
                    options.append(Option(i, k, Umpire.COTE_SUITE))

        # Choosing the best combination

        shift_manager = ShiftManager()

        if options:
            best_option = options[0]
            for option in options:
                if option.cote > best_option.cote:
                    best_option = option

            shift_manager.set_hand(best_option.hand)
            shift_manager.set_side(best_option.side)
            return

        # 4 Play a random card on a random free side

        if self.statistics.auto_ls0():
            shift_manager.set_side(self.sides[choice(self.statistics.auto_ls0())])
            shift_manager.set_card(choice(self.playmat.cards))
            return

        # 5 Last call...

        self.cervo0()
