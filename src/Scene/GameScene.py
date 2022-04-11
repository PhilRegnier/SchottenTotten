from PyQt5.QtWidgets import QGraphicsScene

from src.Scene.Game.Automaton import Automaton
from src.Scene.Game.Card import Card
from src.Scene.Game.CardManager import CardManager
from src.Scene.Game.Deck import Deck
from src.Scene.Game.Player import Player
from src.Scene.Game.Stone import Stone
from src.Scene.Starter.HomeCurtain import HomeCurtain
from src.Style import Style
from src.variables_globales import mainWindow_width, mainWindow_height, mainWindow_marge, stone_marge, stone_width, \
    stone_height, side_height, marge


class GameScene(QGraphicsScene):

    def __init__(self, parent):
        super().__init__(parent)

        self.setSceneRect(0, 0, mainWindow_width - 40, mainWindow_height - 60)

        # Starter attributes

        self.home = HomeCurtain()
        self.addItem(self.home)
        self.home.setVisible(True)

        # Game attributes

        self.cardManager = CardManager()
        self.deck = Deck(self)
        self.player = Player('humain', Style.user_side_color0, Style.user_side_color1, Style.user_side_pen)
        self.automaton = Automaton('Bot', Style.auto_side_color0, Style.auto_side_color1, Style.auto_side_pen)

        self.stones = [Stone(i) for i in range(9)]

    # Create board game items and set the board scene

    def setup(self):

        # Frontier items

        for i in range(9):
            x = i * stone_marge + i * stone_width + mainWindow_marge
            y = mainWindow_marge + stone_height + stone_marge
            self.automaton.sides[i].setPos(x, y)
            y += side_height + stone_marge
            self.stones[i].setPos(x - 2, y - 2)
            y += stone_height + stone_marge
            self.player.sides[i].setPos(x, y)

        # User's hand cards items

        index = 0
        for card in self.player.hand.cards:
            card.setParentItem(self.player.playmat)
            card.setPos((index + 1) * marge + index * Card.width, marge)
            card.setAnchorPoint(card.pos())
            card.setDraggable(True)
            card.setVisible(True)
            index += 1

        # Computer's hand cards items [CHEAT MODE]

        index = 0
        for card in self.automaton.hand.cards:
            card.setParentItem(self.automaton.playmat)
            card.setPos((index + 1) * marge + index * Card.width, marge)
            card.setAnchorPoint(card.pos())
            card.setVisible(True)
            index += 1

        self.automaton.playmat.setScale(0.6)

        # Set items positions

        bottom_y = mainWindow_height - 5 * mainWindow_marge - Card.height - 2 * marge

        self.deck.set_pos_init(1000, bottom_y)
        self.player.playmat.setPos(10, bottom_y)
        self.automaton.playmat.setPos(400, 10)

        # Game board assembly

        self.board.addItem(self.deck)

        for i in range(9):
            self.board.addItem(self.automaton.sides[i])
            self.board.addItem(self.player.sides[i])
            self.board.addItem(self.stones[i])

        self.board.addItem(self.user_deck)

        # Set zValue max

        MovingCard.reset_zmax()
        for item in self.board.items():
            MovingCard.set_zmax(item.zValue())