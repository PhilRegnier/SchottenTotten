# class contener for variables managing cards movements between graphics items


class MovingCard:

    __card_hover = -1
    __card_dx = 0.
    __zmax = 0.

    def __init__(self, instance, side, hand):
        self.instance = instance
        self.side = side
        self.hand = hand
        self.__movedToReorganize = False
        self.__dragged = False

    @classmethod
    def set_zmax(valeur):
        MovingCard.__zmax = max(MovingCard.__zmax, valeur)

    @classmethod
    def get_zmax():
        return MovingCard.__zmax

    @classmethod
    def reset_zmax():
        MovingCard.__zmax = 0.

    def userDontWantToReorganize():
        MovingCard.__movedToReorganize = False
        MovingCard.__card_hover = -1

    def userWantToReorganize():
        MovingCard.__movedToReorganize = True

    def isMovedToReorganize():
        return MovingCard.__movedToReorganize

    def isDragged():
        return MovingCard.__dragged

    def dragged():
        MovingCard.__dragged = True

    def undragged():
        MovingCard.__dragged = False

    def set_card_id(id):
        MovingCard.__card_id = id

    def card_id():
        return MovingCard.__card_id

    def set_hand_id(id):
        MovingCard.__hand_id = id

    def hand_id():
        return MovingCard.__hand_id

    def set_side_id(id):
        MovingCard.__side_id = id

    def side_id():
        return MovingCard.__side_id

