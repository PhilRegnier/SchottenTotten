from random import choice

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
        self.statistics = Statistics()
        self.shift_manager = ShiftManager()
        self.board = parent

    """
    Ask the automaton to play a card on his side
    """
    def play_a_card(self):

        settings_manager = SettingsManager()

        # select an option (card + side)

        if settings_manager.get_difficulty() == 1:
            self.cervo1()
        else:
            self.cervo0()

        # move the selected card on the selected side

        self.shift_manager.card.setVisible(True)

        # update statistics before (side has really been affected...)

        self.statistics.add_card_to_autoside(self.shift_manager.side)

    """
    updates statistics after treatment in gameScene (side has been updated overthere
    """
    def update_statistics(self):
        self.statistics.remove_from_playmat(self.shift_manager.playmat_index)

    """
    Automate 0 : random card and random side
    """
    def cervo0(self):
        self.shift_manager.set_playmat_index(choice(self.statistics.auto_lh()))
        self.shift_manager.set_side(choice(self.statistics.auto_ls()))

    """
    Automate 1 :    search the best option considering the automaton's cards
                    in his hand and in his sides 
    """
    def cervo1(self):

        print("lh:", self.statistics.auto_lh())
        print("ls0: ", self.statistics.auto_ls0())
        for card in self.playmat.cards:
            print("playmat cards: ", card.index)

        # Settings for memorization of relevant combinations

        options = []

        # Set cards color and valor in lists

        v = [0 for _ in range(6)]
        c = ["0" for _ in range(6)]

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
                            if c[i] == self.sides[k].cards[0].couleur:
                                dvik = v[i] - self.sides[k].cards[0].valeur
                                if (dvij == 2 and dvik == 1) \
                                        or (dvij == -2 and dvik == -1) \
                                        or (dvij == 1 and dvik == 2) \
                                        or (dvij == -1 and dvik == -2):
                                    options.append(Option(i, k, Umpire.COTE_BOTH))

                    # For pair(s)

                    if dvij == 0:
                        for k in self.statistics.auto_ls1():
                            if v[i] == self.sides[k].cards[0].valeur:
                                options.append(Option(i, k, Umpire.COTE_BRELAN))

        # 2 Search into sides with 2 cards

        for i in self.statistics.auto_lh():
            for k in self.statistics.auto_ls2():

                dvij = v[i] - self.sides[k].cards[0].valeur
                dvik = v[i] - self.sides[k].cards[1].valeur

                lcolor = (c[i] == self.sides[k].cards[0].couleur
                          and c[i] == self.sides[k].cards[1].couleur)

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

                dvij = v[i] - self.sides[k].cards[0].valeur

                lcolor = (c[i] == self.sides[k].cards[0].couleur)
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

        if options:
            best_option = options[0]
            for option in options:
                if option.cote > best_option.cote:
                    best_option = option

            self.shift_manager.select(
                self.playmat.cards[best_option.playmat_index],
                self.sides[best_option.side],
                best_option.playmat_index)
            print("Automaton Best option")
            return

        # 4 Play a random card on a random free side

        if self.statistics.auto_ls0():
            index = choice(self.statistics.auto_lh())
            self.shift_manager.select(
                self.playmat.cards[index],
                self.sides[choice(self.statistics.auto_ls0())],
                index)
            print("Automaton random")
            return

        # 5 Last call...

        self.cervo0()
        print("Automaton cervo0")

