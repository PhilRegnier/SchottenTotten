#
# Game definition
#
from math import sqrt
from random import choice

from PyQt5.QtCore import QPropertyAnimation, QLineF, QTimer, QParallelAnimationGroup
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

from src import UserSide
from src.AutoSide import AutoSide
from src.Card import Card
from src.Chifoumi import Chifoumi
from src.Curtain import Curtain
from src.Deck import Deck
from src.Home import Home
from src.Memo import Memo
from src.MovingCard import MovingCard
from src.PlayerDeck import PlayerDeck
from src.Settings import Settings
from src.Statistics import Statistics
from src.Stone import Stone
from src.TextInForeground import TextInForeground
from src.variables_globales import mainWindow_width, background_color, stone_marge, stone_width, \
    mainWindow_marge, stone_height, side_height, user_side_color0, user_side_pen, marge, \
    auto_side_color0, auto_side_color1, auto_side_pen, mainWindow_height, cote_both, \
    cote_brelan, cote_couleur, cote_suite, user_side_color1


class Game(QGraphicsView):

    def __init__(self, parent):
        super().__init__(parent)

        # initialize private variables

        self.user_score = 0
        self.auto_score = 0
        self.i_round = 0

        self.chifoumi = Chifoumi()

        # Preset the scene and the view

        self.board = QGraphicsScene(self)
        self.board.setSceneRect(0, 0, mainWindow_width - 40, mainWindow_height - 60)

        # Set the view

        self.parent = parent
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setBackgroundBrush(QBrush(background_color))
        self.setScene(self.board)

        # Home screen

        self.home = Home()
        self.board.addItem(self.home)
        self.home.setVisible(True)

        # Prepare a timer

        self.timer = QTimer(self)

    def newRound(self):

        # ending the game

        if self.i_round == Settings.get_rounds_nb():
            self.home.setVisible(True)
            self.home.animate_incoming()
            return

        # starting the game

        self.items_selected = []
        self.i_round += 1

        # Switch the first player between each round

        if self.i_round > 1:
            Settings.switch_first_player()

        # Set the board

        self.deck = Deck()
        self.setupHands()
        self.setupBoard()

        self.ending = False

        global statistics
        statistics = Statistics()

    def setupHands(self):
        """
        Create players' hands
        """
        self.user_hand = []
        self.auto_hand = []
        self.new_order = []

        for i in range(Settings.get_hand_nb()):
            self.user_hand.append(self.deck.draw())
            self.auto_hand.append(self.deck.draw())

    def setupBoard(self):
        """
        Create board game items and set the board scene
        """

        # Frontier items

        self.auto_side = [AutoSide(i) for i in range(9)]
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

        self.user_deck = PlayerDeck(user_side_color0, user_side_color1, user_side_pen)

        for i in range(Settings.get_hand_nb()):
            Card.cards[self.user_hand[i]].setParentItem(self.user_deck)
            Card.cards[self.user_hand[i]].setPos((i + 1) * marge + i * Card.width, marge)
            Card.cards[self.user_hand[i]].setAnchorPoint(Card.cards[self.user_hand[i]].pos())
            Card.cards[self.user_hand[i]].setDraggable(True)
            Card.cards[self.user_hand[i]].setVisible(True)
            Card.cards[self.user_hand[i]].setIndex(i)

        # Computer's hand cards items [CHEAT MODE]

        self.auto_deck = PlayerDeck(auto_side_color0, auto_side_color1, auto_side_pen)

        for i in range(Settings.get_hand_nb()):
            Card.cards[self.auto_hand[i]].setParentItem(self.auto_deck)
            Card.cards[self.auto_hand[i]].setPos((i + 1) * marge + i * Card.width, marge)
            Card.cards[self.auto_hand[i]].setAnchorPoint(Card.cards[self.auto_hand[i]].pos())
            Card.cards[self.auto_hand[i]].setVisible(True)

        self.auto_deck.setScale(0.6)

        # Set items positions

        bottom_y = mainWindow_height - 5 * mainWindow_marge - Card.height - 2 * marge

        self.deck.setPosInit(1000, bottom_y)
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

    def autoHandView(self):
        """
        Showing computer's hand cards in a subwindow
        """
        self.board.addItem(self.auto_deck)

    def autoHandClose(self):
        self.board.removeItem(self.auto_deck)

    def mouseMoveEvent(self, event):
        QGraphicsView.mouseMoveEvent(self, event)

        if MovingCard.isDragged():

            # Enlightment for user's side hovered

            items = self.items(event.pos())

            for item in items:
                if item.Type == UserSide.Type:
                    if item.nCard < 3:
                        item.setOpacity(1)
                        self.itemsSelected.append(item)

            for item in self.itemsSelected:
                if not item in items:
                    item.setOpacity(0.5)

            # Management for reordering the user's hand

            # self.mouseMoveHand()

    def mouseMoveHand(self):
        """
        Reorganization of the user's hand
        """
        MovingCard.userDontWantToReorganize()

        col_items = Card.cards[MovingCard.card_id].collidingItems()

        if col_items:
            shortest_dist = 100000.
            for item in col_items:

                if item == Card.cards[MovingCard.card_id].parentItem():
                    continue

                if item.parentItem() == Card.cards[MovingCard.card_id].parentItem():
                    line = QLineF(item.sceneBoundingRect().center(),
                                  Card.cards[MovingCard.card_id].sceneBoundingRect().center())
                    if line.length() < shortest_dist:
                        shortest_dist = line.length()
                        # if card_hover != item.numero or card_dx*line.dx() < 0:
                        MovingCard.userWantToReorganize()

                        card_dx = line.dx()
                        card_hover = item.numero

        if MovingCard.isMovedToReorganize():
            self.new_order = self.user_hand
        else:
            return

        # Set the concerned cards

        if Card.cards[MovingCard.card_id].index - Card.cards[card_hover].index < 0:
            i1 = Card.cards[MovingCard.card_id].index + 1
            i2 = Card.cards[card_hover].index
            sens = -1
            if card_dx > 0:
                i2 += 1
        else:
            i1 = Card.cards[card_hover].index
            i2 = Card.cards[MovingCard.card_id].index
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

        QGraphicsView.mouseReleaseEvent(self, event)

        # Events from Cards: If cards has been moved to a droppable zone

        if MovingCard.isDragged():

            # Card moved on user's deck

            if MovingCard.isMovedToReorganize():
                self.user_hand = self.new_order

            # Card moved on side or no ?

            if MovingCard.side_id() >= 0:

                # position in the hand

                i = Card.cards[MovingCard.card_id()].index

                # Memorize initial position for new card from the deck

                pos = Card.cards[MovingCard.card_id()].anchorPoint

                # Add the card drop to the side

                self.user_side[MovingCard.side_id()].addCard(MovingCard.card_id)
                self.user_side[MovingCard.side_id()].setOpacity(0.5)

                # Draw a new card

                if self.deck.isEmpty():
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

                if self.user_side[MovingCard.side_id()].nCard == 3:
                    self.book(self.user_side[MovingCard.side_id()])

                self.judge()

                side_nb = -1
                card_nb = -1

                # Run automate's turn

                self.automate()

                if self.auto_side[side_nb].nCard == 3:
                    self.auto_side[side_nb].droppable = False
                    self.book(self.auto_side[side_nb])

                self.judge()

                side_nb = -1
                card_nb = -1
            else:
                Card.cards[MovingCard.card_id].moveTo(Card.cards[MovingCard.card_id].pos(),
                                                      Card.cards[MovingCard.card_id].anchorPoint)

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
                self.board.addItem(self.chifoumi)
                self.chifoumi.animate_incoming()
                self.chifoumi.start()

            # ... Chifoumi

            if selected < 3:
                self.chifoumi.choosePlayer()

                if player_1 == -1:
                    self.chifoumi.restart()
                else:
                    if player_1 == 0:
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

    # --------------------------------------------------------------------------------------------------
    # Leave chifoumi curtain and launch the game
    # --------------------------------------------------------------------------------------------------
    def letsGo(self):
        self.text.setVisible(False)
        self.chifoumi.animate_leaving()
        self.home.animate_leaving()
        self.newRound()

    # --------------------------------------------------------------------------------------------------
    # Choose the automate and play the card on the side
    # --------------------------------------------------------------------------------------------------
    def automate(self):

        if Settings.get_difficulty() == 1:
            self.cervo1()
        else:
            self.cervo0()

        # move the card and draw a new one

        MovingCard.set_card_id(self.auto_hand[MovingCard.hand_id()])
        pos = Card.cards[MovingCard.card_id()].anchorPoint
        self.auto_side[MovingCard.side_id()].addCard(MovingCard.card_id())
        pos0 = self.auto_deck.pos() - self.auto_side[MovingCard.side_id()].pos() + pos
        Card.cards[MovingCard.card_id()].moveTo(pos0, Card.cards[MovingCard.card_id()].anchorPoint)

        if self.deck.isEmpty():
            self.auto_hand[MovingCard.hand_id()] = -1
            statistics.removeAutoHand(MovingCard.hand_id())
            if sum(self.auto_hand) == -6:
                self.ending = True
        else:
            self.auto_hand[MovingCard.hand_id()] = self.deck.draw()
            Card.cards[self.auto_hand[MovingCard.hand_id()]].setVisible(True)
            Card.cards[self.auto_hand[MovingCard.hand_id()]].setParentItem(self.auto_deck)
            Card.cards[self.auto_hand[MovingCard.hand_id()]].setAnchorPoint(pos)
            Card.cards[self.auto_hand[MovingCard.hand_id()]].setPos(pos)

    # --------------------------------------------------------------------------------------------------
    # Automate 0 : random card and random stone
    # --------------------------------------------------------------------------------------------------
    def cervo0(self):
        MovingCard.set_hand_id(choice(statistics.autoLh()))
        MovingCard.set_side_id(choice(statistics.autoLs()))

    # --------------------------------------------------------------------------------------------------
    # Automate 1 : first steps choice
    # --------------------------------------------------------------------------------------------------
    def cervo1(self):

        # Settings for memorization of relevant combinations

        memo = []

        # Setting cards color and valor in lists

        v = [0 for i in range(6)]
        c = ["0" for i in range(6)]

        for i in statistics.autoLh():
            v[i] = Card.cards[self.auto_hand[i]].valeur
            c[i] = Card.cards[self.auto_hand[i]].couleur

        # 1 Looking in the hand

        for i in statistics.autoLh():
            for j in statistics.autoLh():
                if i != j:

                    dvij = v[i] - v[j]

                    # For flush pair(s)

                    if c[i] == c[j] and 3 > dvij > -3:
                        for k in statistics.autoLs1():
                            if c[i] == Card.cards[self.auto_side[k].index[0]].couleur:
                                dvik = v[i] - Card.cards[self.auto_side[k].index[0]].valeur
                                if (dvij == 2 and dvik == 1) \
                                        or (dvij == -2 and dvik == -1) \
                                        or (dvij == 1 and dvik == 2) \
                                        or (dvij == -1 and dvik == -2):
                                    memo.append(Memo(i, k, cote_both))

                    # For pair(s)

                    if dvij == 0:
                        for k in statistics.autoLs1():
                            if v[i] == Card.cards[self.auto_side[k].index[0]].valeur:
                                memo.append(Memo(i, k, cote_brelan))

        # 2 Search in the sides with 2 cards

        for i in statistics.autoLh():
            for k in statistics.autoLs2():

                dvij = v[i] - Card.cards[self.auto_side[k].index[0]].valeur
                dvik = v[i] - Card.cards[self.auto_side[k].index[1]].valeur

                lcolor = (c[i] == Card.cards[self.auto_side[k].index[0]].couleur
                          and c[i] == Card.cards[self.auto_side[k].index[1]].couleur)

                lsuite = ((dvij == -1 and dvik == -2)
                          or (dvij == -2 and dvik == -1)
                          or (dvij == 1 and dvik == -1)
                          or (dvij == -1 and dvik == 1)
                          or (dvij == 2 and dvik == 1)
                          or (dvij == 1 and dvik == 2))

                # Test if a card in the hand goes to flush third

                if lcolor and lsuite:
                    memo.append(Memo(i, k, cote_both * 1.5))

                # Test if a card in the hand goes to 3 of a kind

                if dvij == 0 and dvik == 0:
                    memo.append(Memo(i, k, cote_brelan * 1.5))

                # Test if a card in the hand goes to color

                if lcolor:
                    memo.append(Memo(i, k, cote_couleur))

                # Test if a card in the hand goes to suite

                if lsuite:
                    memo.append(Memo(i, k, cote_suite))

        # 3 Search in the sides with 1 card

        for i in statistics.autoLh():
            for k in statistics.autoLs1():

                dvij = v[i] - Card.cards[self.auto_side[k].index[0]].valeur

                lcolor = (c[i] == Card.cards[self.auto_side[k].index[0]].couleur)
                lsuite = (dvij == -1 or dvij == -2 or dvij == 1 or dvij == 2)

                # Test if a card of the hand matchs for flush third

                if lcolor and lsuite:
                    memo.append(Memo(i, k, cote_both))

                # Test if a card of the hand matchs for 3 of a kind

                if dvij == 0:
                    memo.append(Memo(i, k, cote_brelan / 1.5))

                # Test if a card of the hand matchs for color

                if lcolor:
                    memo.append(Memo(i, k, cote_couleur / 1.5))

                # Test if a card of the hand match for suite

                if lsuite:
                    memo.append(Memo(i, k, cote_suite))

        # Choosing the best combination

        if memo:
            c = 0.0
            k = 0
            for i in range(len(memo)):
                c = max(c, memo[i].cote)
                if c == memo[i].cote:
                    k = i

            MovingCard.set_hand_id(memo[k].hand)
            MovingCard.set_side_id(memo[k].side)
            return

        # 4 Play a random card on a random free side

        if statistics.autoLs0():
            MovingCard.set_side_id(choice(statistics.autoLs0()))
            MovingCard.set_hand_id(choice(statistics.autoLh()))
            return

        # 5 Last call...

        self.cervo0()

    # --------------------------------------------------------------------------------------------------
    # Test after a third card has been played on a side
    # --------------------------------------------------------------------------------------------------
    def book(self, side):

        i = side.index[0]
        j = side.index[1]
        k = side.index[2]

        suite = False
        flush = False

        # test for straight =>  somme € [106; 124]

        liste = sorted([Card.cards[i].valeur, Card.cards[j].valeur, Card.cards[k].valeur])

        if liste[1] == liste[0] + 1 and liste[2] == liste[1] + 1:
            suite = True
            side.somme += cote_suite

        # test for flush => somme € [206; 324]

        if Card.cards[i].couleur == Card.cards[j].couleur == Card.cards[k].couleur:
            flush = True
            side.somme += cote_couleur

        # test for straight flush => somme € [506; 524]

        if suite and flush:
            side.somme += cote_both

        # test for three of a kind => somme € [403; 427]

        elif Card.cards[i].valeur == Card.cards[j].valeur == Card.cards[k].valeur:
            side.somme += cote_brelan

    # --------------------------------------------------------------------------------------------------
    # Compare sides and test for victory
    # --------------------------------------------------------------------------------------------------
    def judge(self):

        # if 3 cards have been played on each side, test for claim of the stone

        if self.user_side[side_nb].nCard == 3 and self.auto_side[side_nb].nCard == 3:
            if self.user_side[side_nb].somme > self.auto_side[side_nb].somme:
                self.stone[side_nb].winner = "user"
                self.stone[side_nb].moveStoneTo(side_height + 6 + stone_height)
            elif self.user_side[side_nb].somme < self.auto_side[side_nb].somme:
                self.stone[side_nb].winner = "auto"
                self.stone[side_nb].moveStoneTo(-side_height - 6 - stone_height)
            else:
                self.stone[side_nb].winner = "equal"

        # party endding

        uss = 0
        aus = 0

        if self.ending:

            # Finish to claim stones

            for i in range(9):
                if not self.stone[i].winner:
                    if self.user_side[i].somme > self.auto_side[i].somme:
                        self.stone[i].winner = "user"
                        self.stone[i].moveStoneTo(side_height + 6 + stone_height)
                    elif self.user_side[i].somme < self.auto_side[i].somme:
                        self.stone[i].winner = "auto"
                        self.stone[i].moveStoneTo(-side_height - 6 - stone_height)
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
            self.i_round -= 1
        elif winner == "user":
            text = "YOU WON ROUND " + str(self.i_round) + " !!!"
            self.user_score += 1
        else:
            text = "AUTOMA WON ROUND " + str(self.i_round) + " !!!"
            self.auto_score += 1

        if self.i_round < Settings.get_rounds_nb():
            text += "ROUND " + str(self.i_round) + " !!!"
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

        QTimer.singleShot(3000, self.newRound)
