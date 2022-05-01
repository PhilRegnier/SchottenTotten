from math import sqrt

from PyQt5.QtWidgets import QGraphicsScene

from src.Scene.Game.Automaton import Automaton
from src.Scene.Game.Card import Card
from src.Scene.Game.CardManager import CardManager
from src.Scene.Game.Deck import Deck
from src.Scene.Game.Player import Player
from src.Scene.Game.ShiftManager import ShiftManager
from src.Scene.Game.Side import Side
from src.Scene.Game.Stone import Stone
from src.Scene.Game.Umpire import Umpire
from src.Scene.Starter.HomeCurtain import HomeCurtain
from src.SettingsManager import SettingsManager
from src.Style import GeometryStyle, PlayerColors, AutomatonColors


class GameScene(QGraphicsScene):

    width = 0
    height = 0
    marge = 5

    def __init__(self):
        super().__init__()

        # Game attributes

        # TODO : Maybe the initialization occuring before settings change could be a problem

        self.stones = [Stone(i) for i in range(9)]
        self.cardManager = CardManager()
        self.cardManager.initialize()
        self.deck = Deck()
        self.player = Player('humain', PlayerColors)
        self.automaton = Automaton('Bot', AutomatonColors, self)
        self.umpire = Umpire()
        self.current_round = 1

        self.new_order = []
        self.itemsSelected = []

        # set the required width and height to the scene

        GameScene.set_size()

        # Starter attributes

        # TODO : send width and height of the scene to curtains...

        self.home = HomeCurtain()
        self.addItem(self.home)
        self.home.setVisible(True)

        self.setSceneRect(0, 0, GameScene.width, GameScene.height)

    # Create board game items and set the board scene

    def setup(self):

        settings_manager = SettingsManager()

        # Frontier items

        for i in range(9):
            x = i * Stone.marge + i * Stone.width + GeometryStyle.main_marge
            y = GeometryStyle.main_marge + Stone.height + Stone.marge
            self.automaton.sides[i].setPos(x, y)
            y += Side.height + Stone.marge
            self.stones[i].setPos(x - 2, y - 2)
            y += Stone.height + Stone.marge
            self.player.sides[i].setPos(x, y)

        # User's hand cards items

        index = 0
        for card in self.player.hand.cards:
            card.setParentItem(self.player.playmat)
            card.setPos((index + 1) * GeometryStyle.main_marge + index * Card.width, GeometryStyle.main_marge)
            card.setAnchorPoint(card.pos())
            card.setDraggable(True)
            card.setVisible(True)
            index += 1

        # Computer's hand cards items [CHEAT MODE]

        index = 0
        for card in self.automaton.hand.cards:
            card.setParentItem(self.automaton.playmat)
            card.setPos((index + 1) * GeometryStyle.main_marge + index * Card.width, GeometryStyle.main_marge)
            card.setAnchorPoint(card.pos())
            card.setVisible(True)
            index += 1

        self.automaton.playmat.setScale(0.6)

        # Set items positions

        bottom_y = GameScene.height - 5 * GeometryStyle.main_marge - Card.height() - 2 * GeometryStyle.main_marge

        self.deck.set_pos_init(1000, bottom_y)
        self.player.playmat.setPos(10, bottom_y)
        self.automaton.playmat.setPos(400, 10)

        # Game board assembly

        self.addItem(self.deck)

        for i in range(9):
            self.addItem(self.automaton.sides[i])
            self.addItem(self.player.sides[i])
            self.addItem(self.stones[i])

        self.addItem(self.player.playmat)

        # Set zValue max

        self.cardManager.reset_zmax()
        for item in self.items():
            self.cardManager.set_zmax(item.zValue())

        # Create players' hands

        for i in range(settings_manager.get_max_cards_in_hand()):
            self.player.hand.add(self.deck.draw())
            self.automaton.hand.add(self.deck.draw())

    def __new_round(self):

        settings_manager = SettingsManager()

        # ending the game

        if self.current_round == settings_manager.get_number_of_rounds():
            self.home.setVisible(True)
            self.home.animate_incoming()
            return

        # starting the game

        self.current_round += 1

        # Switch the first player between each round

        if self.current_round > 1:
            settings_manager.switch_first_player()

        # Set the board

        self._setup_hands()
        self.setup()
        self.umpire.final_countdown = False

    def mouseMoveEvent(self, event):
        #print("gamescene: mouseMove")
        shift_manager = ShiftManager()

        if shift_manager.dragged:

            # Enlightment for user's side hovered. TODO : => treatement in Side class ?

            items = self.items(event.pos())

            for item in items:
                if isinstance(item, Side) and item.parentItem == self.player:
                    if len(item.cards) < 3:
                        item.light_on()
                        self.itemsSelected.append(item)

            for item in self.itemsSelected:
                if item not in items:
                    item.light_off()
                    self.itemsSelected.remove(item)

        else:
            QGraphicsScene.mouseMoveEvent(self, event)

            # TODO : Management for reordering the user's hand

            # self.mouseMoveHand()

    # Reorganization of the user's hand
    """
    def mouseMoveHand(self):
        self.cardManager.user_dont_want_to_reorganize()

        col_items = self.cardManager.shift_card.collidingItems()

        if col_items:
            shortest_dist = 100000.
            for item in col_items:

                if item == self.cardManager.shift_card.parentItem():
                    continue

                if item.parentItem() == self.cardManager.shift_card.parentItem():
                    line = QLineF(item.sceneBoundingRect().center(),
                                  self.cardManager.shift_card.sceneBoundingRect().center())
                    if line.length() < shortest_dist:
                        shortest_dist = line.length()
                        # if card_hover != item.numero or card_dx*line.dx() < 0:
                        self.cardManager.user_want_to_reorganize()

                        card_dx = line.dx()
                        card_hover = item
        
        if self.cardManager.is_moved_to_reorganize():
            self.new_order = self.user_hand
        else:
            return
        
        # Set the concerned cards

        if self.cardManager.shift_card.index - card_hover.index < 0:
            i1 = self.cardManager.shift_card.index + 1
            i2 = card_hover.index
            sens = -1
            if card_dx > 0:
                i2 += 1
        else:
            i1 = card_hover.index
            i2 = self.cardManager.shift_card.index
            sens = 1
            if card_dx > 0:
                i1 += 1

        # reconstruct the hand

        # Set the animation moving concerned cards

        animations = QParallelAnimationGroup()

        for i in range(i1, i2):
            animation = QPropertyAnimation(self.player.hand[i]], b"pos")
            pos1 = Card.cards[self.user_hand[i]].anchorPoint
            pos2 = Card.cards[self.user_hand[i + sens]].anchorPoint
            dx = pos1.x() - pos2.x()
            dy = pos1.y() - pos2.y()
            duration = sqrt(dx ** 2 + dy ** 2) / 1
            animation.setDuration(duration)
            animation.setStartValue(pos1)
            animation.setEndValue(pos2)
            animations.addAnimation(animation)
            self.new_order[i + sens] = self.user_hand[i]

        animations.start()
    """
    def mouseReleaseEvent(self, event):
        print("gamescene: mouseRelease")

        # start the game

        if self.home.starting_button.selected and self.home.starting_button.handled:
            self.home.starting_button.unselect()
            self.__new_round()
            return

        # Events from Cards: If cards has been moved to a droppable zone

        shift_manager = ShiftManager()

        if shift_manager.dragged:

            # Card moved on user's deck
            """
            if self.cardManager.is_moved_to_reorganize():
                self.user_hand = self.new_order
            """
            # Card moved on side ? TODO : => a part of this treatment in Side class ?

            if shift_manager.side is not None:

                # Memorize initial position for new card from the deck

                pos = shift_manager.card.anchor_point

                # Add the card dropped to the side

                shift_manager.side.add_card(shift_manager.card)
                shift_manager.side.light_off()

                # Draw a new card

                if self.deck.is_empty():
                    self.player.hand.lose_a_card()
                    if self.player.hand.is_empty():
                        self.umpire.final_countdown = True
                else:
                    new_card = self.deck.draw()
                    self.player.hand.add(new_card)
                    new_card.setAnchorPoint(pos)
                    new_card.moveTo(self.deck.pos() - self.player.playmat.pos(), pos)

                # Actions if the targetted side is full

                if shift_manager.side.is_full():
                    self.umpire.book(shift_manager.side)

                self.umpire.judge(shift_manager.side)

                shift_manager.reset()

                # Run automate's turn

                self.automaton.play_a_card()

                if shift_manager.side.is_full():
                    self.umpire.book(shift_manager.side)

                self.umpire.judge(shift_manager.side)

            else:
                shift_manager.card.moveTo(shift_manager.card.pos(), shift_manager.card.anchorPoint)

            shift_manager.reset()
            self.update()
            return

        else:
            QGraphicsScene.mouseReleaseEvent(self, event)

    """
     Calcul the height knowing the width needed to show the scene
     without scrolling
    """
    @classmethod
    def set_size(cls):
        cls.width = GeometryStyle.main_width - 40
        cls.height = int(
            4 * Stone.height + 4.33 * Card.height
            + cls.marge * 2 + 8 * GeometryStyle.pen_width + 4 * Stone.marge + 40
        ) - 60

    """
     cheat mode: show automaton's hand in a subwindow
    """
    def show_automaton_hand_view(self):
        self.board.addItem(self.auto_deck)

    def hide_automaton_hand_view(self):
        self.board.removeItem(self.auto_deck)
