import player_choice
from hand import Hand, hand_comparison


def analyze_hand(player_hand, dealer_hand, wager, shoe, blackjack_value, dealer_hits_on_soft_17, double_after_split,
                 surrender_allowed, double_allowed):
    total_wager = 0
    hand_wager = wager
    winnings = 0

    dealer_hand.dealer_hit(shoe, replace=True, hit_on_soft_17=dealer_hits_on_soft_17)

    choice = ''
    while choice not in ('stand', 'surrender'):
        if player_hand.value == 'BUST':
            break
        is_double = (len(player_hand.cards) != len(set(player_hand.cards))) and len(player_hand.cards) == 2
        if player_hand.total == 3:
            print(player_hand, player_hand.total)
        choice = player_choice.get_player_decision(player_hand.total, dealer_hand.cards[0], player_hand.soft_aces > 0,
                                                   is_double, dealer_hits_on_soft_17)

        # Surrender Choice
        if choice in ('RP', 'RS', 'RH') and surrender_allowed:
            return wager, wager / 2
        # Split Choice
        if choice in ('P', 'PH', 'RP'):
            if double_after_split or choice == 'P' or choice == 'RP':
                new_hand = Hand(player_hand.remove_card())
                new_hand.add_card(shoe.get_random_card())
                player_hand.add_card(shoe.get_random_card())
                hand1_wager, hand1_winnings = analyze_hand(new_hand, dealer_hand, wager, shoe, blackjack_value,
                                                           dealer_hits_on_soft_17, double_after_split,
                                                           surrender_allowed, double_allowed)
                total_wager += hand1_wager
                winnings += hand1_winnings
                continue
        # Double Choice
        if choice in ('DH', 'DS') and double_allowed:
            player_hand.add_card(shoe.get_random_card())
            hand_wager += wager
            break
        if choice in ('H', 'DH', 'PH', 'RH'):
            player_hand.add_card(shoe.get_random_card())
            continue

        # Otherwise, stand
        break

    winnings += hand_wager * hand_comparison(player_hand, dealer_hand, True, True, blackjack_value)
    total_wager += hand_wager

    return total_wager, winnings
