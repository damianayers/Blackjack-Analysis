import random
import player_choice


class Hand:
    def __init__(self, card1, card2=None):
        self.cards = [card1]
        if card2 is not None:
            self.cards.append(card2)
        self.total = sum(self.cards)
        self.value = self.total
        self.soft_aces = self.cards.count(11)
        self.check_values()

    def __str__(self):
        ret_val = '['
        for card in self.cards[:-1]:
            ret_val += str(card) + ', '
        ret_val += str(self.cards[-1]) + ']'

        return ret_val

    def check_values(self):
        if self.total > 21 and self.soft_aces > 0:
            self.total -= 10
            self.soft_aces -= 1
        if self.total == 1 and self.cards[0] == 11:
            self.soft_aces += 1
            self.total += 10
        if self.total == 21 and len(self.cards) == 2:
            self.value = 'BJ'
        elif self.total > 21:
            self.value = 'BUST'
        else:
            self.value = self.total

    def add_card(self, card):
        self.cards.append(card)
        self.total += card
        if card == 11:
            self.soft_aces += 1
        self.check_values()

    def remove_card(self):
        card = self.cards.pop()
        self.total -= card
        if card == 11:
            self.soft_aces -= 1
        self.check_values()
        return card

    def dealer_hit(self, shoe=None, replace=False, hit_on_soft_17=False):
        if shoe is None:
            while self.total < 17 or (hit_on_soft_17 and self.soft_aces > 0):
                self.add_card(random.randrange(2, 12))
        else:
            while self.total < 17 or (hit_on_soft_17 and self.soft_aces > 0):
                if replace:
                    self.add_card(shoe.get_random_card())
                else:
                    self.add_card(shoe.draw_card())

    def player_hit(self, shoe=None):
        if shoe is None:
            self.add_card(random.randint(2, 12))
        else:
            self.add_card(shoe.get_random_card())


def hand_comparison(player_hand, dealer_hand, push_on_tie=True, lose_on_dealer_bj=True, bj_value=2):
    # This method will return value earned
    if dealer_hand.value == 'BJ':
        return 0
    elif player_hand.value == 'BJ':
        return bj_value
    elif player_hand.value == 'BUST':
        return 0
    elif dealer_hand.value == 'BUST':
        return 2
    elif player_hand.value == dealer_hand.value:
        return 1
    elif player_hand.value > dealer_hand.value:
        return 2
    else:
        return 0
