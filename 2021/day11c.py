import sys
import curses
import time
import itertools
from collections import Counter
from statistics import median

test = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

live = """\
1443582148
6553734851
1451741246
8835218864
1662317262
1731656623
1128178367
5842351665
6677326843
7381433267"""

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    ndata = test
else:
    ndata = live

def makegrid(ndata):
    data = []
    for row in ndata.splitlines():
        data.append( [int(i) for i in row.rstrip()] )
    return data


def printgrid(data):
    for i,row in enumerate(data):
        stdscr.addstr( 20+i, 5,  ''.join(str(i) for i in row) )
    stdscr.refresh()
    time.sleep( 0.1 )

# I could use an array class that understands boundaries.

class Neighbors:
    dirs = (
        (-1,-1), (0,-1), (1,-1),
        (-1,0),          (1,0),
        (-1,1),  (0,1),  (1,1)
    )

    def __init__( self, w, h ):
        self.w = w
        self.h = h

    def nextto( self, x, y ):
        for dx,dy in self.dirs:
            x0,y0 = x+dx,y+dy
            if 0 <= x0 < WIDTH and 0 <= y0 < HEIGHT:
                yield x0,y0

# Steps:
# Each +1
# Each 9 causes +1 for all neighbors
# Repeat until no more pass 9.
# Any that get to >= 9 reset to 0


def generation(data):
    # This modidies data in place.
    adj = Neighbors(WIDTH,HEIGHT)
    flashes = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            data[y][x] += 1
    more = True
    while more:
        more = False
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if data[y][x] >= 10:
                    flashes += 1
                    data[y][x] = 0
                    for x0,y0 in adj.nextto(x,y):
                        if data[y0][x0]:
                            more = True
                            data[y0][x0] += 1
    printgrid(data)
    return flashes

# How many generations until they all flash at once?

def part2(data):
    flash = 0
    for gen in itertools.count(1):
        stdscr.addstr( 33, 13, "%d" % gen )
        n = generation(data)
        if n == WIDTH*HEIGHT:
            return gen
        flash += n
        if gen == 100: 
            stdscr.addstr( 32, 5, "Part 1: %d" % flash )

def main(_stdscr):
    global stdscr
    global WIDTH
    global HEIGHT

    stdscr = _stdscr
    stdscr.clear()

    data = makegrid(ndata)
    WIDTH = len(data[0])
    HEIGHT = len(data)

    printgrid(data)
    stdscr.addstr( 33, 5, "Part 2: %d" % part2(data))  #  1717
    stdscr.getkey()

curses.wrapper(main)
