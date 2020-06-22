import math
import sys
import pandas as pd

from hand import Hand
from shoe import Shoe
from analyze_hand import analyze_hand


def get_variance(total_value, trials, total_value_squared):
    # Add real error checking or exception handling
    if trials == 1:
        return 0
    mean_squared = total_value * total_value / trials
    variance = (total_value_squared - mean_squared) / (trials - 1)
    return variance


def print_values(total_wagers, total_return, trials, total_squared, params=None, file=None):
    output = file or sys.stdout
    variance = get_variance(total_return, trials, total_squared)
    print('Wagers: ' + str(total_wagers), file=output)
    print('Return: ' + str(total_return), file=output)
    print('RTP%: ' + str(total_return / total_wagers), file=output)
    print('Hands Played: ' + str(trials), file=output)
    print('Std Dev: ' + str(math.sqrt(variance)), file=output)
    if params is not None:
        print(file=output)
        for key in params.keys():
            print(key, ':', params[key], file=output)
    print(file=output)


def get_values(total_wagers, total_return, trials, total_squared):
    variance = get_variance(total_return, trials, total_squared)
    return {'Wagers': total_wagers, 'Return': total_return, 'RTP%': total_return / total_wagers, 'Hands Played': trials,
            'Std Dev': math.sqrt(variance)}


def run_sims(num_hands, params, num_decks=1, print_results=True, file=None):
    dealer_hits_on_soft_17 = params['Dealer Hits on Soft 17']
    double_after_split = params['Double Allowed After Split']
    surrender_allowed = params['Surrender Allowed']
    double_allowed = params['Double Allowed']
    blackjack_return = params['Blackjack Payout']

    total_return = 0
    total_wagers = 0
    total_squared = 0

    shoe = Shoe(num_decks)

    for i in range(num_hands):
        player_hand = Hand(shoe.get_random_card(), shoe.get_random_card())
        dealer_hand = Hand(shoe.get_random_card())
        dealer_hand.dealer_hit(shoe, replace=True, hit_on_soft_17=False)

        new_wagers, new_winnings = analyze_hand(player_hand, dealer_hand, 1, shoe, blackjack_return,
                                                dealer_hits_on_soft_17,
                                                double_after_split, surrender_allowed, double_allowed)
        total_wagers += new_wagers
        total_return += new_winnings
        total_squared += new_winnings * new_winnings

    if print_results:
        print_values(total_wagers, total_return, num_hands, total_squared, params, file)
    return get_values(total_wagers, total_return, num_hands, total_squared)


def run_analysis(params, trials, file=None):
    df = pd.DataFrame()

    for bj_payout in [1.5, 2, 2.5]:
        params['Blackjack Payout'] = bj_payout
        for dealer_hits_on_17 in [True, False]:
            params['Dealer Hits on Soft 17'] = dealer_hits_on_17
            for surrender in [True, False]:
                params['Surrender Allowed'] = surrender
                for double_able in [True, False]:
                    params['Double Allowed After Split'] = double_able
                    if file is None:
                        results = {**run_sims(trials, params, print_results=False), **params}
                    else:
                        results = {**run_sims(trials, params, file=file), **params}
                    df = df.append(results, ignore_index=True)

    return df
