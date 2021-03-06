real = [
3,8,1005,8,324,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1002,8,1,29,2,1102,17,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,55,2,4,6,10,1,1006,10,10,1,6,14,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,89,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,1002,8,1,110,1,104,8,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,137,2,9,17,10,2,1101,14,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,101,0,8,167,1,107,6,10,1,104,6,10,2,1106,6,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,1001,8,0,200,1006,0,52,1006,0,70,1006,0,52,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,1002,8,1,232,1006,0,26,1,104,19,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,102,1,8,260,1,2,15,10,2,1102,14,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,290,1,108,11,10,1006,0,36,1006,0,90,1006,0,52,101,1,9,9,1007,9,940,10,1005,10,15,99,109,646,104,0,104,1,21101,0,666412360596,1,21101,341,0,0,1105,1,445,21101,838366659476,0,1,21102,1,352,0,1106,0,445,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,0,97713695975,1,21102,1,399,0,1106,0,445,21102,179469028392,1,1,21101,410,0,0,1105,1,445,3,10,104,0,104,0,3,10,104,0,104,0,21102,1,988220650260,1,21101,433,0,0,1105,1,445,21101,0,838345843560,1,21101,444,0,0,1106,0,445,99,109,2,22101,0,-1,1,21102,1,40,2,21102,1,476,3,21101,466,0,0,1106,0,509,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,471,472,487,4,0,1001,471,1,471,108,4,471,10,1006,10,503,1101,0,0,471,109,-2,2106,0,0,0,109,4,1202,-1,1,508,1207,-3,0,10,1006,10,526,21101,0,0,-3,22101,0,-3,1,22102,1,-2,2,21102,1,1,3,21101,0,545,0,1106,0,550,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,573,2207,-4,-2,10,1006,10,573,21201,-4,0,-4,1106,0,641,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21102,592,1,0,1106,0,550,21201,1,0,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,611,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,633,22102,1,-1,1,21102,1,633,0,106,0,508,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0]

import sys
from intcode import Program
TRACE = 0

# NESW
directions = (0-1j,-1+0j,0+1j,1+0j)

def run( base, blacks, whites ):
    pgm = Program(real)
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

    print( len(blacks), len(whites) )
    print( "Part 1: ", len(blacks) + len(whites) )

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

def part2():
    blacks = set()
    whites = set()
    whites.add( 0+0j )
    run( (0+0j), blacks, whites )
    print( len(blacks), len(whites) )

    lowx,lowy,highx,highy = bounds(blacks,whites)

    array = []
    for x in range(lowy,highy+1):
        array.append( [' ']*(highx-lowx+1) )

    for pt in whites:
        array[int(pt.imag)-lowy][int(pt.real)-lowx] = 'X'

    print( "Part 2:" )
    for row in array:
        print( ''.join(row) )

part1()
part2()

