import os
import re
import sys
import functools
import itertools
import operator
from pprint import pprint

test = """\
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.""".splitlines()


DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

if 'test' in sys.argv:
    data = test
else:
    data = open('day13.txt').read().split('\n')[:-1]

m = re.compile(r'(\S*) would (gain|lose) (\d*) happiness units by sitting next to (\S*).')
def parse(data):
    names = set()
    scores = {}
    for ln in data:
        parts = m.match(ln)
        delta = int(parts[3])
        if parts[2] == 'lose':
            delta = -delta
        names.add( parts[1] )
        names.add( parts[4] )
        scores[parts.group(1,4)] = delta
    return names, scores

def allsums(names,scores):
    return [(sum( scores[a,b] + scores[b,a] for a,b in zip(setup,setup[1:]+setup[0:1]) )) for setup in itertools.permutations(names)]

names, scores = parse(data)

print( "Part 1:", max(allsums(names,scores)) )

# Add me.

for n in names:
    scores['Me',n] = scores[n,'Me'] = 0
names.add( 'Me' )

print( "Part 2:", max(allsums(names,scores)) )
