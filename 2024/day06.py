import os
import sys
from collections import defaultdict
from functools import cmp_to_key
from pprint import pprint

test = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

WIDTH = len(data[0])
HEIGHT = len(data)

data = [list(d) for d in data]

# Find the guard.

for y,line in enumerate(data):
    if '^' in line:
        x = line.index('^')
        break

GUARD = (x,y)

N = (0,-1)
W = (-1,0)
S = (0,1)
E = (1,0)

turn = {
    N:E,
    E:S,
    S:W,
    W:N
}

def part1(data):
    steps = set()
    gx,gy = GUARD
    dir = N
    while 1:
        steps.add((gx,gy))
        nx = gx+dir[0]
        ny = gy+dir[1]
        if nx in range(WIDTH) and ny in range(HEIGHT):
            if data[ny][nx] != '#':
                gx,gy = nx,ny
            else:
                dir = turn[dir]
        else:
            break
    return len(steps)

# If we are facing an empty cell, but there is an already-reached spot to our right, that's a loop.

def follow( x, y, dir, data, seen ):
    gx = x
    gy = y
    while 1:
        nx = gx+dir[0]
        ny = gy+dir[1]
        if (nx,ny) in seen[dir] or (nx,ny) == (x,y):
            return True
        if nx in range(WIDTH) and ny in range(HEIGHT):
            if data[ny][nx] == '#':
                dir = turn[dir]
            else:
                gx,gy = nx,ny
        else:
            break
    return False

def solve(data):
    steps = set()
    lines = {N:set(), W:set(), E:set(), S:set()}
    gx,gy = GUARD
    dir = N
    while 1:
        steps.add((gx,gy))
        lines[dir].add((gx,gy))
        nx = gx+dir[0]
        ny = gy+dir[1]
        if nx in range(WIDTH) and ny in range(HEIGHT):
            if (nx,ny) in lines[dir]:
                return set()
            elif data[ny][nx] != '#':
                gx,gy = nx,ny
            else:
                dir = turn[dir]
        else:
            break
    return steps


def part1(data):
    return len(solve(data))

# Why doesn't this work?  At each point, if turning right results in us
# finding a cell we've visited before, then this is a loop.  This comes
# up with 526, way short of 2262.  Do I have to search around corners?

def part2(data):
    steps = {N:set(), W:set(), E:set(), S:set()}
    blocks = set()
    gx,gy = GUARD
    dir = N

    while 1:
        steps[dir].add((gx,gy))
        nx = gx+dir[0]
        ny = gy+dir[1]
        if nx in range(WIDTH) and ny in range(HEIGHT):
            right = turn[dir]
            if data[ny][nx] != '#':
                print('checking',gx,gy,right)
                if follow( gx, gy, right, data, steps ):
                    print("Added", nx, ny)
                    blocks.add( (nx,ny) )
                gx,gy = nx,ny
            else:
                dir = right
        else:
            break

    return len(blocks)

# Brute force.  For every spot we visited, if we put an obstacle, do we loop?

def part2(data):
    visits = solve(data)
    sumx = 0
    for x,y in visits:
        data[y][x] = '#'        
        sumx += not solve(data)
        print(sumx,end='\r')
        data[y][x] = '.'
    return sumx

print("Part 1:", part1(data))
print("Part 2:", part2(data))
