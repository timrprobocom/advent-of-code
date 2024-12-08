import os
import sys
from pprint import pprint
from collections import defaultdict

test = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

WIDTH = len(data[0])
HEIGHT = len(data)

spots = defaultdict(list)
for y,row in enumerate(data):
    for x,c in enumerate(row):
        if c != '.':
            spots[c].append((x,y))

def printgrid(antinodes):
    grid = [list(row) for row in data]
    for x,y in antinodes:
        grid[y][x] = '#'
    for row in grid:
        print(''.join(row)) 

def part1(spots):
    antinodes = set()
    for k,v in spots.items():
        for i,(x0,y0) in enumerate(v):
            for x1,y1 in v[i+1:]:
                dx = x1-x0
                dy = y1-y0
                antinodes.add( (x0-dx,y0-dy))
                antinodes.add( (x1+dx,y1+dy))
    antinodes = set((x,y) for (x,y) in antinodes if x in range(WIDTH) and y in range(HEIGHT))
    if DEBUG:
        printgrid(antinodes)
    return len(antinodes)

def part2(data):
    antinodes = set()
    for k,v in spots.items():
        for i,(xx0,yy0) in enumerate(v):
            for x1,y1 in v[i+1:]:
                x0 = xx0
                y0 = yy0
                dx = x1-x0
                dy = y1-y0
                while x0 in range(WIDTH) and y0 in range(HEIGHT):
                    antinodes.add( (x0,y0) )
                    x0 -= dx
                    y0 -= dy
                while x1 in range(WIDTH) and y1 in range(HEIGHT):
                    antinodes.add( (x1,y1) )
                    x1 += dx
                    y1 += dy
    if DEBUG:
        printgrid(antinodes)
    return len(antinodes)

print("Part 1:", part1(spots))
print("Part 2:", part2(spots))
