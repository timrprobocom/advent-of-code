import os
import sys
from collections import defaultdict
from functools import cache

test = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read()

towels,needs = data.split('\n\n')
towels = towels.split(', ')
needs = needs.splitlines()

def possible(need,sofar=''):
    return 1 if need==sofar else any(possible(need,sofar+t) for t in towels if need.startswith(sofar+t))

def part1(needs):
    return sum(map(possible, needs))

@cache
def howmany(need,sofar=''):
    return 1 if need==sofar else sum(howmany(need,sofar+t) for t in towels if need.startswith(sofar+t))

def part2(needs):
    return sum(map(howmany, needs))

print("Part 1:", part1(needs))
print("Part 2:", part2(needs))

if DEBUG:
    print(howmany.cache_info())