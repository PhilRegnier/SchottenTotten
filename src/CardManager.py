# manager for the playing cards
# TODO: singleton
from src.Card import Card


class CardManager(Singleton):

    max_value = 9
    colors = ['jaune', 'vert', 'rouge', 'brun', 'bleu', 'violet']
    cards = []
    total_cards = len(colors) * max_value

    def __init__(self):

        # Setting all the playing cards

        for i in range(CardManager.total_cards):
            CardManager.cards.append(Card(i, CardManager.max_value))
