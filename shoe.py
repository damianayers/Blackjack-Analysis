import random


class Shoe:
    def __init__(self, deck_count=1):
        cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        card_counts = {11: 4, 10: 16, 9: 4, 8: 4, 7: 4, 6: 4, 5: 4, 4: 4, 3: 4, 2: 4}
        self.shoe = [item for sublist in [[c] * card_counts[c] for c in cards] for item in sublist] * deck_count

    def remove(self, card):
        self.shoe.remove(card)

    def get_random_card(self):
        return random.choice(self.shoe)

    def draw_card(self):
        card = random.choice(self.shoe)
        self.shoe.remove(card)
        return card
