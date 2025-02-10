import os
import sys
import math
from collections import defaultdict

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

data = list(map(int,data.splitlines()))
test2 = list(map(int,test2.splitlines()))
    
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
    for secret in data:
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

def make4key( deltas ):
    res = 0
    for t in deltas:
        res = res * 100 + t + 9
    return res

# Generate all of the 4-tuples from the deltas and the price at the end.

def part2(data):
    fours = defaultdict(int)
    for secret in data:
        prices,deltas = sequence(secret)
        seen = set()
        for i in range(len(prices)-4):
            key = make4key(deltas[i:i+4])
            if key not in seen:
                fours[key] += prices[i+3]
                seen.add( key )
    return max(fours.values())

print("Part 1:", part1(data))
if TEST:
    data = test2
print("Part 2:", part2(data))
