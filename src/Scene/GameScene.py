from PyQt5.QtWidgets import QGraphicsScene

from src.variables_globales import mainWindow_width, mainWindow_height


class GameScene(QGraphicsScene):

    def __init__(self, parent):
        super().__init__(parent)

        self.setSceneRect(0, 0, mainWindow_width - 40, mainWindow_height - 60)

    def setup(self):
        """
        Create board game items and set the board scene
        """

        # Frontier items

        self.stone = [Stone(i) for i in range(9)]
        self.user_side = [UserSide(i) for i in range(9)]

        for i in range(9):
            x = i * stone_marge + i * stone_width + mainWindow_marge
            y = mainWindow_marge + stone_height + stone_marge
            self.auto_side[i].setPos(x, y)
            y += side_height + stone_marge
            self.stone[i].setPos(x - 2, y - 2)
            y += stone_height + stone_marge
            self.user_side[i].setPos(x, y)

        # User's hand cards items

        self.user_deck = PlayerDeck(Style.user_side_color0, Style.user_side_color1, Style.user_side_pen)

        for i in range(Settings.get_hand_nb()):
            Card.cards[self.user_hand.get(i)].setParentItem(self.user_deck)
            Card.cards[self.user_hand.get(i)].setPos((i + 1) * marge + i * Card.width, marge)
            Card.cards[self.user_hand.get(i)].setAnchorPoint(Card.cards[self.user_hand[i]].pos())
            Card.cards[self.user_hand[i]].setDraggable(True)
            Card.cards[self.user_hand[i]].setVisible(True)
            Card.cards[self.user_hand[i]].setIndex(i)

        # Computer's hand cards items [CHEAT MODE]

        self.auto_deck = PlayerDeck(Style.auto_side_color0, Style.auto_side_color1, Style.auto_side_pen)

        for i in range(Settings.get_hand_nb()):
            Card.cards[self.auto_hand[i]].setParentItem(self.auto_deck)
            Card.cards[self.auto_hand[i]].setPos((i + 1) * marge + i * Card.width, marge)
            Card.cards[self.auto_hand[i]].setAnchorPoint(Card.cards[self.auto_hand[i]].pos())
            Card.cards[self.auto_hand[i]].setVisible(True)

        self.auto_deck.setScale(0.6)

        # Set items positions

        bottom_y = mainWindow_height - 5 * mainWindow_marge - Card.height - 2 * marge

        self.deck.set_pos_init(1000, bottom_y)
        self.user_deck.setPos(10, bottom_y)
        self.auto_deck.setPos(400, 10)

        # Game board assembly

        self.board.addItem(self.deck)

        for i in range(9):
            self.board.addItem(self.auto_side[i])
            self.board.addItem(self.user_side[i])
            self.board.addItem(self.stone[i])

        self.board.addItem(self.user_deck)

        # Set zValue max

        MovingCard.reset_zmax()
        for item in self.board.items():
            MovingCard.set_zmax(item.zValue())