from PyQt5.QtCore import QTimer

from src.Scene.Game import ShiftManager
from src.Scene.Game.Side import Side
from src.Scene.Game.Stone import Stone
from src.Scene.Starter.Curtain import Curtain
from src.TextInForeground import TextInForeground


class Umpire:

    final_countdown = False

    # cotations for cards combinations

    COTE_SUITE = 100
    COTE_COULEUR = 200
    COTE_BOTH = 200
    COTE_BRELAN = 400

    """
    Test the combination after a third card has been played on a side.
    The somme attribute of the side is updated with the corresponding score.
    """
    @classmethod
    def book(cls, side):

        suite = False
        flush = False

        # test for straight =>  somme € [106; 124]

        liste = sorted([side.cards[0].valeur, side.cards[1].valeur, side.cards[2].valeur])

        if liste[1] == liste[0] + 1 and liste[2] == liste[1] + 1:
            suite = True
            side.somme += cls.COTE_SUITE

        # test for flush => somme € [206; 324]

        if side.cards[0].couleur == side.cards[1].couleur == side.cards[2].couleur:
            flush = True
            side.somme += cls.COTE_COULEUR

        # test for straight flush => somme € [506; 524]

        if suite and flush:
            side.somme += cls.COTE_BOTH

        # test for three of a kind => somme € [403; 427]

        elif side.cards[0].valeur == side.cards[1].valeur == side.cards[2].valeur:
            side.somme += cls.COTE_BRELAN

    # if 3 cards have been played on each side, test for claim of the stone

    @staticmethod
    def claim_the_stone(stone, player_side, automaton_side):

        if player_side.is_full() and automaton_side.is_full():
            if player_side.somme > automaton_side.somme:
                stone.winner = "user"
                stone.moveStoneTo(player_side.height + 6 + stone.height)
            elif player_side.somme < automaton_side.somme:
                stone.winner = "auto"
                stone.moveStoneTo(-player_side.height - 6 - stone.height)
            else:
                stone.winner = "equal"

    """
    Compare each sides of the stones and test for victory
    """
    def judge(self, player_side, automaton_side, stone):

        if player_side.is_full() and automaton_side.is_full():
            stone.claim(player_side.somme, automaton_side.somme)

        # party endding

        uss = 0
        aus = 0

        if Umpire.final_countdown:

            # Finish to claim stones

            for i in range(9):
                if not self.stone[i].winner:
                    if self.user_side[i].somme > self.auto_side[i].somme:
                        self.stone[i].winner = "user"
                        self.stone[i].moveStoneTo(Side.height + 6 + Stone.height)
                    elif self.user_side[i].somme < self.auto_side[i].somme:
                        self.stone[i].winner = "auto"
                        self.stone[i].moveStoneTo(-Side.height - 6 - Stone.height)
                    else:
                        self.stone[i].winner = "equal"

            # count stones won

            for i in range(9):
                if self.stone[i].winner == "user":
                    uss += 1
                elif self.stone[i].winner == "auto":
                    aus += 1

        # check if 3 stones are aligned

        ucount = 0
        acount = 0
        ul = False
        al = False
        uw = False
        aw = False

        for i in range(9):
            if self.stone[i].winner == "user":
                al = False
                acount = 0
                if ul:
                    ucount += 1
                else:
                    ul = True
                    ucount += 1

                if ucount == 3:
                    uw = True

            elif self.stone[i].winner == "auto":
                ul = False
                ucount = 0
                if al:
                    acount += 1
                else:
                    al = True
                    acount += 1

                if acount == 3:
                    aw = True

            else:
                ucount = 0
                acount = 0
                ul = False
                al = False

        if uw and not aw:
            self.victory("user")
        elif aw and not uw:
            self.victory("auto")
        elif self.ending:
            if uss > aus:
                self.victory("you")
            elif uss < aus:
                self.victory("auto")
            else:
                self.victory("draw")

    # show the endround/endgame's message

    def victory(self, winner):

        # test who won

        if winner == "draw":
            text = "DRAW !!\n\nRESTARTING THE ROUND"
            self.current_round -= 1
        elif winner == "user":
            text = "YOU WON ROUND " + str(self.current_round) + " !!!"
            self.user_score += 1
        else:
            text = "AUTOMA WON ROUND " + str(self.current_round) + " !!!"
            self.auto_score += 1

        if self.current_round < self.settings_manager.get_rounds_nb():
            text += "ROUND " + str(self.current_round) + " !!!"
        else:
            if self.user_score > self.auto_score:
                text = "CONGRATS !\n YOU WON THIS GAME !!!"
            else:
                text = "SO CLOSE !\n COME ON, LOSER, TRY AGAIN !"

        # Prepare the curtain

        self.frame = Curtain()

        # Set the congrats text

        self.msg = TextInForeground(text, self.frame)

        self.board.addItem(self.frame)

        self.frame.setVisible(True)
        self.frame.animate_incoming()

        for i in range(Card.total_cards):
            Card.cards[i].setDraggable(False)
            Card.cards[i].setZValue(0)

        QTimer.singleShot(3000, self.__new_round)
