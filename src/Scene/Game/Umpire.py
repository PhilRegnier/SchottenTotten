from PyQt5.QtCore import QTimer

from src.Scene.Game.Side import Side
from src.Scene.Game.Stone import Stone
from src.Scene.Starter.Curtain import Curtain
from src.TextInForeground import TextInForeground


class Umpire:

    final_countdown = False

    # cotations for cards combinations

    cote_suite = 100
    cote_couleur = 200
    cote_both = 200
    cote_brelan = 400

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
            side.somme += cls.cote_suite

        # test for flush => somme € [206; 324]

        if side.cards[0].couleur == side.cards[1].couleur == side.cards[2].couleur:
            flush = True
            side.somme += cls.cote_couleur

        # test for straight flush => somme € [506; 524]

        if suite and flush:
            side.somme += cls.cote_both

        # test for three of a kind => somme € [403; 427]

        elif side.cards[0].valeur == side.cards[1].valeur == side.cards[2].valeur:
            side.somme += cls.cote_brelan
    """
    Compare each sides of the stones and test for victory
    """
    def judge(self, player, automaton, stones):

        # if 3 cards have been played on each side, test for claim of the stone

        if self.user_side[side_id].nCard == 3 and self.auto_side[side_id].nCard == 3:
            if self.user_side[side_id].somme > self.auto_side[side_id].somme:
                self.stone[side_id].winner = "user"
                self.stone[side_id].moveStoneTo(side.height + 6 + Stone.height)
            elif self.user_side[side_id].somme < self.auto_side[side_id].somme:
                self.stone[side_id].winner = "auto"
                self.stone[side_id].moveStoneTo(-side.height - 6 - Stone.height)
            else:
                self.stone[side_id].winner = "equal"

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
