# manager for the playing cards
# TODO: singleton

class Dealer:

    max_value = 9
    colors = ['jaune', 'vert', 'rouge', 'brun', 'bleu', 'violet']
    cards = []
    total_cards = len(colors) * max_value

    def __init__(self):

        # Setting all the playing cards

        for i in range(N_cards):
            Card.cards.append(Card(i))
        if numero < 0 or numero > Card.total_cards - 1:
            print("Card number must be into [0, 53]. Program stopped")
            sys.exit(0)