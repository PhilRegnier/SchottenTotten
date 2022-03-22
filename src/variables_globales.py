#
# Variables globales (peut mieux faire...)
#
__version__ = "1.1"

# Game set
from PyQt5.QtGui import QColor

colors = ['jaune', 'vert', 'rouge', 'brun', 'bleu', 'violet']
max_value = 9
N_hand = 6
difficulT = 1
N_rounds = 1
sounds = False
variant = False

# Objects dimensions & geometries

mainWindow_width = 1200
mainWindow_marge = 20
pen_width = 1.
stone_marge = 4.
marge = 5.
stone_width = (mainWindow_width - 2 * mainWindow_marge - 8 * stone_marge - 40) / 9 - 2 * pen_width
stone_height = stone_width * 0.58
side_height = card_height * 1.667
mainWindow_height = int(
    4 * stone_height + 4.33 * card_height + mainWindow_marge * 2 + 8 * pen_width + 4 * stone_marge + 40)
rBound = 10.0

# Global variables managing scenography

parentId = 0
userType = 100000
clicked = False
selected = -1  # 0= feuille; 1=ciseaux; 2=pierre; 10=settings; 11=starting; 20=ok ; 21=cancel;
player_1 = 0  # O=user (default); 1=automate

# cotations for cards combinations

cote_suite = 100
cote_couleur = 200
cote_both = 200
cote_brelan = 400

# Colors

cadre_color = (57, 57, 57)
relief_color = (53, 53, 43, 255)
relief_color2 = (65, 71, 35, 255)
ombrage_color = QColor(36, 36, 36, 90)
ombrage_color_bt = QColor(36, 36, 36, 200)
background_color = QColor(167, 159, 120)

user_side_color0 = QColor(9, 18, 27, 90)
user_side_color1 = QColor(85, 170, 255, 90)
user_side_pen = QColor(85, 81, 44)
user_hand_color = QColor(85, 170, 255, 40)
user_hand_pen = QColor(10, 11, 8)

auto_side_color1 = QColor(255, 85, 0, 90)
auto_side_color0 = QColor(70, 23, 0, 90)
auto_side_pen = QColor(85, 81, 44)
auto_hand_color = QColor(49, 53, 42, 150)
auto_hand_pen = QColor(10, 11, 8)
