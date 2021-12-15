import sys
from collections import Counter
import itertools

test = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day15.txt').readlines()

grid = [ [int(k) for k in row.strip()] for row in data]

dirs = ( (-1,0), (1,0), (0,1), (0,-1) )

def expandgrid(grid):
    newgrid = []
    for i in range(5):
        for row in grid:
            newrow = []
            for j in range(5):
                for cell in row:
                    v = cell+i+j
                    if v > 9:
                        v -= 9
                    newrow.append( v )
            newgrid.append(newrow)
    return newgrid

# This is Dijkstra's algorithm.  I should remember this.

def part1(grid):
    MAXX = len(grid[0])-1
    MAXY = len(grid)-1

    untried = [(0, 0, 0)]
    costs = {}
    while True:
        cost,x,y = untried.pop(0)
        if x==MAXX and y==MAXY:
            break
        for dx, dy in dirs:
            xx,yy = x+dx, y+dy
            if xx in range(MAXX+1) and yy in range(MAXY+1):
                nc = cost + grid[yy][xx]
                if (xx,yy) in costs and costs[(xx,yy)]<=nc:
                    continue
                costs[(xx,yy)]=nc
                untried.append((nc,xx,yy))
        # Always look at the lowest cost path first.
        untried.sort()
    return cost

print("Part 1:", part1(grid))
print("Part 2:", part1(expandgrid(grid)))
