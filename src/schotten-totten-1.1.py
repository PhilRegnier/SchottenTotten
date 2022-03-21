#------------------------------------------------------------------------------------------------------
# Schotten Totten
#------------------------------------------------------------------------------------------------------
import sys

from random import shuffle, choice, randint
from math import sqrt

from PIL import Image, ImageDraw, ImageQt


from PyQt5.QtWidgets import (QApplication, QMainWindow, QStatusBar, QGraphicsLineItem,
                             QAction, QMessageBox, QGraphicsItem, QGraphicsObject,
                             QGraphicsView, QGraphicsScene, QGraphicsSimpleTextItem,
                             QGraphicsPixmapItem, QGraphicsDropShadowEffect,
                             QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSpinBox, QPushButton)
from PyQt5.QtCore import (Qt, QLineF, QPointF, QRect, QRectF, QPropertyAnimation, QParallelAnimationGroup, QTimer)
from PyQt5.QtGui import (QIcon, QPixmap, QBrush, QColor, QPainter, QPen,
                         QLinearGradient, QFont)
#------------------------------------------------------------------------------------------------------
# Variables globales (peut mieux faire...)
#------------------------------------------------------------------------------------------------------
__version__ = "1.1"

# Game set

colors    = ['jaune','vert','rouge','brun','bleu','violet']
max_value = 9
N_cards   = len(colors)*max_value
N_hand    = 6
card      = []
difficulT = 1
N_rounds  = 1
sounds    = False
variant   = False

# Objects dimensions & geometries

mainWindow_width  = 1200
mainWindow_marge  = 20
pen_width         = 1.
stone_marge       = 4.
marge             = 5.
stone_width       = (mainWindow_width - 2*mainWindow_marge - 8*stone_marge - 40) / 9 - 2*pen_width
card_width        = stone_width - 4
card_height       = card_width * 1.42
stone_height      = stone_width * 0.58
side_height       = card_height * 1.667
mainWindow_height = int(4*stone_height + 4.33*card_height + mainWindow_marge*2 + 8*pen_width + 4*stone_marge + 40)
rBound            = 10.0

# Global variables managing scenography

parentId = 0
userType = 100000
clicked  = False
selected = -1 # 0= feuille; 1=ciseaux; 2=pierre; 10=settings; 11=starting; 20=ok ; 21=cancel; 
player_1 = 0 # O=user (default); 1=automate

# Global Variables managing cards movements between graphics items

side_nb = -1 # to point on the side of the drop
card_nb = -1 # to point on card dropped
hand_nb = -1 # to point on the hand's index of the card dragged
dragged = False
userWantToReorganize = False
card_hover = -1
card_dx = 0.
z_max = 0.

# cotations for cards combinations

cote_suite = 100
cote_couleur = 200
cote_both = 200
cote_brelan = 400

# Colors

cadre_color      = (57,57,57)
relief_color     = (53,53,43,255)
relief_color2    = (65,71,35,255)
ombrage_color    = QColor(36,36,36,90)
ombrage_color_bt = QColor(36,36,36,200)
background_color = QColor(167,159,120)

user_side_color0 = QColor(9,18,27,90)
user_side_color1 = QColor(85,170,255,90)
user_side_pen = QColor(85,81,44)
user_hand_color = QColor(85,170,255,40)
user_hand_pen = QColor(10,11,8)

auto_side_color1 = QColor(255,85,0,90)
auto_side_color0 = QColor(70,23,0,90)
auto_side_pen    = QColor(85,81,44)
auto_hand_color  = QColor(49,53,42,150)
auto_hand_pen    = QColor(10,11,8)

#------------------------------------------------------------------------------------------------------
# Image pretreatment : rounding corners
#------------------------------------------------------------------------------------------------------
def round_corners(image, r):
    w, h = image.size
    circle = Image.new('L', (r*2,r*2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, r*2, r*2), fill = 255)
    alpha = Image.new('L', image.size, 255)
    alpha.paste(circle.crop((0, 0, r, r)), (0, 0))
    alpha.paste(circle.crop((0, r, r, r*2)), (0, h-r))
    alpha.paste(circle.crop((r, 0, r*2, r)), (w-r, 0))
    alpha.paste(circle.crop((r, r, r*2, r*2)), (w-r, h-r))
    image.putalpha(alpha)
    return image
#------------------------------------------------------------------------------------------------------
# Image pretreatment : frame & thickness
#------------------------------------------------------------------------------------------------------
def enluminure(im, r=rBound, t=1, ow=1, oh=1):
    im = round_corners(im, int(r))

    cadre = Image.new('RGBA', (im.width+2*t,im.height+2*t), cadre_color)
    cadre = round_corners(cadre, int(r+t))
    cadre.paste(im, (t,t), im)

    trame = Image.new('RGBA', (cadre.width+ow,cadre.height+oh), (0,0,0,0))
    relief = Image.new('RGBA', (cadre.width,cadre.height), relief_color)
    relief = round_corners(relief, int(r+t))
    trame.paste(relief, (ow,oh), relief)
    trame.paste(cadre, (0,0), cadre)
    image = ImageQt.ImageQt(trame)

    return image

#------------------------------------------------------------------------------------------------------
# Card definition
#------------------------------------------------------------------------------------------------------
class Card(QGraphicsObject):
    
    def __init__(self, numero, parent=None):
        if numero < 0 or numero > N_cards-1:
            print("Card number must be into [0, 53]. Program stopped")
            sys.exit(0)
        super().__init__(parent)
        self.numero  = numero
        self.index   = -1
        self.anchorPoint = QPointF()
        self.valeur  = numero % max_value + 1
        self.couleur = colors[numero // max_value]
        
        image = Image.open('images/'+self.couleur+str(self.valeur)+'.jpg')
        image.thumbnail((card_width-2,card_height-2))
        self.pixmap = QPixmap.fromImage(enluminure(image))
        
        self.setAcceptHoverEvents(False)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self.ombrage = Ombrage()
        self.setGraphicsEffect(self.ombrage)
        
    def setDraggable(self, draggable=True):
        if draggable:
            self.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.setAcceptHoverEvents(True)
        else:
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.setAcceptHoverEvents(False)

    def setAnchorPoint(self, anchorPoint):
        self.anchorPoint = anchorPoint
        
    def setIndex(self, index):
        self.index = index

    def hoverEnterEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)
        self.setPos(self.x()-2,self.y()-2)
        self.ombrage.setEnabled(True)
        
    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.setPos(self.anchorPoint)
        self.ombrage.setEnabled(False)

    def mousePressEvent(self, event):
        if not event.button() == Qt.LeftButton:
            return
        if self.parentItem().Type == UserSide.Type or self.parentItem().Type == AutoSide.Type:
            return

        self.dragStartPosition = event.pos()
        self.setCursor(Qt.ClosedHandCursor)
        self.ombrage.setEnabled(True)
            
    def mouseMoveEvent(self, event):
        global dragged, card_nb
        
        # Check button pressed, card's origin, and that a minimum move has been done
        
        if not (event.buttons() == Qt.LeftButton):
            return
        if self.parentItem().Type == UserSide.Type or self.parentItem().Type == AutoSide.Type:
            return
        if ((event.pos() - self.dragStartPosition).manhattanLength() < QApplication.startDragDistance()):
            return
        
        # All staff when a card is dragged from the user's hand

        dragged = True
        card_nb = self.numero
        QGraphicsObject.mouseMoveEvent(self, event)
        self.ombrage.setEnabled(True)
        self.setOpacity(0.9)
        self.setCursor(Qt.ClosedHandCursor)

        # get sure the card dragged is in the foreground
        
        zvalue = 0.
        colItems = self.collidingItems()
        if colItems:
            for item in colItems:
                if item.zValue() >= zvalue:
                    zvalue = item.zValue() + 0.1

        self.setZValue(zvalue)
                
    def setCardOnSide(self, item):
        global side_nb
        if item.Type == UserSide.Type:
            if item.nCard < 3:
                side_nb = item.numero
                self.setDraggable(False)
                       
                # get sure that the card dropped is in the foreground
                        
                if item.nCard > 0:
                    self.setZValue(card[item.index[len(item.index)-1]].zValue()+0.1)        
        
    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        if dragged:
            colItems = self.collidingItems()
            if colItems:
                closestItem = colItems[0]
                shortestDist = 100000.
                
                for item in colItems:
                    line = QLineF(item.sceneBoundingRect().center(),
                                  self.sceneBoundingRect().center())
                    if line.length() < shortestDist:
                        shortestDist = line.length()
                        closestItem = item

                if closestItem.parentItem():
                    self.setCardOnSide(closestItem.parentItem())
                else:
                    self.setCardOnSide(closestItem)

            QGraphicsObject.mouseReleaseEvent(self, event)
            self.ombrage.setEnabled(False)
            self.setOpacity(1)            

    def moveTo(self, pos1, pos2):

        # animation for the move

        self.moveCard = QPropertyAnimation(self, b"pos")
        dx = pos1.x() - pos2.x()
        dy = pos1.y() - pos2.y()
        duration = int(sqrt(dx**2 + dy**2) / 1)
        self.moveCard.setDuration(duration)
        self.moveCard.setStartValue(pos1)
        self.moveCard.setEndValue(pos2)
        
        self.setOnTop()
        self.moveCard.finished.connect(self.setOnGround)
    
        self.moveCard.start()

    def setOnTop(self):
        self.z_old = self.zValue()
        self.setZValue(1000)
    
    def setOnGround(self):
        self.setZValue(self.z_old)

    def boundingRect(self):
        penWidth = 1.0
        return QRectF(-penWidth/2, -penWidth/2, card_width+penWidth, side_height+penWidth)
    
    def paint(self, painter, option, widget):
        rect = QRect(-1, -1, int(card_width), int(card_height))
        painter.drawPixmap(rect, self.pixmap)

#------------------------------------------------------------------------------------------------------
# Stone definition
#------------------------------------------------------------------------------------------------------
class Stone(QGraphicsObject):
    
    Type = userType + 1
    
    def __init__(self, numero, parent=None):
        super().__init__(parent)
        self.numero = numero
        image = Image.open('images/borne'+str(self.numero+1)+'.jpg')
        image.thumbnail((stone_width-1,stone_height-1))
        self.pixmap = QPixmap.fromImage(enluminure(image, ow=2, oh=2))
        self.winner = ""

    def boundingRect(self):
        penWidth = 1.0
        return QRectF(-penWidth/2, -penWidth/2, stone_width+penWidth, stone_height+penWidth)
    
    def paint(self, painter, option, widget):
        rect = QRect(-1, -1, int(stone_width), int(stone_height))
        painter.drawPixmap(rect, self.pixmap)

    #--------------------------------------------------------------------------------------------------
    # Animation for claimed stones
    #--------------------------------------------------------------------------------------------------                
    def moveStoneTo(self,dy):
        self.moveStone = QPropertyAnimation(self, b"pos")
        self.moveStone.setDuration(800)
        self.moveStone.setStartValue(self.pos())
        self.moveStone.setEndValue(QPointF(self.x(),self.y()+dy))
        self.moveStone.start()
#------------------------------------------------------------------------------------------------------
# Deck definition
#------------------------------------------------------------------------------------------------------
class Deck(QGraphicsPixmapItem):
    
    Type = userType + 2
    Nc = N_cards
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.x1 = 0
        self.y1 = 0

        self.empilement()
        self.empty = False
        
        # Create a random deck
        
        liste_cartes = [i for i in range(N_cards)]
        shuffle(liste_cartes)

        self.index = liste_cartes

        for i in range(N_cards):
            card[i].setParentItem(self)
            card[i].setPos(0,0)
            card[i].setVisible(False)

    def isEmpty(self):
        return self.empty
    
    def draw(self):
        card = self.index[0]
        del self.index[0]
        self.Nc -= 1
        if self.Nc == 0:
            self.setVisible(False)
            self.empty = True
        else:
            self.empilement()
            self.setPos(self.x1-self.wi,self.y1-self.he)
            
        return card
            
    def setPosInit(self,x0,y0):
        self.x1 = x0 + self.wi
        self.y1 = y0 + self.he
        self.setPos(x0,y0)
        
    def empilement(self):
        r  = rBound
        t  = 1
        ow = 1
        oh = 1
        im = Image.open("images/back.jpg")
        im.thumbnail((card_width-2*t,card_height-2*t))
        im = round_corners(im, int(r))        
        cadre = Image.new('RGBA', (im.width+2*t,im.height+2*t), cadre_color)
        cadre = round_corners(cadre, int(r+t))
        cadre.paste(im, (t,t), im)
        nc2 = int(self.Nc/2)
        trame = Image.new('RGBA', (cadre.width+nc2*ow,cadre.height+nc2*oh), (0,0,0,0))
        relief1 = Image.new('RGBA', (cadre.width,cadre.height), relief_color2)
        relief1 = round_corners(relief1, int(r+t))
        relief2 = Image.new('RGBA', (cadre.width,cadre.height), relief_color)
        relief2 = round_corners(relief2, int(r+t))

        for i in range(nc2,1,-2):
            trame.paste(relief1, (i*ow,i*oh), relief1)
            trame.paste(relief2, ((i-1)*ow,(i-1)*oh), relief2)
            
        trame.paste(cadre, (0,0), cadre)        
        image = ImageQt.ImageQt(trame)        
        pixmap = QPixmap.fromImage(image)
        self.setPixmap(pixmap)
        self.wi = pixmap.width()
        self.he = pixmap.height()
#------------------------------------------------------------------------------------------------------
# Common side definitions
#------------------------------------------------------------------------------------------------------
class Side(QGraphicsItem):
    
    def __init__(self, numero, color0, color1, pen, parent=None):
        super().__init__(parent)
        self.numero = numero
        self.nCard = 0
        self.index = []
        self.somme = 0
        self.setFlag(QGraphicsItem.ItemDoesntPropagateOpacityToChildren)
        self.setOpacity(0.5)
        self.color0 = color0
        self.color1 = color1
        self.pen = pen

    def boundingRect(self):
        penWidth = 1.0
        return QRectF(-penWidth/2, -penWidth/2, stone_width+penWidth, side_height+penWidth)
    
    def paint(self, painter, option, widget):
        gradient = QLinearGradient(0., side_height, 0., 0.)
        gradient.setSpread(QLinearGradient.ReflectSpread)
        gradient.setColorAt(0, self.color0)
        gradient.setColorAt(1, self.color1)
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(self.pen, 1))   
        rect = QRectF(0., 0., float(stone_width), float(side_height))
        painter.drawRoundedRect(rect, rBound, rBound)
    
    def addCard(self, i, pos):
        self.index.append(i)
        card[i].setAnchorPoint(pos)
        card[i].setParentItem(self)
        card[i].setIndex(-1)
        self.nCard += 1
        self.somme += card[i].valeur
#------------------------------------------------------------------------------------------------------
# User's cards drop zone
#------------------------------------------------------------------------------------------------------
class UserSide(Side):
    
    Type = userType + 3
    
    def __init__(self, numero, parent=None):
        super().__init__(numero, user_side_color0, user_side_color1, user_side_pen, parent)
        
    def addCard(self, i):
        pos = QPointF(3, 3 + self.nCard*card_height*0.32)
        Side.addCard(self, i, pos)
        card[i].setPos(pos)
#------------------------------------------------------------------------------------------------------
# Automate's cards zone
#------------------------------------------------------------------------------------------------------
class AutoSide(Side):
    
    Type = userType + 4
    
    def __init__(self, numero, parent=None):
        super().__init__(numero, auto_side_color0, auto_side_color1, auto_side_pen, parent)

    def addCard(self, i):
        pos = QPointF(3, 3 + (2-self.nCard)*card_height*0.32)
        #card[i].moveTo(card[i].pos(),pos)
        Side.addCard(self, i, pos)
        stats.addCardToAutoSide(self)
#------------------------------------------------------------------------------------------------------
# player's playmat
#------------------------------------------------------------------------------------------------------
class PlayerDeck(QGraphicsItem):
        
    def __init__(self, color1, color2, color3, parent=None):
        super().__init__(parent)
        self.gcolor1 = color1
        self.gcolor2 = color2
        self.pcolor  = color3
        self.width = 1.0 * (N_hand*(card_width+marge) + marge)
        self.height = card_height + marge*2.0
    
    def boundingRect(self):
        return QRectF(-pen_width/2, -pen_width/2, self.width+pen_width, self.height+pen_width)
    
    def paint(self, painter, option, widget):
        gradient = QLinearGradient(0., side_height, 0., 0.)
        gradient.setSpread(QLinearGradient.ReflectSpread)
        gradient.setColorAt(0, self.gcolor1)
        gradient.setColorAt(1, self.gcolor2)
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(self.pcolor, 1))
        rect = QRectF(0., 0., float(self.width), float(self.height))
        painter.drawRoundedRect(rect, rBound, rBound)
#------------------------------------------------------------------------------------------------------
# Statistics
#------------------------------------------------------------------------------------------------------
class Stats:

    auto_lh  = [] # index where there is a card in the hand
    auto_ls  = [] # index where there is a place or more in the side
    auto_ls0 = [] # index where there is no card in the side
    auto_ls1 = [] # index where there is one only card in the side
    auto_ls2 = [] # index where there are two cards in the side
    user_lh  = []
    user_ls  = []
    
    def __init__(self):
        global auto_lh, auto_ls, auto_ls0, auto_ls1, auto_ls2, user_lh, user_ls
        
        # record for indexes avaiable
        
        auto_lh  = [0, 1, 2, 3, 4, 5]
        auto_ls  = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        auto_ls0 = [0, 1, 2, 3, 4, 5, 6, 7, 8]     
        auto_ls1 = []
        auto_ls2 = []
        user_lh  = [0, 1, 2, 3, 4, 5]
        user_ls  = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        
        # data for cards played
    
        self.cjc = [[colors[0], 0], [colors[1], 0], [colors[2], 0],
                    [colors[3], 0], [colors[4], 0], [colors[5], 0]]
    
        self.cjv = [range(9), 0]
        self.cjn = 0
    
        # data for cards in the deck or in the other hand
    
        self.csc = [[colors[0], 9], [colors[1], 9], [colors[2], 9],
                    [colors[3], 9], [colors[4], 9], [colors[5], 9]]
        self.csv = [range(9), 6]
        self.csn = 54

    def autoLh(self):
        global auto_lh
        return auto_lh

    def autoLs(self):
        global auto_ls
        return auto_ls
    
    def autoLs0(self):
        global auto_ls0
        return auto_ls0   

    def autoLs1(self):
        global auto_ls1
        return auto_ls1
    
    def autoLs2(self):
        global auto_ls2
        return auto_ls2
    
    def removeAutoHand(self, index):
        global auto_lh
        for i in range(len(auto_lh)):
            if auto_lh[i] == index:
                del auto_lh[i]
                break

    def addCardToAutoSide(self, side):
        global side_nb,auto_ls,auto_ls0,auto_ls1,auto_ls2

        if side.nCard == 1:
            auto_ls1.append(side_nb)
            auto_ls1.sort()
            for i in range(len(auto_ls0)):
                if auto_ls0[i] == side_nb:
                    del auto_ls0[i]
                    break

        elif side.nCard == 2:
            for i in range(len(auto_ls1)):
                if auto_ls1[i] == side_nb:
                    del auto_ls1[i]
                    break
            
            auto_ls2.append(side_nb)
            auto_ls2.sort()
            
        else:
            for i in range(len(auto_ls)):
                if auto_ls[i] == side_nb:
                    del auto_ls[i]
                    break

            for i in range(len(auto_ls2)):
                if auto_ls2[i] == side_nb:
                    del auto_ls2[i]
                    break
#------------------------------------------------------------------------------------------------------
class Memo:
    def __init__(self, hand, side, cote):
        self.hand = hand
        self.side = side
        self.cote = cote

#------------------------------------------------------------------------------------------------------
# Generic clickable button
#------------------------------------------------------------------------------------------------------
class Clickable(QGraphicsPixmapItem):
    
    def __init__(self, file, width, height, num, parentItem=None, back=False):
        super().__init__()
        
        image = Image.open('images/'+file)
        if back:
            back_img = Image.new("RGB", (image.size[0],image.size[1]), (222,222,222))
            image = Image.composite(image, back_img, image)

        image.thumbnail((width,height))
        self.setPixmap(QPixmap.fromImage(enluminure(image)))
        self.id = num
        self.setParentItem(parentItem)
        self.setAcceptHoverEvents(True)
        
        self.ombrage = Ombrage()
        self.setGraphicsEffect(self.ombrage)
        
    def hoverEnterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        self.anchorPoint = self.pos()
        self.setPos(self.x()-2, self.y()-2)
        self.ombrage.setEnabled(True)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.setPos(self.anchorPoint)
        self.ombrage.setEnabled(False)
        
    def mousePressEvent(self, event):
        global clicked
        if not event.button() == Qt.LeftButton:
            return

        clicked = True

    def mouseReleaseEvent(self, event):
        global selected
        if clicked:
            selected = self.id
            self.ombrage.setColor(ombrage_color_bt)

    def width(self):
        return self.boundingRect().width()
    
    def height(self):
        return self.boundingRect().height()
#------------------------------------------------------------------------------------------------------
# Slider's button
#------------------------------------------------------------------------------------------------------
class Handler(QGraphicsItem):
    moved = False
    
    def __init__(self, parentItem):
        super().__init__()
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setParentItem(parentItem)
        self.anchorPoint = QPointF()
        
        self.r = self.parentItem().r
        self.xmin = self.parentItem().x()
        self.xmax = self.xmin + self.parentItem().boundingRect().width()

    def setPosition(self, x, y):
        self.setPos(x, y)
        self.anchorPoint = self.pos()
        
    def hoverEnterEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)
        
    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        
    def mousePressEvent(self, event):
        global clicked
        if not event.button() == Qt.LeftButton:
            return
        clicked = True

    def mouseMoveEvent(self, event):
        # ensure it's a legal move
        if clicked:
            xh = event.pos().x()
            yh = self.anchorPoint.y()
            
            if xh < self.xmin:
                xh = self.xmin
            if xh > self.xmax:
                xh = self.xmax
            
            self.setPos(xh,yh)
    
    def boundingRect(self):
        penWidth = 1.0
        return QRectF(-penWidth/2, -penWidth/2, 2*self.r+penWidth, 2*self.r+penWidth)
    
    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.parentItem().colorBack)
        r = 2 * int(self.r)
        painter.drawEllipse(0, 0, r, r)         
#------------------------------------------------------------------------------------------------------
# Generic slider
#------------------------------------------------------------------------------------------------------
class Slider(QGraphicsItem):
    
    mini = 0
    maxi = 1
    nStep = 1
    singleStep = 1
    sliderPosition = 0
    relief_offset = 3.
    r = 5.
    
    colorBack  = QColor(53,53,43,255)
    colorLeft  = QColor(170,28,0,255)
    colorRight = QColor(110,157,0,255)
    brush      = QColor(255,85,0,255)
    pen        = QColor(21,11,127,255)
    
    def __init__(self, parentItem, title, npos=2, legend=['off','on']):
        super().__init__()

        self.nStep = npos
        self.sliderHeight = 15.
        self.stepWidth    = 40.
        self.sliderWidth  = self.stepWidth*(npos-1) + 2*self.r
        self.setParentItem(parentItem)
        self.setAcceptHoverEvents(True)

        self.xpos = [self.stepWidth*i for i in range(npos)]

        # legend
        
        font = QFont("Helvetica [Cronyx]", 15)
        font.setStretch(150)
        
        self.legend = [QGraphicsSimpleTextItem(legend[i]) for i in range(npos)]
        
        for i in range(npos):
            self.legend[i].setFont(font)
            self.legend[i].setBrush(self.brush)
            self.legend[i].setPen(self.pen)
            self.legend[i].setParentItem(self)
        
        if npos > 2:
            ym = self.y() - self.legend[0].boundingRect().height() - self.r
            for i in range(npos):
                xm = self.x() + i*self.stepWidth - self.legend[i].boundingRect().width()
                self.legend[i].setPos(xm,ym)
        else:
            ym = self.y()
            xm = self.x() - self.legend[0].boundingRect().width() - self.r
            self.legend[0].setPos(xm,ym)
            xm = self.x() + self.boundingRect().width() + self.r
            self.legend[1].setPos(xm,ym)
        
        # title
        
        font = QFont("Helvetica [Cronyx]", 25)
        font.setStretch(150)
        
        self.title = QGraphicsSimpleTextItem(title)
        self.title.setFont(font)
        self.title.setBrush(self.brush)
        self.title.setPen(self.pen)
        self.title.setParentItem(self)
        xm = (self.boundingRect().width() - self.title.boundingRect().width())/2
        ym = -self.legend[0].boundingRect().height() - 20 - self.title.boundingRect().height()
        self.title.setPos(xm,ym)

        # handler
        
        self.handler = Handler(self)
        
        # Setting non focus opacity
        
        self.setOpacity(0.8)
        
        # dimensions
        
        wl = self.legend[npos-1].x()+self.legend[npos-1].boundingRect().width() - self.legend[0].x()
        
        self.width = max(wl, self.title.boundingRect().width())
        
        self.height = self.boundingRect().height() - ym

    def setSliderPosition(self, i):
        self.sliderPosition = i
        x = self.x() + i*self.stepWidth
        y = self.y() + 3
        self.handler.setPosition(x,y)

    def setRange(self, i, j):
        self.mini = i
        self.maxi = j
        self.setSingleStep()

    def setSingleStep(self):
        self.singleStep = (self.maxi - self.mini)/self.nStep

    def value(self):
        return self.mini + self.sliderPosition*self.singleStep

    def boundingRect(self):
        return QRectF(-pen_width/2, -pen_width/2, self.sliderWidth+pen_width, self.sliderHeight+pen_width)
    
    def paint(self, painter, option, widget):
        # assembly of 3 roundedRects
        
        painter.setBrush(QBrush(self.colorBack))
        painter.setPen(QPen(self.pen, 1))
        rect = QRectF(0., 0., float(self.sliderWidth), float(self.sliderHeight))
        painter.drawRoundedRect(rect, self.r, self.r)
        
        painter.setBrush(QBrush(self.colorLeft))
        painter.setPen(Qt.NoPen)
        rect = QRectF(self.relief_offset, self.relief_offset, self.handler.x()+self.handler.boundingRect().width(), float(self.sliderHeight))
        painter.drawRoundedRect(rect, self.r, self.r)
        
        painter.setBrush(QBrush(self.colorRight))
        painter.setPen(Qt.NoPen)   
        rect = QRectF(self.handler.x(), 0., float(self.sliderWidth), float(self.sliderHeight))
        painter.drawRoundedRect(rect, self.r, self.r)
    
#    def setOn(self):
        # Brighter and colorful button if "on" chosen in "on/off" case

    def hoverEnterEvent(self, event):
        # Highlight the button if mouse's incoming or rectangle plus clair...
        self.setOpacity(1.0)
        
    def hoverLeaveEvent(self, event):
        # Normal rendering if mouse's leaving
        self.setOpacity(0.8)
        
    def mousePressEvent(self, event):
        # valide le click
        global clicked
        if not event.button() == Qt.LeftButton:
            return
        self.setCursor(Qt.ClosedHandCursor)
        clicked = True
        
    def mouseReleaseEvent(self, event):
        # et renvoie cette position dans sliderPosition
        # if on/off case, change state on click
        global clicked
        
        if clicked:
            
            # set the position to the nearest slot
            
            xh = self.pos().x()

            dx1 = abs(xh - self.xpos[0])            
            for i in range(self.nStep-1):
                dx2 = abs(xh - self.xpos[i+1])
                if dx1 > dx2:
                    self.handler.setPosition(self.xpos[i], self.handler.pos().y())
                    break
                else:
                    self.handler.setPosition(self.xpos[i+1], self.handler.pos().y())
                    break
                
                dx1 = dx2
                
            clicked = False

#------------------------------------------------------------------------------------------------------
# curtain for transition
#------------------------------------------------------------------------------------------------------
class Curtain(QGraphicsObject):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVisible(False)
        self.setPos(0,0)

    def boundingRect(self):
        penWidth = 2.0
        return QRectF(-penWidth/2, -penWidth/2, mainWindow_width+penWidth, mainWindow_height+penWidth)
    
    def paint(self, painter, option, widget):
        gradient = QLinearGradient(0., side_height, 0., 0.)
        gradient.setSpread(QLinearGradient.ReflectSpread)
        gradient.setColorAt(0, QColor(0,85,127,255))
        gradient.setColorAt(1, QColor(0,37,54,255))
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(68,68,68,255), 2))
        rect = QRectF(0., 0., float(mainWindow_width), float(mainWindow_height))
        painter.drawRoundedRect(rect, rBound, rBound)

    def animate_incoming(self):
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(800)
        self.anim.setStartValue(QPointF(0,-self.boundingRect().height()))
        self.anim.setEndValue(QPointF(0,0))
        self.setVisible(True)
        self.anim.start()

    def animate_leaving(self):
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(800)
        self.anim.setStartValue(QPointF(0,0))
        self.anim.setEndValue(QPointF(0,-self.boundingRect().height()))
        self.anim.finished.connect(self.remove)
        self.anim.start()
        
    def remove(self):
        self.setVisible(False)

#------------------------------------------------------------------------------------------------------
# chifoumi to know who's beggining
#------------------------------------------------------------------------------------------------------
class Chifoumi(Curtain):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # prepare geometry
        
        ww = self.boundingRect().width()
        wh = self.boundingRect().height()
        cw = card_height
        ew = 20
        
        # set the items
        
        self.interro = QGraphicsPixmapItem()   
        image = Image.open('images/interrogation.jpg')
        image.thumbnail((cw,cw))
        self.guess = QPixmap.fromImage(enluminure(image))
        self.interro.setPixmap(self.guess)
        self.interro.setParentItem(self)
        
        self.pierre  = Clickable('pierre.jpg', cw, cw, 2, self)
        self.ciseaux = Clickable('ciseaux.jpg', cw, cw, 1, self)
        self.feuille = Clickable('feuille.jpg', cw, cw, 0, self)
                
        self.sep = QGraphicsLineItem()
        self.sep.setPen(QPen(QColor(68,68,68,255), 2))
        self.sep.setParentItem(self)

        self.text1 = TextInForeground("Choose your hand !", self)
        self.text1.setVisible(False)
        self.text2 = TextInForeground("Tie !!\n\n", self)
        self.text2.setVisible(False)
        
        # continue geometry
        
        cw = self.feuille.width()
        ch = self.feuille.height()
        lw = 3*(ew+cw)
        lh = 2*ew

        # set the scene
        
        self.sep.setLine((ww-lw)/2, wh/2, (ww+lw)/2, wh/2)
        self.interro.setPos((ww-cw)/2, wh/2-ch-lh)
        self.pierre.setPos((ww-3*cw)/2-ew, wh/2+lh)
        self.ciseaux.setPos((ww-cw)/2, wh/2+lh)
        self.feuille.setPos((ww+cw)/2+ew, wh/2+lh)

    def start(self):
        self.text1.setVisible(True)
        
    def restart(self):
        self.text2.setVisible(True)
        self.interro.setPixmap(self.guess)
        QTimer.singleShot(3000, self.restart_countdown)
    
    def restart_countdown(self):
        self.text2.setVisible(False)
        self.start()
    
    def choosePlayer(self):
        global player_1
        
        # User's choice
            
        self.text1.setVisible(False)
        self.text2.setVisible(False)
            
        autoc = randint(0,2)

        # showing auto's choice
            
        if autoc == 0:
            self.interro.setPixmap(self.feuille.pixmap())
        elif autoc == 1:
            self.interro.setPixmap(self.ciseaux.pixmap())
        else:
            self.interro.setPixmap(self.pierre.pixmap())
                
        # verdict
                
        if selected == autoc:
            player_1 = -1
            return
        elif (selected == 0 and autoc == 2) \
        or   (selected == 1 and autoc == 0) \
        or   (selected == 2 and autoc == 1):
            player_1 = 0
        else:
            player_1 = 1

    def freeze(self):
        self.pierre.setAcceptHoverEvents(False)
        self.ciseaux.setAcceptHoverEvents(False)
        self.feuille.setAcceptHoverEvents(False)
#------------------------------------------------------------------------------------------------------
# Control panel
#------------------------------------------------------------------------------------------------------
class Settings(Curtain):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # prepare geometry
        
        ww = self.boundingRect().width()
        #wh = self.boundingRect().height()
        lw = int(ww/4)
        mh = 20
        
        # Set title
        
        self.title = TextInForeground("SETTINGS",self)
        
        # Set selectors
        
        self.sound_selector      = Slider(self, 'Sound')
        self.variant_selector    = Slider(self, 'Variant')
        self.difficulty_selector = Slider(self, 'Difficulty', 2, ['dumb','spicy'])
        self.rounds_selector     = Slider(self, 'Number of rounds', 5, ['1','2','3','4','5'])
        
        self.rounds_selector.setRange(1,5)
        
        if sounds:
            self.sound_selector.setSliderPosition(1)
            
        if variant:
            self.variant_selector.setSliderPosition(1)
            
        self.difficulty_selector.setSliderPosition(difficulT)
        self.rounds_selector.setSliderPosition(N_rounds-1)
        
        # Set "OK" and "CANCEL" buttons
        
        self.ok = Clickable('ok.png', 50, 50, 20, self, True)
        self.cancel = Clickable('cancel.png', 50, 50, 21, self, True)
        
        # Set the scene
        
        y = mh
        self.title.setPos(lw,y)
        y += mh + self.title.boundingRect().height() + 60
        self.sound_selector.setPos(lw,y)
        y += mh + self.sound_selector.height
        self.difficulty_selector.setPos(lw,y)
        y += mh + self.difficulty_selector.height
        self.rounds_selector.setPos(lw,y)
        y += mh + self.rounds_selector.height
        self.variant_selector.setPos(lw,y)
        y += mh + self.variant_selector.height
        self.ok.setPos(lw,y)
        self.cancel.setPos(lw+self.difficulty_selector.width,y)

    def setValues(self):
        global N_rounds, sounds, difficulT
        N_rounds  = self.rounds_selector.value()
        sounds    = self.sound_selector.value() == 1
        difficulT = self.difficulty_selector.value()            

#------------------------------------------------------------------------------------------------------
# Home panel
#------------------------------------------------------------------------------------------------------
class Home(Curtain):
        
    def __init__(self, parent=None):
        super().__init__(parent)

        # prepare geometry
        
        ww = self.boundingRect().width()
        wh = self.boundingRect().height()
        cw = 2*card_height
        ew = 80

        # title

        self.titre = QGraphicsPixmapItem()
        image = Image.open('images/titre.png')
        image.thumbnail((2*cw,2*cw))
        self.titre.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
        self.titre.setParentItem(self)

        # settings and starting button

        self.settings = Clickable('engrenages.jpg', cw, cw, 10, self)
        self.starting = Clickable('run.jpg', cw, cw, 11, self)
        
        # settings panel item
        
        self.settings_panel = Settings()
        self.settings_panel.setParentItem(self)
        self.settings_panel.setVisible(False)

        # continue geometry
        
        cw = self.settings.boundingRect().width()
        #ch = self.settings.boundingRect().height()

        # set the scene
        
        self.titre.setPos((ww-self.titre.boundingRect().width())/2, wh/2-ew-self.titre.boundingRect().height())
        self.settings.setPos(ww/2-ew-cw, wh/2+ew)
        self.starting.setPos(ww/2+ew, wh/2+ew)

    def setValues(self):
        self.settings_panel.setValues()
        self.closeSettings()
        
    def closeSettings(self):
        self.settings_panel.animate_leaving()

    def openSettings(self):
        self.settings_panel.setVisible(True)
        self.settings_panel.animate_incoming()

#------------------------------------------------------------------------------------------------------
# Game definition
#------------------------------------------------------------------------------------------------------
class Game(QGraphicsView):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # initialize private variables
        
        self.user_score = 0
        self.auto_score = 0
        self.i_round    = 0
        
        # Preset the scene and the view

        self.board = QGraphicsScene(self)
        self.board.setSceneRect(0, 0, mainWindow_width-40, mainWindow_height-60)
        
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
        
        if self.i_round == N_rounds:
            self.home.setVisible(True)
            self.home.animate_incoming()
            return
        
        # starting the game
        
        self.itemsSelected = []
        self.i_round += 1

        # Switch the first player between each round
        
        global player_1
        
        if self.i_round > 1:
            if player_1 == 0:
                player_1 = 1
            else:
                player_1 = 0

        # Set the board

        self.deck = Deck()
        self.setupHands()
        self.setupBoard()
  
        self.ending = False
        
        global stats
        stats = Stats()

    def setupHands(self):
        """
        Create players' hands
        """
        self.user_hand = []
        self.auto_hand = []
        self.new_order = []

        for i in range(N_hand):
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
            x = i*stone_marge + i*stone_width + mainWindow_marge
            y = mainWindow_marge + stone_height + stone_marge
            self.auto_side[i].setPos(x, y)
            y += side_height + stone_marge
            self.stone[i].setPos(x-2, y-2)
            y += stone_height + stone_marge
            self.user_side[i].setPos(x, y)

        # User's hand cards items

        self.user_deck = PlayerDeck(user_side_color0, user_side_color1, user_side_pen)

        for i in range(N_hand):
            card[self.user_hand[i]].setParentItem(self.user_deck)
            card[self.user_hand[i]].setPos((i+1)*marge+i*card_width, marge)
            card[self.user_hand[i]].setAnchorPoint(card[self.user_hand[i]].pos())
            card[self.user_hand[i]].setDraggable(True)
            card[self.user_hand[i]].setVisible(True)
            card[self.user_hand[i]].setIndex(i)

        # Computer's hand cards items [CHEAT MODE]

        self.auto_deck = PlayerDeck(auto_side_color0, auto_side_color1, auto_side_pen)

        for i in range(N_hand):
            card[self.auto_hand[i]].setParentItem(self.auto_deck)
            card[self.auto_hand[i]].setPos((i+1)*marge+i*card_width, marge)
            card[self.auto_hand[i]].setAnchorPoint(card[self.auto_hand[i]].pos())
            card[self.auto_hand[i]].setVisible(True)
        
        self.auto_deck.setScale(0.6)
        
        # Set items positions

        bottom_y = mainWindow_height - 5*mainWindow_marge - card_height - 2*marge

        self.deck.setPosInit(1000,bottom_y)
        self.user_deck.setPos(10,bottom_y)
        self.auto_deck.setPos(400,10)
        
        # Game board assembly
       
        self.board.addItem(self.deck)
        
        for i in range(9):
            self.board.addItem(self.auto_side[i])
            self.board.addItem(self.user_side[i])
            self.board.addItem(self.stone[i])
            
        self.board.addItem(self.user_deck)

         # Set zValue max
        
        global z_max

        z_max = 0.        
        for item in self.board.items():
            z_max = max(z_max, item.zValue())

    def autoHandView(self):
        """
        Showing computer's hand cards in a subwindow
        """
        self.board.addItem(self.auto_deck)
        
    def autoHandClose(self):
        self.board.removeItem(self.auto_deck)

    def mouseMoveEvent(self, event):
        QGraphicsView.mouseMoveEvent(self, event)

        if dragged:

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
                    
            # Management for reardering the user's hand
            
            #self.mouseMoveHand()

    def mouseMoveHand(self):
        """
        Reorganization of the user's hand
        """
        global userWantToReorganize, card_hover, card_dx
        
        userWantToReorganize = False
        card_hover = -1

        colItems = card[card_nb].collidingItems()
        
        if colItems:
            shortestDist = 100000.
            for item in colItems:

                if item == card[card_nb].parentItem():
                    continue
                
                if item.parentItem() == card[card_nb].parentItem():
                    line = QLineF(item.sceneBoundingRect().center(),
                                  card[card_nb].sceneBoundingRect().center())
                    if line.length() < shortestDist:
                        shortestDist = line.length()
                        #if card_hover != item.numero or card_dx*line.dx() < 0:
                        userWantToReorganize = True
                            
                        card_dx = line.dx()
                        card_hover = item.numero


        if userWantToReorganize:
            self.new_order = self.user_hand
        else:
            return
        
        # Set the concerned cards

        if card[card_nb].index - card[card_hover].index < 0:
            i1 = card[card_nb].index+1
            i2 = card[card_hover].index
            sens = -1
            if card_dx > 0:
                i2 += 1
        else:
            i1 = card[card_hover].index
            i2 = card[card_nb].index
            sens = 1
            if card_dx > 0:
                i1 += 1        

        # Set the animation moving concerned cards

        self.anims = QParallelAnimationGroup()

        for i in range(i1,i2):
            anim = QPropertyAnimation(card[self.user_hand[i]], b"pos")
            pos1 = card[self.user_hand[i]].anchorPoint
            pos2 = card[self.user_hand[i+sens]].anchorPoint
            dx = pos1.x() - pos2.x()
            dy = pos1.y() - pos2.y()
            duration = sqrt(dx**2 + dy**2) / 1
            anim.setDuration(duration)
            anim.setStartValue(pos1)
            anim.setEndValue(pos2)
            self.anims.addAnimation(anim)
            self.new_order[i+sens] = self.user_hand[i]

        self.anims.start()

    def mouseReleaseEvent(self, event):
        global side_nb, card_nb, dragged
        
        QGraphicsView.mouseReleaseEvent(self, event)

        # Events from Cards: If cards has been moved to a droppable zone

        if dragged:
            
            # Card moved on user's deck
            
            if userWantToReorganize:
                self.user_hand = self.new_order
                    
            # Card moved on side or no ?
                    
            if side_nb >= 0:

                # position in the hand
                
                i = card[card_nb].index

                # Memorize initial position for new card from the deck

                pos = card[card_nb].anchorPoint
                
                 # Add the card drop to the side

                self.user_side[side_nb].addCard(card_nb)
                self.user_side[side_nb].setOpacity(0.5)

                # Draw a new card    

                if self.deck.isEmpty():
                    self.user_hand[i] = -1
                    if sum(self.user_hand) == -6:
                        self.ending = True
                else:
                    self.user_hand[i] = self.deck.draw()
                    card[self.user_hand[i]].setVisible(True)
                    card[self.user_hand[i]].setDraggable(True)
                    card[self.user_hand[i]].setAnchorPoint(pos)
                    card[self.user_hand[i]].moveTo(self.deck.pos() - self.user_deck.pos(), pos)
                    card[self.user_hand[i]].setParentItem(self.user_deck)
                    card[self.user_hand[i]].setIndex(i)

                # Actions if the side is full

                if self.user_side[side_nb].nCard == 3:
                    self.book(self.user_side[side_nb])
                    
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
                card[card_nb].moveTo(card[card_nb].pos(),card[card_nb].anchorPoint)

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

    #--------------------------------------------------------------------------------------------------
    # Leave chifoumi curtain and launch the game
    #--------------------------------------------------------------------------------------------------
    def letsGo(self):
        self.text.setVisible(False)
        self.chifoumi.animate_leaving()
        self.home.animate_leaving()
        self.newRound()
    #--------------------------------------------------------------------------------------------------
    # Choose the automate and play the card on the side
    #--------------------------------------------------------------------------------------------------
    def automate(self):
        global side_nb, card_nb, hand_nb

        if difficulT == 1:
            self.cervo1()            
        else:            
            self.cervo0()
            
        # move the card and draw a new one

        card_nb = self.auto_hand[hand_nb]        
        pos = card[card_nb].anchorPoint
        self.auto_side[side_nb].addCard(card_nb)
        pos0 = self.auto_deck.pos() - self.auto_side[side_nb].pos() + pos
        card[card_nb].moveTo(pos0,card[card_nb].anchorPoint)
        
        if self.deck.isEmpty():
            self.auto_hand[hand_nb] = -1
            stats.removeAutoHand(hand_nb)
            if sum(self.auto_hand) == -6:
                    self.ending = True
        else:
            self.auto_hand[hand_nb] = self.deck.draw()
            card[self.auto_hand[hand_nb]].setVisible(True)
            card[self.auto_hand[hand_nb]].setParentItem(self.auto_deck)
            card[self.auto_hand[hand_nb]].setAnchorPoint(pos)
            card[self.auto_hand[hand_nb]].setPos(pos)
    #--------------------------------------------------------------------------------------------------
    # Automate 0 : random card and random stone
    #--------------------------------------------------------------------------------------------------
    def cervo0(self):
        global side_nb, hand_nb
        hand_nb = choice(stats.autoLh())
        side_nb = choice(stats.autoLs())
    #--------------------------------------------------------------------------------------------------
    # Automate 1 : first steps choice
    #--------------------------------------------------------------------------------------------------
    def cervo1(self):
        global side_nb, hand_nb

        # Settings for memorization of relevant combinations
        
        memo = []

        # Setting cards color and valor in lists

        v = [0 for i in range(6)]
        c = ["0" for i in range(6)]

        for i in stats.autoLh():
            v[i] = card[self.auto_hand[i]].valeur
            c[i] = card[self.auto_hand[i]].couleur
            
        # 1 Looking in the hand

        for i in stats.autoLh():            
            for j in stats.autoLh():
                if i != j:
                    
                    dvij = v[i]-v[j]
                
                    # For flush pair(s)
                
                    if c[i] == c[j] and dvij < 3 and dvij > -3:
                        for k in stats.autoLs1():
                            if c[i] == card[self.auto_side[k].index[0]].couleur:
                                dvik = v[i] - card[self.auto_side[k].index[0]].valeur
                                if (dvij ==  2 and dvik ==  1) \
                                or (dvij == -2 and dvik == -1) \
                                or (dvij ==  1 and dvik ==  2) \
                                or (dvij == -1 and dvik == -2):
                                    memo.append(Memo(i, k, cote_both))

                    # For pair(s)
                            
                    if dvij == 0:
                        for k in stats.autoLs1():
                            if v[i] == card[self.auto_side[k].index[0]].valeur:
                                    memo.append(Memo(i, k, cote_brelan))
                
        #2 Search in the sides with 2 cards

        for i in stats.autoLh():
            for k in stats.autoLs2():
                
                dvij = v[i] - card[self.auto_side[k].index[0]].valeur
                dvik = v[i] - card[self.auto_side[k].index[1]].valeur

                lcolor = (c[i] == card[self.auto_side[k].index[0]].couleur \
                          and c[i] == card[self.auto_side[k].index[1]].couleur)
                       
                lsuite = ((dvij == -1 and dvik == -2) \
                          or (dvij == -2 and dvik == -1) \
                          or (dvij ==  1 and dvik == -1) \
                          or (dvij == -1 and dvik ==  1) \
                          or (dvij ==  2 and dvik ==  1) \
                          or (dvij ==  1 and dvik ==  2))
                
                # Test if a card in the hand goes to flush third
                
                if lcolor and lsuite:
                    memo.append(Memo(i, k, cote_both*1.5))

                # Test if a card in the hand goes to 3 of a kind
                
                if dvij == 0 and dvik == 0:
                    memo.append(Memo(i, k, cote_brelan*1.5))

                # Test if a card in the hand goes to color
                
                if lcolor:
                    memo.append(Memo(i, k, cote_couleur))
                
                # Test if a card in the hand goes to suite

                if lsuite:
                    memo.append(Memo(i, k, cote_suite))
                
        #3 Search in the sides with 1 card

        for i in stats.autoLh():                
            for k in stats.autoLs1():

                dvij = v[i] - card[self.auto_side[k].index[0]].valeur

                lcolor = (c[i] == card[self.auto_side[k].index[0]].couleur)
                lsuite = (dvij == -1 or dvij == -2 or dvij == 1 or dvij == 2)
                
                # Test if a card of the hand matchs for flush third
        
                if lcolor and lsuite:
                    memo.append(Memo(i, k, cote_both))
                
                # Test if a card of the hand matchs for 3 of a kind
                
                if dvij == 0:
                    memo.append(Memo(i, k, cote_brelan/1.5))

                # Test if a card of the hand matchs for color
                
                if lcolor:
                    memo.append(Memo(i, k, cote_couleur/1.5))
                
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
            
            hand_nb = memo[k].hand
            side_nb = memo[k].side
            return
        
        #4 Play a random card on a random free side
        
        if stats.autoLs0():
            side_nb = choice(stats.autoLs0())
            hand_nb = choice(stats.autoLh())
            return
        
        #5 Last call...
        
        self.cervo0()
        
    #--------------------------------------------------------------------------------------------------
    # Test after a third card has been played on a side
    #--------------------------------------------------------------------------------------------------
    def book(self,side):

        i = side.index[0]
        j = side.index[1]
        k = side.index[2]
        
        suite = False
        flush = False
        
        # test for straight =>  somme € [106; 124]
        
        liste = sorted([card[i].valeur, card[j].valeur, card[k].valeur])
        
        if liste[1] == liste[0]+1 and liste[2] == liste[1]+1:
            suite = True
            side.somme += cote_suite
            
        # test for flush => somme € [206; 324]
        
        if card[i].couleur == card[j].couleur == card[k].couleur:
            flush = True
            side.somme += cote_couleur

        # test for straight flush => somme € [506; 524]

        if suite and flush:
            side.somme += cote_both

        # test for three of a kind => somme € [403; 427]

        elif card[i].valeur == card[j].valeur == card[k].valeur:
            side.somme += cote_brelan
    #--------------------------------------------------------------------------------------------------
    # Compare sides and test for victory
    #--------------------------------------------------------------------------------------------------
    def judge(self):
        
        # if 3 cards have been played on each side, test for claim of the stone

        if self.user_side[side_nb].nCard == 3 and self.auto_side[side_nb].nCard == 3:
            if self.user_side[side_nb].somme > self.auto_side[side_nb].somme:
                self.stone[side_nb].winner = "user"
                self.stone[side_nb].moveStoneTo(side_height+6+stone_height)
            elif self.user_side[side_nb].somme < self.auto_side[side_nb].somme:
                self.stone[side_nb].winner = "auto"
                self.stone[side_nb].moveStoneTo(-side_height-6-stone_height)
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
                        self.stone[i].moveStoneTo(side_height+6+stone_height)
                    elif self.user_side[i].somme < self.auto_side[i].somme:
                        self.stone[i].winner = "auto"
                        self.stone[i].moveStoneTo(-side_height-6-stone_height)
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
                    ucount +=1

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
    #--------------------------------------------------------------------------------------------------
    # show the endround/endgame's message
    #--------------------------------------------------------------------------------------------------
    def victory(self, winner):
        
        # test who won
        
        if winner == "draw":
            text = "DRAW !!\n\nRESTARTING THE ROUND"
            self.i_round -= 1
        elif winner == "user":
            text = "YOU WON ROUND "+str(self.i_round)+" !!!"
            self.user_score += 1
        else:
            text = "AUTOMA WON ROUND "+str(self.i_round)+" !!!"
            self.auto_score += 1

        if self.i_round < N_rounds:
            text += "ROUND "+str(self.i_round)+" !!!"
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
        
        for i in range(N_cards):
            card[i].setDraggable(False)
            card[i].setZValue(0)
            
        QTimer.singleShot(3000, self.newRound)

#------------------------------------------------------------------------------------------------------
# Définition de la fenêtre principale de l'interface
#------------------------------------------------------------------------------------------------------
class GameWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setFixedSize(mainWindow_width, mainWindow_height)
        self.setWindowTitle('Schotten Totten')
        self.setWindowIcon(QIcon('images/logo.png'))

        # Setting all the playing cards

        global card
        for i in range(N_cards):
            card.append(Card(i))
        
        self.createGame()
        self.createMenu()
        self.show()

    def createMenu(self):
        """
        Create menubar and menu action
        """
        # Create actions for file menu
        self.exit_act = QAction(QIcon('images/exit.png'), 'Exit', self)
        self.exit_act.setShortcut('Ctrl+Q')
        self.exit_act.setStatusTip('Quit program')
        self.exit_act.triggered.connect(self.close)

        self.newGame_act = QAction(QIcon('images/logo.png'), 'New game', self)
        self.newGame_act.setShortcut('Ctrl+N')
        self.newGame_act.setStatusTip('Start a new game')
        self.newGame_act.triggered.connect(self.newGame)

        # Create actions for configuration menu
        self.level0 = QAction("stupid boy", self, checkable=True)
        self.level1 = QAction("lightning", self, checkable=True)
        self.level1.setChecked(True)
        self.level0.triggered.connect(self.setLevel0)
        self.level1.triggered.connect(self.setLevel1)

        self.sound_act = QAction('Play sounds', self, checkable=True)
        self.sound_act.setStatusTip('Play sounds in the game')

        self.round_nb = QAction('Rounds...\t ('+str(N_rounds)+')', self)
        self.round_nb.triggered.connect(self.setRounds)
        self.round_nb.setStatusTip('Set the number of rounds for a match')

        # Create actions for help menu
        self.rules_act = QAction(QIcon('images/help.png'), 'Rules', self)
        self.rules_act.setShortcut('F1')
        self.rules_act.setStatusTip('See the rules of Schotten Totten')
        self.rules_act.triggered.connect(self.showRules)
        
        self.about_act = QAction(QIcon('images/info.png'), 
                                 'About Schotten Totten...', self)
        self.about_act.triggered.connect(self.showInfo)

        # Create menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        
        # Create file menu and new game actions
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(self.newGame_act)
        file_menu.addAction(self.exit_act)
        
        # Create configuration menu
        config_menu = menu_bar.addMenu('&Config')
        level = config_menu.addMenu("Level")
        level.addAction(self.level0)
        level.addAction(self.level1)
        config_menu.addAction(self.sound_act)
        config_menu.addAction(self.round_nb)
        
        # Create help menu
        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(self.rules_act)
        help_menu.addAction(self.about_act)

        # Display info about actions in the status bar
        self.setStatusBar(QStatusBar(self))

    def setLevel0(self):
        global difficulT
        self.level0.setChecked(True)
        self.level1.setChecked(False)
        difficulT = 0

    def setLevel1(self):
        global difficulT
        self.level0.setChecked(False)
        self.level1.setChecked(True)
        difficulT = 1

    def setRounds(self):
        self.new_N_rounds = N_rounds
        
        self.rounds_window = QWidget()
        
        msg = QLabel("Define how many rounds must be won to take away the game\n", self)

        self.sbox = QSpinBox(self)
        self.sbox.setRange(1,10)
        self.sbox.setSingleStep(1)
        self.sbox.setValue(N_rounds)
        self.sbox.valueChanged.connect(self.newNRounds)
        
        okb = QPushButton("Ok", self)
        okb.clicked.connect(self.setNRounds)
        ccb = QPushButton("Cancel", self)
        ccb.clicked.connect(self.rounds_window.close)
        hbox = QHBoxLayout()
        hbox.addWidget(okb)
        hbox.addWidget(ccb)

        vbox = QVBoxLayout()
        vbox.addWidget(msg)
        vbox.addWidget(self.sbox)
        vbox.addLayout(hbox)

        self.rounds_window.setLayout(vbox)
        self.rounds_window.setGeometry(300,300,350,250)
        self.rounds_window.setWindowTitle("Setting number of rounds")
        self.rounds_window.show()

    def newNRounds(self):
        self.new_N_rounds = self.sbox.value()

    def setNRounds(self):
        global N_rounds
        if self.new_N_rounds != N_rounds:
            N_rounds = self.new_N_rounds
        self.rounds_window.close()

    def showRules(self):
        msg = "Les cartes Clan représentent les membres de votre tribu " \
            "écossaise que vous envoyez sur le terrain pour défendre les " \
            "Bornes. Chaque carte Clan existe en six couleurs différentes " \
            "et possède une force allant de 1 à 9 (1 étant la force la " \
            "plus faible)."
        
        helpBox = QMessageBox()
        helpBox.setIcon(QMessageBox.Question)
        helpBox.setWindowTitle("Les règles du jeu")
        helpBox.setText(msg)
        helpBox.setStandardButtons(QMessageBox.Ok)
        helpBox.exec_()

    def showInfo(self):
        QMessageBox.about(self, "About Schotten Totten",
                """<b> Schotten Totten</b> v %s
                <p>Adaptation of the cards game developped
                by Reiner Knizia et Djib
                <p>Copyright &copy; 2016-2019 IELLO for the 
                original cards game.
                <p>Copyright &copy; 2020 Philippe Régnier for
                this video game.""" % (__version__))

    def newGame(self):
        """
        Asking before creating a new game
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Are you sure you want to quit the " \
                    "current game and create a new one ?")
        msg.setWindowTitle("Warning !")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        returnValue = msg.exec()
        
        if returnValue == QMessageBox.Yes:
            self.createGame()
        else:
            pass
        
    def createGame(self):
        """
        Create a new Schotten Totten game
        """
        self.game = Game(self)
        self.setCentralWidget(self.game)
        
    def keyPressEvent(self, event):
        """
        Hidden short-cut pressed handler
        """
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_A:
                self.game.autoHandView()

    def keyReleaseEvent(self, event): # NOT WORKING !!!
        """
        Hidden short-cut release handler
        """
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_A:
                self.game.autoHandClose()
#------------------------------------------------------------------------------------------------------
# Lancement du jeu
#------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    sys.exit(app.exec_())
