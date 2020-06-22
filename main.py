import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import pandas as pd

from math_analysis import run_analysis, run_sims

dealer_hits_on_soft_17 = True
double_after_split = True
surrender_allowed = False
double_allowed = True
blackjack_return = 2

params = {'Dealer Hits on Soft 17': dealer_hits_on_soft_17,
          'Double Allowed After Split': double_after_split,
          'Surrender Allowed': surrender_allowed,
          'Double Allowed': double_allowed,
          'Blackjack Payout': blackjack_return}


def create_group_plot():
    df = pd.read_csv('simulation results.csv')
    df2 = df[(df['RTP%'] < 1) & (df['RTP%'] > 0.96)]

    sns.set(style="whitegrid")

    g = sns.catplot(x='Blackjack Payout', y='RTP%', hue='Dealer Hits on Soft 17', col='Surrender Allowed',
                    row='Double Allowed After Split',
                    data=df2, kind='bar', ci=None)
    g._legend.remove()
    plt.ylim([0.96, 1])
    plt.show()


def create_single_plot():
    df = pd.read_csv('BJP 2 DAS 1 SA 1 sim results.csv')
    mean = df['RTP%'].mean()
    ax = sns.distplot(df['RTP%'], norm_hist=False, kde=True)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    ax.axvline(mean, color='red')

    plt.show()


def run_single_simulation():
    params['Double Allowed After Split'] = True
    params['Surrender Allowed'] = True
    params['Dealer Hits on Soft 17'] = False
    params['Blackjack Payout'] = 2
    df = pd.DataFrame()
    for i in range(1000):
        results = {**run_sims(200, params, 1, False), **params}
        df = df.append(results, ignore_index=True)

    return df


def run_multiple_simulations():
    file = open('simulation results.txt', 'w')
    df = run_analysis(params, 1000000, file=None)
    df.to_csv('simulation results.csv')
