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
    'nw': (-1-1j),
    'ne': (1-1j),
    'e': (2),
    'se': (1+1j),
    'sw': (-1+1j),
    'w': (-2)
}


def add(a,b):
    return (a[0]+b[0],a[1]+b[1])

def part1():
    blacks = set()
    for ln in data:
        posn = 0
        for c in re.findall('[ns]?[ew]', ln):
            posn += moves[c]
        if posn in blacks:
            blacks.remove(posn)
        else:
            blacks.add(posn)
    return blacks

#Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
#Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.

def neighbors(blacks,cell):
    return sum( 1 for m in moves.values() if cell+m in blacks )

def cycle(blacks):
    nxt = set()
    for x in range(-100,100):
        for y in range(-100,100):
            cell = complex(x,y)
            blks = neighbors( blacks, cell )
            if cell in blacks and blks in (1,2):
                nxt.add( cell )
            if cell not in blacks and blks == 2:
                nxt.add( cell )
    return nxt

def printgrid(blacks):
    minx = min(int(k.real) for k in blacks)
    maxx = max(int(k.real) for k in blacks)
    miny = min(int(k.imag) for k in blacks)
    maxy = max(int(k.imag) for k in blacks)
    print( '   ' + ''.join(('%2d'%d for d in range(minx,maxx))))
    for y in range(miny,maxy):
        ln = ['%2d '%y]
        for x in range(minx,maxx):
            if complex(x,y) in blacks:
                ln.append( ' X' )
            else:
                ln.append( '  ' )
        print( (''.join(ln)).rstrip() )


blacks = part1()
dprint(blacks)
printgrid(blacks)
print( "Part 1:", len(blacks) )
for day in range(100):
    blacks = cycle(blacks)
    dprint(day+1,len(blacks))
print( "Part 2:", len(blacks) )
