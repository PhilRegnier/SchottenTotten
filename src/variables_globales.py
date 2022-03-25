#
# Variables globales (peut mieux faire...)
#
__version__ = "1.1"

# Game set

colors = ['jaune', 'vert', 'rouge', 'brun', 'bleu', 'violet']


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

# cotations for cards combinations

cote_suite = 100
cote_couleur = 200
cote_both = 200
cote_brelan = 400


