from src.Scene.Game.ShiftManager import ShiftManager


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

        # Look where the last card has been moved to eventually claim the stone and count it

        shift_manager = ShiftManager()

        i = shift_manager.side.numero

        if player.sides[i].is_full() and automa.sides[i].is_full():
            stones[i].claim(player, automa)
            stones[i].winner.round_score += 1

        # When the party ends (no more cards to play), all stones have to be claimed

        if Umpire.final_countdown:
            for stone in stones:
                if stone.winner is not None:
                    i = stone.numero
                    stone.claim(player, automa)
                    stone.winner.round_score += 1

        # check if there are 3 stones aligned on one side

        player_3_in_a_row = 0
        automa_3_in_a_row = 0

        for i in range(9):
            if stones[i].winner == player:
                automa_3_in_a_row = 0
                player_3_in_a_row += 1
                if player_3_in_a_row == 3:
                    break

            elif stones[i].winner == automa:
                player_3_in_a_row = 0
                automa_3_in_a_row += 1
                if automa_3_in_a_row == 3:
                    break

            else:
                player_3_in_a_row = 0
                automa_3_in_a_row = 0

        # check if anyone wins and score

        if player_3_in_a_row == 3:
            player.round_score = 5
            return player
        elif automa_3_in_a_row == 3:
            automa.round_score = 5
            return automa
        elif player.round_score >= 5:
            return player
        elif automa.round_score >= 5:
            return automa

        return None

