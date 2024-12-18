import os
import sys
import math
from collections import defaultdict
import heapq

test = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.split()
    WIDTH = 7
else:
    data = open(day+'.txt').read().split()
    WIDTH = 71

grid = [eval(w) for w in data]

start = (0,0)
finish = (WIDTH-1,WIDTH-1)

dirs = [(-1,0),(0,-1),(1,0),(0,1)]

def shortest(walls):
    queue = [(0,0,0)]
    visited = set()
    visited.add( (0,0) )
    while queue:
        x,y,d = queue.pop(0)
        if (x,y) == finish:
            return d
        for dx,dy in dirs:
            x0 = x+dx
            y0 = y+dy
            if x0 in range(WIDTH) and y0 in range(WIDTH) and (x0,y0) not in walls and (x0,y0) not in visited:
                visited.add( (x0,y0) )
                queue.append( (x0,y0,d+1) )
    return -1

def part1(walls):
    limit = 12 if TEST else 1024
    return shortest(walls[:limit])

# Binary search.

def part2(walls):
    minx = 12 if TEST else 1024
    maxx = len(walls)

    while minx < maxx:
        mid = (maxx+minx)//2
        n = shortest(walls[:mid])
        if n < 0:
            maxx = mid
            if DEBUG:
                print(mid, "fails")
        else:
            minx = mid+1
            if DEBUG:
                print(mid, "passes")
    return walls[mid-1]

print("Part 1:", part1(grid))
print("Part 2:", part2(grid))
