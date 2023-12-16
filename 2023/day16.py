import os
import sys
import itertools
import functools

test = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test.strip()
else:
    data = open(day+'.txt').read().strip()

DEBUG = 'debug' in sys.argv

grid = data.splitlines()

WID = len(grid[0])
HGT = len(grid)

N,E,S,W = (0,-1),(1,0),(0,1),(-1,0)

change = {
    '/':  { N:E, S:W, E:N, W:S },
    '\\': { N:W, S:E, E:S, W:N }
}

def printg(seen):
    grid = [list('.'*WID) for _ in range(HGT)]
    for x,y in seen:
        grid[y][x] = '#'
    for row in grid:
        print(''.join(row))

def process(grid, start):
    beams = [start]
    seen = set()

    while beams:
        x,y,dir = beams.pop(0)
        if x not in range(WID) or y not in range(HGT):
            continue
        if (x,y,dir) in seen:
            continue
        seen.add((x,y,dir))
        c = grid[y][x]
        if c in '/\\':
            dir = change[c][dir]
            beams.append( (x,y,change[c][dir] ))
        elif c == '|':
            if dir in (E,W):
                beams.append( (x,y-1,N) )
                dir = S
        elif c == '-':
            if dir in (N,S):
                beams.append( (x-1,y,W) )
                dir= E
        x += dir[0]
        y += dir[1]
        if x in range(WID) and y in range(HGT):
            beams.append( (x,y,dir) )
    return len(set( (x,y) for (x,y,_) in seen ))

def part1(grid):
    return process(grid, (0,0,E) )

def part2(grid):
    ener = 0
    for y in range(HGT):
        ener = max( ener,
            process(grid, (0,    y,E)),
            process(grid, (WID-1,y,W))
        )
    for x in range(WID):
        ener = max( ener,
            process(grid, (x,    0,S)),
            process(grid, (x,HGT-1,N))
        )
    return ener
    
print("Part 1:", part1(grid))
print("Part 2:", part2(grid))