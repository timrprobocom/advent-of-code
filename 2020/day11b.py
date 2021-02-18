import os
import sys
import functools
import operator

test = """\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".splitlines()

from pprint import pprint

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
else:
    data = open('day11.txt').read().split('\n')[:-1]

# Unintuitively, this is about 10% slower than the string-based approach.

xlen = len(data[0])
ylen = len(data)

deltas = ( 
    (-1,-1),(-1,0),(-1,1),
    ( 0,-1),       ( 0,1),
    ( 1,-1),( 1,0),( 1,1)
)

def translate(data):
    return set(
        (x,y) 
        for y,ln in enumerate(data)
        for x,c in enumerate(ln) if c == 'L'
    )

def countneighbors( cell, occupied ):
    x,y = cell
    return sum( (x+dx,y+dy) in occupied for dx,dy in deltas )

def countneighbors2( cell, occupied ):
    adjacent = 0
    for dx,dy in deltas:
        x = cell[0]+dx
        y = cell[1]+dy
        while 0 <= x <= xlen and 0 <= y <= ylen:
            if (x,y) in seats:
                if (x,y) in occupied:
                    adjacent += 1
                break
            x += dx
            y += dy
    return adjacent

def passstep( seats, occupied, counter, criteria ):
    new = []
    for cell in seats:
        n = counter( cell, occupied )
        if cell not in occupied and n == 0:
            new.append( cell )
        if cell in occupied and n < criteria:
            new.append( cell )

    return set(new)

for p,counter,criteria in ('Pass 1:', countneighbors, 4),('Pass 2:', countneighbors2, 5):
    seats = translate(data)
    occupied = set()
    while 1:
        if DEBUG:
            pprint( occupied )
        occ2 = passstep(seats, occupied, counter, criteria)
        if DEBUG:
            print( len(occ2) )
        if occupied == occ2:
            break
        occupied = occ2
    print( p, len(occupied) )

