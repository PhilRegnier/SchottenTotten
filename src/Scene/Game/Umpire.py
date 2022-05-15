from PyQt5.QtCore import QTimer

from src.Scene.Game.ShiftManager import ShiftManager
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

    """
    Compare each sides of the stones and test for victory
    """
    def judge(self, player, automa, stones):

        # Look where the last card has been moved

        shift_manager = ShiftManager()

        i = shift_manager.side.numero

        if player.sides[i].is_full() and automa.sides[i].is_full():
            stones[i].claim(player.sides[i].somme, automa.sides[i].somme)

        # When the party ends, all stones have to be claimed

        if Umpire.final_countdown:

            for stone in stones:
                if stone.winner is not None:
                    i = stone.numero
                    stone.claim(player.sides[i].somme, automa.sides[i].somme)

            # count stones won

            player_stones_won = 0
            automa_stones_won = 0

            for stone in stones:
                if stone.winner == Stone.WINNER_PLAYER:
                    player_stones_won += 1
                elif stone.winner == Stone.WINNER_AUTOMA:
                    automa_stones_won += 1

        # check if 3 stones are aligned

        player_count = 0
        automa_count = 0
        player_3_stones_in_a_row = False
        automa_3_stones_in_a_row = False
        uw = False
        aw = False

        for i in range(9):
            if stones[i].winner == Stone.WINNER_PLAYER:
                automa_3_stones_in_a_row = False
                acount = 0
                if player_3_stones_in_a_row:
                    ucount += 1
                else:
                    automa_3_stones_in_a_row = True
                    ucount += 1

                if ucount == 3:
                    uw = True

            elif stones[i].winner == Stone.WINNER_AUTOMA:
                player_3_stones_in_a_row = False
                ucount = 0
                if automa_3_stones_in_a_row:
                    acount += 1
                else:
                    automaton_3_stones_in_a_row = True
                    acount += 1

                if acount == 3:
                    aw = True

            else:
                ucount = 0
                acount = 0
                player_3_stones_in_a_row = False
                automa_3_stones_in_a_row = False

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
