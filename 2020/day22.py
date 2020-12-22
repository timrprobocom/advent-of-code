import os
import re
import sys
import functools
import itertools
import operator
from pprint import pprint


test = """\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10""".split('\n\n')

DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

if 'test' in sys.argv:
    data = test
else:
    data = open('day22.txt').read().split('\n\n')

def parse(decks):
    return [[int(k) for k in deck.splitlines() if k[0] != 'P'] for deck in decks]

def part1(data):
    deck1,deck2 = parse(data)
    while deck1 and deck2:
        dprint( deck1, deck2 )
        d1 = deck1.pop(0)
        d2 = deck2.pop(0)
        if d1 > d2:
            deck1.extend([d1,d2])
        else:
            deck2.extend([d2,d1])

    return score(deck1,deck2)

def encode(d1,d2):
    return (''.join(chr(d+32) for d in d1)) + ',' + (''.join(chr(d+20) for d in d2))

def roundx(deck1,deck2,depth=0):
    dprint( depth, "Recurse...", deck1, deck2 )
    remember = set()
    while deck1 and deck2:
        dprint( deck1, deck2 )
        e = encode(deck1,deck2)
        if e in remember:
            dprint( "WIN player 1" )
            return 0

        remember.add( e )

        d1 = deck1.pop(0)
        d2 = deck2.pop(0)
        if d1 > len(deck1) or d2 > len(deck2):
            winner = 0 if d1 > d2 else 1
        else:
            winner = roundx( deck1[:d1], deck2[:d2], depth+1 )
        
        if not winner:
            dprint( "Player 1 wins" )
            deck1.extend([d1,d2])
        else:
            dprint( "Player 2 wins" )
            deck2.extend([d2,d1])
    dprint( "Round over" )
    return 0 if deck1 else 1

def part2(data):
    decks = parse(data)
    while all(decks):
        roundx( *decks )
    return score( *decks )


def score(deck1,deck2):
    d = deck1 + deck2
    return sum( (len(d)-i) * v for i,v in enumerate(d) )

print( "Part 1:", part1(data) )
print( "Part 2:", part2(data) )

