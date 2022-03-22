# class contener for variables managing cards movements between graphics items

class MovingCard:

    __side_id = -1  # to point on the side of the drop
    __card_id = -1  # to point on card dropped
    __hand_id = -1  # to point on the hand's index of the card dragged
    __dragged = False
    __movedToReorganize = False
    __card_hover = -1
    __card_dx = 0.
    __zmax = 0.

    @staticmethod
    def set_zmax(valeur):
        MovingCard.__zmax = max(MovingCard.__zmax, valeur)

    @staticmethod
    def get_zmax():
        return MovingCard.__zmax

    @staticmethod
    def reset_zmax():
        MovingCard.__zmax = 0.

    @staticmethod
    def userDontWantToReorganize():
        MovingCard.__movedToReorganize = False
        MovingCard.__card_hover = -1

    @staticmethod
    def userWantToReorganize():
        MovingCard.__movedToReorganize = True

    @staticmethod
    def isMovedToReorganize():
        return MovingCard.__movedToReorganize

    @staticmethod
    def isDragged():
        return MovingCard.__dragged

    @staticmethod
    def dragged():
        MovingCard.__dragged = True

    @staticmethod
    def unDragged():
        MovingCard.__dragged = False

    @staticmethod
    def set_card_id(id):
        MovingCard.__card_id = id

    @staticmethod
    def card_id():
        return MovingCard.__card_id

    @staticmethod
    def set_hand_id(id):
        MovingCard.__hand_id = id

    @staticmethod
    def hand_id():
        return MovingCard.__hand_id

    @staticmethod
    def set_side_id(id):
        MovingCard.__side_id = id

    @staticmethod
    def side_id():
        return MovingCard.__side_id

