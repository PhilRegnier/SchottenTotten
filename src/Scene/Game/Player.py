from random import choice

from src.Scene.Game.Option import Option
from src.Scene.Game.Playmat import Playmat
from src.Scene.Game.ShiftManager import ShiftManager
from src.Scene.Game.Side import Side
from src.Scene.Game.Statistics import Statistics
from src.Scene.Game.Umpire import Umpire


class Player:

    def __init__(self, name, colors, accept_hover_event=False):
        self.round_score = 0
        self.total_score = 0
        self.name = name
        self.colors = colors
        self.sides = [
            Side(
                numero=i,
                colors=self.colors,
                hover=accept_hover_event
            )
            for i in range(9)
        ]
        self.playmat = Playmat(self.colors)
        self.shift_manager = ShiftManager()
        self.statistics = Statistics(self.sides)

    def update(self):
        self.statistics.reset_stat_sides(self.sides)
        self.total_score += self.round_score
        self.round_score = 0

    def reset(self):
        self.statistics.reset_stat_sides(self.sides)
        self.round_score = 0
        self.total_score = 0

    """
    Select an option (card + side) depending of level chosen.
    Move the selected card on the selected side.
    Update statistics before (side has really been affected...)
    """
    def choose_card(self, level=0):

        match level:
            case 1:
                self.cervo1()
            case 0:
                self.cervo0()

        self.shift_manager.card.setVisible(True)

        self.statistics.add_card_to_autoside(self.shift_manager.side)

    """
    Automate 0 : chose a random card and a random side
    """
    def cervo0(self):
        self.shift_manager.select(
            choice(self.playmat.cards),
            choice(self.statistics.auto_ls()))

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
                        for side in self.statistics.auto_ls1():
                            if card_i.couleur == side.cards[0].couleur:
                                dvik = card_i.valeur - side.cards[0].valeur
                                if (dvij == 2 and dvik == 1) \
                                        or (dvij == -2 and dvik == -1) \
                                        or (dvij == 1 and dvik == 2) \
                                        or (dvij == -1 and dvik == -2):
                                    options.append(Option(card_i, side, Umpire.COTE_BOTH))

                    # For pair(s)

                    if dvij == 0:
                        for side in self.statistics.auto_ls1():
                            if card_i.valeur == side.cards[0].valeur:
                                options.append(Option(card_i, side, Umpire.COTE_BRELAN))

        # 2 Search into sides with 2 cards

        for card in self.playmat.cards:
            for side in self.statistics.auto_ls2():

                dvij = card.valeur - side.cards[0].valeur
                dvik = card.valeur - side.cards[1].valeur

                lcolor = (card.couleur == side.cards[0].couleur
                          and card.couleur == side.cards[1].couleur)

                lsuite = ((dvij == -1 and dvik == -2)
                          or (dvij == -2 and dvik == -1)
                          or (dvij == 1 and dvik == -1)
                          or (dvij == -1 and dvik == 1)
                          or (dvij == 2 and dvik == 1)
                          or (dvij == 1 and dvik == 2))

                # Test if a card in the hand goes to flush third

                if lcolor and lsuite:
                    options.append(Option(card, side, Umpire.COTE_BOTH * 1.5))

                # Test if a card in the hand goes to 3 of a kind

                if dvij == 0 and dvik == 0:
                    options.append(Option(card, side, Umpire.COTE_BRELAN * 1.5))

                # Test if a card in the hand goes to color

                if lcolor:
                    options.append(Option(card, side, Umpire.COTE_COULEUR))

                # Test if a card in the hand goes to suite

                if lsuite:
                    options.append(Option(card, side, Umpire.COTE_SUITE))

        # 3 Search in the sides with 1 card

        for card in self.playmat.cards:
            for side in self.statistics.auto_ls1():

                dvij = card.valeur - side.cards[0].valeur

                lcolor = (card.couleur == side.cards[0].couleur)
                lsuite = (dvij == -1 or dvij == -2 or dvij == 1 or dvij == 2)

                # Test if a card of the hand matchs for flush third

                if lcolor and lsuite:
                    options.append(Option(card, side, Umpire.COTE_BOTH))

                # Test if a card of the hand matchs for 3 of a kind

                if dvij == 0:
                    options.append(Option(card, side, Umpire.COTE_BRELAN / 1.5))

                # Test if a card of the hand matchs for color

                if lcolor:
                    options.append(Option(card, side, Umpire.COTE_COULEUR / 1.5))

                # Test if a card of the hand match for suite

                if lsuite:
                    options.append(Option(card, side, Umpire.COTE_SUITE))

        # Choosing the best combination

        if options:
            best_option = options[0]
            for option in options:
                if option.cote > best_option.cote:
                    best_option = option

            self.shift_manager.select(best_option.card, best_option.side)
            print("Automaton Best option")
            return

        # 4 Play a random card on a random free side

        if self.statistics.auto_ls0():
            self.shift_manager.select(
                choice(self.playmat.cards),
                choice(self.statistics.auto_ls0()))
            print("Automaton random")
            return

        # 5 Last call...

        self.cervo0()
        print("Automaton cervo0")
