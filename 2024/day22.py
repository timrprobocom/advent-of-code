import os
import sys
import math
from functools import cache

test = """\
1
10
100
2024"""

test2 = """\
1
2
3
2024"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read()

data = data.splitlines()
    
# Sequence: x64, mix, prune?
# /32, mix, prune
# *2024, mix, prune
#
# Mix = bitwise xor
# Prune = mod 16777216

def gen(secret):
    secret = (secret ^ (secret <<  6)) & 0xFFFFFF
    secret = (secret ^ (secret >>  5)) & 0xFFFFFF
    secret = (secret ^ (secret << 11)) & 0xFFFFFF
    return secret

def part1(data):
    sumx = 0
    for line in data:
        secret = int(line)
        for _ in range(2000):
            secret = gen(secret)
        sumx += secret
    return sumx

# Generate the part2 prices and deltas from a given secret.

def sequence(secret):
    prices = [secret%10]
    deltas = [0]
    for i in range(2000):
        news = gen(secret)
        prices.append( news%10 )
        deltas.append( news%10 - secret%10 )
        secret = news
    return prices, deltas

# Generate all of the 4-tuplies from the deltas and the price at the end.

def max4(prices, deltas):
    four = {}
    for i in range(len(prices)-4):
        key = tuple(deltas[i:i+4])
        if key not in four:
            four[key] = prices[i+3]
    return four

# Sum up all of the prices for all buyers that have this sequence.

def all_for_this(fours,seq):
    return sum(d.get(seq,0) for d in fours)

def part2(data):
    fours = []
    for line in data:
        secret = int(line)
        p,d = sequence(secret)
        fours.append( max4(p, d))
    # Get the set of all 4-tuples for all buyers.
    allseqs = set(k for d in fours for k in d)
    # Find the best one.
    return max(all_for_this(fours, k) for k in allseqs)

print("Part 1:", part1(data))
if TEST:
    data = test2.splitlines()
print("Part 2:", part2(data))
