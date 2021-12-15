import sys
from heapq import heappush, heappop
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

class Neighbors:
    dirs = (
                 (0,-1),
        (-1,0),          (1,0),
                 (0,1),
    )

    def __init__( self, w, h ):
        self.w = w
        self.h = h

    def nextto( self, x, y ):
        for dx,dy in self.dirs:
            x0,y0 = x+dx,y+dy
            if x0 in range(self.w) and y0 in range(self.h):
                yield x0,y0

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
#
# We use heapq so the lowest cost path is always on top.

def part1(grid):
    MAXX = len(grid[0])-1
    MAXY = len(grid)-1
    adj = Neighbors(MAXX+1, MAXY+1)

    untried = []
    heappush( untried, (0,0,0) )
    costs = {}
    while True:
        cost,x,y = heappop(untried)
        if x==MAXX and y==MAXY:
            break
        for xx, yy in adj.nextto(x,y):
            nc = cost + grid[yy][xx]
            if (xx,yy) in costs and costs[(xx,yy)]<=nc:
                continue
            costs[(xx,yy)]=nc
            heappush(untried, (nc,xx,yy))
    return cost

print("Part 1:", part1(grid))                   # 702
print("Part 2:", part1(expandgrid(grid)))       # 2955
