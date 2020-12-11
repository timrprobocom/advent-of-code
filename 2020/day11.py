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

test2 = """\
""".splitlines()

from pprint import pprint

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
elif 'test2' in sys.argv:
    data = test2
else:
    data = open('day11.txt').read().split('\n')[:-1]

deltas = ( 
    (-1,-1),(-1,0),(-1,1),
    ( 0,-1),       ( 0,1),
    ( 1,-1),( 1,0),( 1,1)
)

def count(grid):
    return sum(ln.count('#') for ln in grid)

def pass1step(grid):
    xlen = len(grid[0])
    ylen = len(grid)
    new = []
    for y,oline in enumerate(grid):
        line = []
        for x,c in enumerate(oline):
            adjacent = 0
            if c != '.':
                for dx,dy in deltas:
                    if 0 <= x+dx < xlen and 0 <= y+dy < ylen and grid[y+dy][x+dx] == '#':
                        adjacent += 1
            if c == 'L' and adjacent == 0:
                line.append('#')
            elif c == '#' and adjacent >= 4:
                line.append('L')
            else:
                line.append(c)
        new.append(''.join(line))
    return new

def pass2step(grid):
    xlen = len(grid[0])
    ylen = len(grid)
    new = []
    for y,oline in enumerate(grid):
        line = []
        for x,c in enumerate(oline):
            adjacent = 0
            if c != '.':
                for dx,dy in deltas:
                    x0,y0 = x,y
                    while 1:
                        x0+=dx
                        y0+=dy
                        if x0 < 0 or x0 >= xlen or y0 < 0 or y0 >= ylen or grid[y0][x0] == 'L':
                            break
                        if grid[y0][x0] == '#':
                            adjacent += 1
                            break
            if c == 'L' and adjacent == 0:
                line.append('#')
            elif c == '#' and adjacent >= 5:
                line.append('L')
            else:
                line.append(c)
        new.append(''.join(line))
    return new


for p,passfunc in ('Pass 1:', pass1step),('Pass 2:',pass2step):
    grid = data
    while 1:
        if DEBUG:
            pprint( grid )
        grid2 = passfunc(grid)
        if DEBUG:
            print( count(grid) )
        if grid == grid2:
            break
        grid = grid2
    print( p, count(grid) )

