import sys
from intcode import Program

live = [int(k) for k in open("day11.txt").read().strip().split(',')]

TRACE = 0
DEBUG = 'debug' in sys.argv

# NESW
directions = (0-1j,-1+0j,0+1j,1+0j)

def run( base, blacks, whites ):
    pgm = Program(live)
    loc = base
    facing = 0
    pgm.start()

    while pgm.is_alive():
        pgm.push( 1 if loc in whites else 0 )
        color = pgm.pop()
        newdir = pgm.pop()
        if TRACE:
            print( color, newdir )
        if color:
            whites.add( loc )
            blacks.discard( loc )
        else:
            blacks.add( loc )
            whites.discard( loc )
        facing = (facing+[1,3][newdir]) % 4
        loc += directions[facing]
        if TRACE:
            print( loc )
    pgm.join()

def bounds(blacks,whites):
    lowx  = int(min(min(k.real for k in blacks), min(k.real for k in whites)))
    lowy  = int(min(min(k.imag for k in blacks), min(k.imag for k in whites)))
    highx = int(max(max(k.real for k in blacks), max(k.real for k in whites)))
    highy = int(max(max(k.imag for k in blacks), max(k.imag for k in whites)))
    return lowx,lowy,highx,highy


def part1():
    blacks = set()
    whites = set()
    run( (0+0j), blacks, whites )

    if DEBUG:
        print( len(blacks), len(whites) )

    if 'image' in sys.argv:
        lowx,lowy,highx,highy = bounds(blacks,whites)
        array = []
        for x in range(lowy,highy+1):
            array.append( [' ']*(highx-lowx+1) )
        for pt in blacks:
            array[int(pt.imag)-lowy][int(pt.real)-lowx] = '.'
        for pt in whites:
            array[int(pt.imag)-lowy][int(pt.real)-lowx] = '#'
        for row in array:
            print( ''.join(row) )

    return len(blacks) + len(whites)

def part2():
    blacks = set()
    whites = set()
    whites.add( 0+0j )
    run( (0+0j), blacks, whites )
    if DEBUG:
        print( len(blacks), len(whites) )

    lowx,lowy,highx,highy = bounds(blacks,whites)

    array = []
    for x in range(lowy,highy+1):
        array.append( [' ']*(highx-lowx+1) )

    for pt in whites:
        array[int(pt.imag)-lowy][int(pt.real)-lowx] = 'X'

    return '\n'.join( ''.join(row) for row in array )

print( "Part 1:", part1() )
print( "Part 2:")
print( part2() )
