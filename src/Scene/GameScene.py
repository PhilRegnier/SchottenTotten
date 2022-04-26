from math import sqrt

from PyQt5.QtCore import QParallelAnimationGroup, QPropertyAnimation, QLineF, QTimer
from PyQt5.QtWidgets import QGraphicsScene

from src.MainWindow.GameWindow import GameWindow
from src.Scene.Game.Automaton import Automaton
from src.Scene.Game.Card import Card
from src.Scene.Game.CardManager import CardManager
from src.Scene.Game.Deck import Deck
from src.Scene.Game.Player import Player
from src.Scene.Game.Side import Side
from src.Scene.Game.Stone import Stone
from src.Scene.Starter.ChifoumiCurtain import Chifoumi
from src.Scene.Starter.HomeCurtain import HomeCurtain
from src.TextInForeground import TextInForeground


class GameScene(QGraphicsScene):

    def __init__(self, parent):
        super().__init__(parent)

        self.setSceneRect(0, 0, GameWindow.width - 40, GameWindow.height() - 60)

        # Starter attributes

        self.home = HomeCurtain()
        self.addItem(self.home)
        self.home.setVisible(True)

        # Game attributes

        # TODO : test if initialization occured before settings could be changed...

        self.cardManager = CardManager()
        self.deck = Deck(self)
        self.player = Player('humain')
        self.automaton = Automaton('Bot')

        self.stones = [Stone(i) for i in range(9)]

        self.new_order = []

    # Create board game items and set the board scene

    def setup(self):

        # Frontier items

        for i in range(9):
            x = i * Stone.marge + i * Stone.width + GameWindow.marge
            y = GameWindow.marge + Stone.height + Stone.marge
            self.automaton.sides[i].setPos(x, y)
            y += Side.height + Stone.marge
            self.stones[i].setPos(x - 2, y - 2)
            y += Stone.height + Stone.marge
            self.player.sides[i].setPos(x, y)

        # User's hand cards items

        index = 0
        for card in self.player.hand.cards:
            card.setParentItem(self.player.playmat)
            card.setPos((index + 1) * GameWindow.marge + index * Card.width, GameWindow.marge)
            card.setAnchorPoint(card.pos())
            card.setDraggable(True)
            card.setVisible(True)
            index += 1

        # Computer's hand cards items [CHEAT MODE]

        index = 0
        for card in self.automaton.hand.cards:
            card.setParentItem(self.automaton.playmat)
            card.setPos((index + 1) * GameWindow.marge + index * Card.width, GameWindow.marge)
            card.setAnchorPoint(card.pos())
            card.setVisible(True)
            index += 1

        self.automaton.playmat.setScale(0.6)

        # Set items positions

        bottom_y = GameWindow.get_height() - 5 * GameWindow.marge - Card.height - 2 * GameWindow.marge

        self.deck.set_pos_init(1000, bottom_y)
        self.player.playmat.setPos(10, bottom_y)
        self.automaton.playmat.setPos(400, 10)

        # Game board assembly

        self.addItem(self.deck)

        for i in range(9):
            self.addItem(self.automaton.sides[i])
            self.addItem(self.player.sides[i])
            self.addItem(self.stones[i])

        self.addItem(self.user_deck)

        # Set zValue max

        self.cardManager.reset_zmax()
        for item in self.items():
            self.cardManager.set_zmax(item.zValue())

        # Create players' hands

        for i in range(self.settings_manager.get_max_cards_in_hand()):
            self.player.hand.add(self.deck.draw())
            self.automaton.hand.add(self.deck.draw())

    def __new_round(self):

        # ending the game

        if self.current_round == self.settings.get_number_of_rounds():
            self.home.setVisible(True)
            self.home.animate_incoming()
            return

        # starting the game

        self.current_round += 1

        # Switch the first player between each round

        if self.current_round > 1:
            self.settings_manager.switch_first_player()

        # Set the board

        self._setup_hands()
        self.setup()

        self.ending = False

    def mouseMoveEvent(self, event):

        if Card.isDragged():

            # Enlightment for user's side hovered

            items = self.items(event.pos())

            for item in items:
                if isinstance(item, Side) && item.parentItem == self.player:
                    if item.nCard < 3:
                        item.setOpacity(1)
                        self.itemsSelected.append(item)

            for item in self.itemsSelected:
                if item not in items:
                    item.setOpacity(0.5)

            # Management for reordering the user's hand

            # self.mouseMoveHand()

    # Reorganization of the user's hand

    def mouseMoveHand(self):
        self.cardManager.UserDontWantToReorganize()

        col_items = Card.cards[self.cardManager.card_id].collidingItems()

        if col_items:
            shortest_dist = 100000.
            for item in col_items:

                if item == Card.cards[self.cardManager.card_id].parentItem():
                    continue

                if item.parentItem() == Card.cards[self.cardManager.card_id].parentItem():
                    line = QLineF(item.sceneBoundingRect().center(),
                                  Card.cards[self.cardManager.card_id].sceneBoundingRect().center())
                    if line.length() < shortest_dist:
                        shortest_dist = line.length()
                        # if card_hover != item.numero or card_dx*line.dx() < 0:
                        self.cardManager.userWantToReorganize()

                        card_dx = line.dx()
                        card_hover = item.numero

        if self.cardManager.isMovedToReorganize():
            self.new_order = self.user_hand
        else:
            return

        # Set the concerned cards

        if Card.cards[self.cardManager.card_id].index - Card.cards[card_hover].index < 0:
            i1 = Card.cards[self.cardManager.card_id].index + 1
            i2 = Card.cards[card_hover].index
            sens = -1
            if card_dx > 0:
                i2 += 1
        else:
            i1 = Card.cards[card_hover].index
            i2 = Card.cards[self.cardManager.card_id].index
            sens = 1
            if card_dx > 0:
                i1 += 1

                # Set the animation moving concerned cards

        self.anims = QParallelAnimationGroup()

        for i in range(i1, i2):
            anim = QPropertyAnimation(Card.cards[self.user_hand[i]], b"pos")
            pos1 = Card.cards[self.user_hand[i]].anchorPoint
            pos2 = Card.cards[self.user_hand[i + sens]].anchorPoint
            dx = pos1.x() - pos2.x()
            dy = pos1.y() - pos2.y()
            duration = sqrt(dx ** 2 + dy ** 2) / 1
            anim.setDuration(duration)
            anim.setStartValue(pos1)
            anim.setEndValue(pos2)
            self.anims.addAnimation(anim)
            self.new_order[i + sens] = self.user_hand[i]

        self.anims.start()

    def mouseReleaseEvent(self, event):

        # QGraphicsView.mouseReleaseEvent(self, event)

        # Events from Cards: If cards has been moved to a droppable zone

        if self.cardManager.isDragged():

            # Card moved on user's deck

            if self.cardManager.isMovedToReorganize():
                self.user_hand = self.new_order

            # Card moved on side or no ?

            side_id = self.cardManager.side_id()

            if side_id >= 0:

                # position in the hand

                i = Card.cards[self.cardManager.card_id()].index

                # Memorize initial position for new card from the deck

                pos = Card.cards[self.cardManager.card_id()].anchorPoint

                # Add the card drop to the side

                self.user_side[side_id].addCard(self.cardManager.card_id)
                self.user_side[side_id].setOpacity(0.5)

                # Draw a new card

                if self.deck.is_empty():
                    self.user_hand[i] = -1
                    if sum(self.user_hand) == -6:
                        self.ending = True
                else:
                    self.user_hand[i] = self.deck.draw()
                    Card.cards[self.user_hand[i]].setVisible(True)
                    Card.cards[self.user_hand[i]].setDraggable(True)
                    Card.cards[self.user_hand[i]].setAnchorPoint(pos)
                    Card.cards[self.user_hand[i]].moveTo(self.deck.pos() - self.user_deck.pos(), pos)
                    Card.cards[self.user_hand[i]].setParentItem(self.user_deck)
                    Card.cards[self.user_hand[i]].setIndex(i)

                # Actions if the side is full

                if self.user_side[side_id].nCard == 3:
                    self.book(self.user_side[side_id])

                self.judge(side_id)

                self.cardManager.set_side_id(-1)
                self.cardManager.set_card_id(-1)

                # Run automate's turn

                self.automate()

                if self.auto_side[side_nb].nCard == 3:
                    self.auto_side[side_nb].droppable = False
                    self.book(self.auto_side[side_nb])

                self.judge(side_id)

                self.cardManager.set_side_id(-1)
                self.cardManager.set_card_id(-1)
            else:
                Card.cards[self.cardManager.card_id].moveTo(Card.cards[self.cardManager.card_id].pos(),
                                                      Card.cards[self.cardManager.card_id].anchorPoint)

            dragged = False
            self.update()
            return

        # Global switch on events from ...

        global clicked, selected

        if clicked and selected >= 0:

            # ... Home

            if selected == 10:
                self.home.openSettings()

            if selected == 11:
                self.chifoumi = Chifoumi()
                self.board.addItem(self.chifoumi)
                self.chifoumi.animate_incoming()
                self.chifoumi.start()

            # ... Chifoumi

            if selected < 3:
                self.chifoumi.choosePlayer()

                if self.settings_manager.get_first_player() == -1:
                    self.chifoumi.restart()
                else:
                    if self.settings_manager.get_first_player() == 0:
                        self.text = TextInForeground("YOU ARE FIRST PLAYER !!", self.chifoumi)
                    else:
                        self.text = TextInForeground("AUTOMATE IS FIRST PLAYER !!", self.chifoumi)

                    self.text.setVisible(True)
                    self.chifoumi.freeze()
                    QTimer.singleShot(3000, self.letsGo)

            # ... Settings

            if selected == 20:
                self.home.setValues()

            if selected == 21:
                self.home.closeSettings()

            clicked = False
            selected = -1

    # Leave chifoumi curtain and launch the game

    def letsGo(self):
        self.text.setVisible(False)
        self.chifoumi.animate_leaving()
        self.home.animate_leaving()
        self.__new_round()

    # cheat mode: show automaton's hand in a subwindow

    def show_automaton_hand_view(self):
        self.board.addItem(self.auto_deck)

    def hide_automaton_hand_view(self):
        self.board.removeItem(self.auto_deck)
