import random


class Coin(object):

    def __init__(self):
        self.n_flips = 0
        self.heads = 0
        self.head_freq = 0
        self.tails = 0
        self.tail_freq = 0

    def flip(self):
        self.n_flips += 1
        if (random.uniform(0, 1) > 0.5):
            self.heads += 1
        else:
            self.tails += -1
        self.head_freq = float(self.heads) / self.n_flips
        self.tail_freq = float(self.tails) / self.n_flips


def flip_coins(n_flips, coins):
    for n in range(n_flips):
        for coin in coins:
            coin.flip()


def experiment(n_coins, n_flips):
    coins = [Coin() for x in range(n_coins)]
    flip_coins(n_flips, coins)
    c_rand = random.choice(coins)
    c_1 = coins[0]
    coins = sorted(coins, key=lambda coin: coin.head_freq)
    c_min = coins[0]
    return c_1, c_rand, c_min

n_runs = 10000
n_coins = 1000
n_flips = 10
c_1_total = 0
c_rand_total = 0
c_min_total = 0
for i in range(n_runs):
    print "Run {0}".format(i)
    c_1, c_rand, c_min = experiment(n_coins, n_flips)
    c_1_total += c_1.head_freq
    c_rand_total += c_rand.head_freq
    c_min_total += c_min.head_freq

print "c_1 average {0}".format(c_1_total / n_runs)
print "c_rand average {0}".format(c_rand_total / n_runs)
print "c_min average {0}".format(c_min_total / n_runs)
