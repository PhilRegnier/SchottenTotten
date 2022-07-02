
from PyQt6.QtCore import QTimer, QLineF
from PyQt6.QtWidgets import QGraphicsScene

from src.Scene.Game.Card import Card
from src.Scene.Game.CardManager import CardManager
from src.Scene.Game.displays.Counter import Counter
from src.Scene.Game.Deck import Deck
from src.Scene.Game.displays.Display import Display
from src.Scene.Game.Player import Player
from src.Scene.Game.displays.Scorer import Scorer
from src.Scene.Game.ShiftManager import ShiftManager
from src.Scene.Game.Side import Side
from src.Scene.Game.Stone import Stone
from src.Scene.Game.Umpire import Umpire
from src.Scene.Curtain import Curtain
from src.Scene.Game.displays.Timer import Timer
from src.Scene.Starter.HomeCurtain import HomeCurtain
from src.SettingsManager import SettingsManager
from src.Style import MainGeometry, PlayerColors, AutomatonColors
from src.TextInForeground import TextInForeground


class GameScene(QGraphicsScene):

    width = 0
    height = 0
    marge = 5

    def __init__(self):
        super().__init__()

        # Game attributes

        # TODO : Maybe the initialization occuring before settings change could be a problem

        self.stones = [Stone(i) for i in range(9)]
        self.card_manager = CardManager()
        self.card_manager.initialize()
        self.deck = Deck()
        self.player = Player('Human', PlayerColors, True)
        self.automaton = Player('Bot', AutomatonColors, False)
        self.umpire = Umpire()
        self.current_round = 0

        self.new_order = []
        self.itemsSelected = []
        self.shift_manager = ShiftManager()
        self.settings_manager = SettingsManager()

        # Add game board items

        self.addItem(self.deck)

        for i in range(9):
            self.addItem(self.automaton.sides[i])
            self.addItem(self.player.sides[i])
            self.addItem(self.stones[i])

        self.addItem(self.player.playmat)

        # Add game managers : counter, scorer and timer

        self.counter = Counter()
        self.addItem(self.counter)

        self.scorer = Scorer(self.player.name, self.automaton.name)
        self.addItem(self.scorer)

        self.timer = Timer(self.time_out)
        self.addItem(self.timer)

        # set the required width and height to the scene

        GameScene.set_size()

        # Position managers

        self.scorer.setPos(
            MainGeometry.width - (self.scorer.boundingRect().width() + Display.max_width) / 2 - 40,
            MainGeometry.centered(
                0,
                self.height,
                self.scorer.boundingRect().height()
                + self.counter.boundingRect().height()
                + self.timer.boundingRect().height()
                + 2 * Display.ext_marge_height
            )
        )
        self.counter.setPos(
            MainGeometry.width - (self.counter.boundingRect().width() + Display.max_width) / 2 - 40,
            self.scorer.y() + self.scorer.boundingRect().height() + Display.ext_marge_height
        )
        self.timer.setPos(
            MainGeometry.width - (self.timer.boundingRect().width() + Display.max_width) / 2 - 40,
            self.counter.y() + self.counter.boundingRect().height() + Display.ext_marge_height
        )

        # Starter attributes

        self.home = HomeCurtain()
        self.addItem(self.home)
        self.home.setVisible(True)

        # Prepare round's curtain for transition

        self.round_curtain = Curtain()
        self.round_text = TextInForeground("", self.round_curtain)
        self.round_text.setPos(GameScene.width / 2, GameScene.height / 2)
        self.addItem(self.round_curtain)

        # Prepare results curtain for the end of the rounds

        self.result_curtain = Curtain(alpha=50)
        self.result_text = TextInForeground("", self.result_curtain)
        self.result_text.setPos(GameScene.width / 2, GameScene.height / 2)
        self.addItem(self.result_curtain)

        self.setSceneRect(0, 0, GameScene.width, GameScene.height)

    def _init_board(self):

        # Fixed manager items

        self.counter.max_round.display_number(self.settings_manager.get_number_of_rounds())

        # Frontier items

        for i in range(9):
            x = i * Stone.marge + i * Stone.width + MainGeometry.marge
            y = MainGeometry.marge + Stone.height + Stone.marge
            self.automaton.sides[i].setPos(x, y)
            y += Side.height + Stone.marge
            self.stones[i].setPos(x+1, y+2)
            y += Stone.height + Stone.marge
            self.player.sides[i].setPos(x, y)

        self.automaton.playmat.setScale(0.6)

        # Set items positions

        y = GameScene.height - 2 * MainGeometry.marge - Card.height

        self.deck.set_pos_init(self.player.playmat.width + 2 * Card.width, y)
        self.player.playmat.setPos(MainGeometry.marge, y)
        self.automaton.playmat.setPos(MainGeometry.marge, MainGeometry.marge)

        # Set zValue max

        self.card_manager.reset_zmax()
        for item in self.items():
            self.card_manager.set_zmax(item.zValue())

    def prepare_new_round(self):

        self.result_curtain.animate_leaving()
        self.settings_manager.switch_first_player()

        # pick up the cards from everywhere

        self.card_manager.pick_up_cards(self.player.playmat.cards)
        self.card_manager.pick_up_cards(self.automaton.playmat.cards)

        for side in self.player.sides:
            self.card_manager.pick_up_cards(side.cards)

        for side in self.automaton.sides:
            self.card_manager.pick_up_cards(side.cards)

        self.card_manager.reset_cards()

        # reset the stones

        for i in range(9):
            self.stones[i].reset()

    def next_round(self):
        print("\n----- next round ------")

        # update scores and statistics

        self.player.update()
        self.automaton.update()
        self.scorer.set_score_left(self.player.total_score)
        self.scorer.set_score_right(self.automaton.total_score)
        print("scores: ", self.player.total_score, self.automaton.total_score)
        # ending the game

        if self.current_round == self.settings_manager.get_number_of_rounds():
            # TODO: curtain telling who won the game
            self.player.reset()
            self.automaton.reset()
            self.home.animate_incoming(self.get_zmax()+1)
            return

        # update current round

        self.current_round += 1
        self.counter.current_round.display_number(self.current_round)

        # if first round starting the game, else preparing next round

        if self.current_round == 1:
            self.home.leave()
            self._init_board()
        else:
            self.prepare_new_round()

        self.umpire.final_countdown = False

        # Animate round's transition

        self.round_curtain.change_text(
            self.round_text,
            "ROUND " + str(self.current_round)
        )
        self.round_curtain.animate_incoming(self.get_zmax()+1)
        QTimer.singleShot(2000, lambda: self.round_curtain.animate_leaving(function=self.start_round))

    def start_round(self):
        print("start round")
        # Draw cards & start the timer

        for i in range(self.settings_manager.get_max_cards_in_hand()):
            self.player.playmat.add(self.deck.draw(), True)
            self.automaton.playmat.add(self.deck.draw())

        self.timer.start(self.settings_manager.get_time())

        # manage the first turn of automaton if he's first player

        if self.settings_manager.get_first_player() == self.automaton:
            self.automaton.choose_card(self.settings_manager.get_difficulty())
            self._play_turn(self.automaton)

    def time_out(self):
        print("time out")
        self.player.choose_card()
        self.proceed()

    def proceed(self):
        self._play_turn(self.player)
        self.automaton.choose_card(self.settings_manager.get_difficulty())
        self._play_turn(self.automaton)

    """
        Method processing the current player's turn
    """
    def _play_turn(self, current_player):
        print("play a turn:", current_player.name)
        side = self.shift_manager.side

        # Memorize initial position for new card from the deck

        pos = self.shift_manager.card.anchor_point

        # Add the card dropped to the side and remove it from the playmat

        current_player.playmat.remove(self.shift_manager.card)
        side.add_card(self.shift_manager.card)
        side.light_off()

        # Draw a new card unless deck is empty

        if self.deck.is_empty():
            if self.player.playmat.is_empty() and self.automaton.playmat.is_empty():
                self.umpire.final_countdown = True
        else:
            new_card = self.deck.draw()
            draggable = current_player is self.player
            current_player.playmat.add(new_card, draggable)
            new_card.set_anchor_point(pos)
            new_card.move_to(self.deck.pos() - current_player.playmat.pos(), pos)

        # Actions if the targetted side is full now

        if side.is_full():
            self.stones[side.numero].put_a_third_card(current_player)
            self.umpire.book(side)

        # Ask the umpire to score and to tell who won the round

        winner = self.umpire.judge(self.player, self.automaton, self.stones)

        # reset shift_manager & eventually show the ending message

        self.shift_manager.reset()

        if winner is not None:
            self.result_curtain.change_text(
                self.result_text,
                winner.name + " WON ROUND " + str(self.current_round)
            )
            self.result_curtain.animate_incoming(self.get_zmax())
            QTimer.singleShot(3000, self.next_round)

        else:
            self.timer.start(self.settings_manager.get_time())

    def mouseMoveEvent(self, event):

        super(GameScene, self).mouseMoveEvent(event)

        if self.shift_manager.dragged:

            # Enlightment for user's side hovered

            items = self.collidingItems(self.shift_manager.card)
            closest_item = None
            if items:
                shortest_dist = 100000.
                for item in items:
                    if item in self.player.sides:
                        line = QLineF(item.sceneBoundingRect().center(),
                                      self.shift_manager.card.sceneBoundingRect().center())
                        if line.length() < shortest_dist:
                            shortest_dist = line.length()
                            closest_item = item

                if closest_item is not None and not closest_item.is_full():
                    closest_item.light_on()
                    self.itemsSelected.append(closest_item)

            for item in self.itemsSelected:
                if item is not closest_item:
                    item.light_off()
                    self.itemsSelected.remove(item)

        # TODO : Management for reordering the user's playmat

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
            pos1 = Card.cards[self.user_hand[i]].anchor_point
            pos2 = Card.cards[self.user_hand[i + sens]].anchor_point
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
    """
        Do following stuf after a card has been dropped
    """
    def mouseReleaseEvent(self, event):

        for item in self.itemsSelected:
            item.light_off()
            self.itemsSelected.remove(item)

        super(GameScene, self).mouseReleaseEvent(event)

        if not self.shift_manager.is_dragged():
            return

        # Events from Cards: If cards has been moved to a droppable zone:

        # 1/ user's deck
        """
        if self.cardManager.is_moved_to_reorganize():
            self.user_hand = self.new_order
        """
        # 2/ when the player puts a card on an avaiable side, starts process for the turn's of each player

        if self.shift_manager.side is not None:
            self.proceed()
        else:
            self.shift_manager.card.move_to(self.shift_manager.card.pos(), self.shift_manager.card.anchor_point)
            self.shift_manager.reset()

        self.update()

    """
     Calcul the height knowing the width needed to show the scene
     without scrolling
    """
    @classmethod
    def set_size(cls):
        cls.width = MainGeometry.width - 40
        cls.height = int(
            4 * Stone.height + 4.33 * Card.height
            + cls.marge * 2 + 8 * MainGeometry.pen_width + 4 * Stone.marge + 40
        ) - 60

    """
       Return the maximum zValue in th scene
    """
    def get_zmax(self):
        return self.card_manager.get_zmax()

    """
     cheat mode: show automaton's playmat in a subwindow
    """
    def show_automaton_playmat(self):
        self.addItem(self.automaton.playmat)

    def hide_automaton_playmat(self):
        self.removeItem(self.automaton.playmat)
