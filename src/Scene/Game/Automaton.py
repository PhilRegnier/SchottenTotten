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
        card = choice(self.playmat.cards)
        self.shift_manager.select(
            card,
            self.sides[choice(self.statistics.auto_ls())],
            card.index)

    """
    Automate 1 :    search the best option considering the automaton's cards
                    in his hand and in his sides 
    """
    def cervo1(self):

        # Settings for memorization of relevant combinations

        options = []

        # 1 Look at the hand

        for card_i in self.playmat.cards:
            for card_j in self.playmat.cards:
                if card_i != card_j:

                    dvij = card_i.valeur - card_j.valeur

                    # For flush pair(s)

                    if card_i.couleur == card_j.couleur and 3 > dvij > -3:
                        for k in self.statistics.auto_ls1():
                            if card_i.couleur == self.sides[k].cards[0].couleur:
                                dvik = card_i.valeur - self.sides[k].cards[0].valeur
                                if (dvij == 2 and dvik == 1) \
                                        or (dvij == -2 and dvik == -1) \
                                        or (dvij == 1 and dvik == 2) \
                                        or (dvij == -1 and dvik == -2):
                                    options.append(Option(card_i.index, k, Umpire.COTE_BOTH))

                    # For pair(s)

                    if dvij == 0:
                        for k in self.statistics.auto_ls1():
                            if card_i.valeur == self.sides[k].cards[0].valeur:
                                options.append(Option(card_i.index, k, Umpire.COTE_BRELAN))

        # 2 Search into sides with 2 cards

        for card in self.playmat.cards:
            for k in self.statistics.auto_ls2():

                dvij = card.valeur - self.sides[k].cards[0].valeur
                dvik = card.valeur - self.sides[k].cards[1].valeur

                lcolor = (card.couleur == self.sides[k].cards[0].couleur
                          and card.couleur == self.sides[k].cards[1].couleur)

                lsuite = ((dvij == -1 and dvik == -2)
                          or (dvij == -2 and dvik == -1)
                          or (dvij == 1 and dvik == -1)
                          or (dvij == -1 and dvik == 1)
                          or (dvij == 2 and dvik == 1)
                          or (dvij == 1 and dvik == 2))

                # Test if a card in the hand goes to flush third

                if lcolor and lsuite:
                    options.append(Option(card.index, k, Umpire.COTE_BOTH * 1.5))

                # Test if a card in the hand goes to 3 of a kind

                if dvij == 0 and dvik == 0:
                    options.append(Option(card.index, k, Umpire.COTE_BRELAN * 1.5))

                # Test if a card in the hand goes to color

                if lcolor:
                    options.append(Option(card.index, k, Umpire.COTE_COULEUR))

                # Test if a card in the hand goes to suite

                if lsuite:
                    options.append(Option(card.index, k, Umpire.COTE_SUITE))

        # 3 Search in the sides with 1 card

        for card in self.playmat.cards:
            for k in self.statistics.auto_ls1():

                dvij = card.valeur - self.sides[k].cards[0].valeur

                lcolor = (card.couleur == self.sides[k].cards[0].couleur)
                lsuite = (dvij == -1 or dvij == -2 or dvij == 1 or dvij == 2)

                # Test if a card of the hand matchs for flush third

                if lcolor and lsuite:
                    options.append(Option(card.index, k, Umpire.COTE_BOTH))

                # Test if a card of the hand matchs for 3 of a kind

                if dvij == 0:
                    options.append(Option(card.index, k, Umpire.COTE_BRELAN / 1.5))

                # Test if a card of the hand matchs for color

                if lcolor:
                    options.append(Option(card.index, k, Umpire.COTE_COULEUR / 1.5))

                # Test if a card of the hand match for suite

                if lsuite:
                    options.append(Option(card.index, k, Umpire.COTE_SUITE))

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

