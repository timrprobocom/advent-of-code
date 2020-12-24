import os
import re
import sys
import functools
import itertools
import operator
from pprint import pprint


test = """\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""".split('\n')

DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

if 'test' in sys.argv:
    data = test
else:
    data = open('day24.txt').read().split('\n')[:-1]

# -1,-1   -3,-1 -4,0 -2,0 0,0

#   (-1,-1)  (1,-1)
#  (-2,0)     (2,0)
#   (-1,+1)  (1,1)

moves = {
    'nw': (-1,-1),
    'ne': (1,-1),
    'e': (2,0),
    'se': (1,1),
    'sw': (-1,1),
    'w': (-2,0)
}


def add(a,b):
    return (a[0]+b[0],a[1]+b[1])

def part1():
    blacks = set()
    for ln in data:
        pfx = ''
        posn = (0,0)
        for c in ln:
            if c in 'ns':
                pfx = c
            else:
                move = moves[pfx+c]
                posn = add(move,posn)
                pfx = ''

        if posn in blacks:
            blacks.remove(posn)
        else:
            blacks.add(posn)
    return blacks

#Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
#Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.

def neighbors(blacks,cell):
    return sum( 1 for m in moves.values() if add(cell,m) in blacks )

def cycle(blacks):
    minx = min(k[0] for k in blacks) - 2
    maxx = max(k[0] for k in blacks) + 2
    miny = min(k[1] for k in blacks) - 1
    maxy = max(k[1] for k in blacks) + 1

#  Not every point is valid!  That's the key.
#  Both must be even or both must be odd.

    nxt = set()
    for x in range(minx,maxx+1):
        for y in range(miny,maxy+1):
            if (abs(x)+abs(y)) & 1:
                continue
            cell = (x,y)
            blks = neighbors( blacks, cell )
            if cell in blacks and blks in (1,2):
                nxt.add( cell )
            if cell not in blacks and blks == 2:
                nxt.add( cell )
    return nxt

def printgrid(blacks):
    minx = min(k[0] for k in blacks) 
    maxx = max(k[0] for k in blacks) + 1
    miny = min(k[1] for k in blacks)
    maxy = max(k[1] for k in blacks) + 1

    print( '   ' + ''.join(('%2d'%d for d in range(minx,maxx))))
    for y in range(miny,maxy):
        ln = ['%2d '%y]
        for x in range(minx,maxx):
            if (x,y) in blacks:
                ln.append( ' X' )
            else:
                ln.append( '  ' )
        print( (''.join(ln)).rstrip() )


blacks = part1()
dprint(blacks)
#printgrid(blacks)
print( "Part 1:", len(blacks) )
for day in range(100):
    blacks = cycle(blacks)
    dprint(day+1,len(blacks))
print( "Part 2:", len(blacks) )
