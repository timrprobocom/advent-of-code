import os
import sys
import itertools
import copy

DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

# Must buy 1 weapon.

weapons = (
    (  8, 4, 0 ),
    ( 10, 5, 0 ),
    ( 25, 6, 0 ),
    ( 40, 7, 0 ),
    ( 74, 8, 0 )
)

# Must buy 0 or 1 weapon.

armor = (
    (   0, 0, 0 ),
    (  13, 0, 1 ),
    (  31, 0, 2 ),
    (  53, 0, 3 ),
    (  75, 0, 4 ),
    ( 102, 0, 5 )
)

# Must buy 0, 1, or 2 rings.

_rings = (
    (  25, 1, 0 ),
    (  50, 2, 0 ),
    ( 100, 3, 0 ),
    (  20, 0, 1 ),
    (  40, 0, 2 ),
    (  80, 0, 3 )
)

def rings():
    yield (0,0,0)
    for r in _rings:
        yield r
    for r,s in itertools.combinations(_rings,2):
        yield tuple(a+b for a,b in zip(r,s))

class Player(object):
    def __init__(self, pts=0, dmg=0, arm=0):
        self.points = pts
        self.damage = dmg
        self.armor = arm
    def __repr__(self):
        return f"p={self.points} d={self.damage} a={self.armor}"

def battle( p, b ):
    while 1:
        b.points -= max( 1, p.damage - b.armor )
        dprint( "Boss down to", b.points )
        if b.points <= 0:
            return 0
        p.points -= max( 1, b.damage - p.armor )
        dprint( "Player down to", p.points )
        if p.points <= 0:
            return 1

if 'test' in sys.argv:
    player = Player( 8, 5, 5 )
    boss = Player( 12, 7, 2 )
    print( ["Player","Boss"][battle( player, boss )], "wins" )
else:
    wins = set()
    loss = set()
    for w in weapons:
        for a in armor:
            for r in rings():
                cost = w[0]+a[0]+r[0]
                player = Player( 100, w[1]+a[1]+r[1], w[2]+a[2]+r[2] )
                boss = Player( 103, 9, 2 )
                if battle( player, boss ):
                    loss.add( cost )
                else:
                    wins.add( cost )
    print( "Part 1:", min(wins) )
    print( "Part 2:", max(loss) )



