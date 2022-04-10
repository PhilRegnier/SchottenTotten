# class Hand to manage user's and automate's hands


class Hand:

    def __init__(self):
        self.card = []

    def add(self, card):
        if len(self.card) > .number_max_of_cards_in_hand:
            return False
        else:
            self.card.append(card)
            return True

    def remove(self, card):
        self.card.remove(card)

    def get(self, index):
        return self.card[index]

    def show(self):
        return self.card



