import os
import sys
import math
from collections import Counter
from itertools import permutations

test = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read()

data = data.splitlines()

WIDTH = len(data[0])
HEIGHT = len(data)

walls = set()
start = None
end = None
for y,row in enumerate(data):
    for x,c in enumerate(row):
        if c=='#':
            walls.add( (x,y))
        elif c=='S':
            start = (x,y)
        elif c=='E':
            end = (x,y)

dirs = [(-1,0),(0,-1),(1,0),(0,1)]

# There is only one path through.  Compute the distance from start for each step.

def makemap(walls):
    mapx = {}
    point = start
    while point != end:
        mapx[point] = len(mapx)
        for dx,dy in dirs:
            x0=point[0]+dx
            y0=point[1]+dy
            if (x0,y0) not in walls and (x0,y0) not in mapx:
                point = (x0,y0)
                break
    mapx[end] = len(mapx)
    return mapx

normal = makemap(walls)

def mandist(pt1,pt2):
    x1,y1 = pt1
    x2,y2 = pt2
    return abs(x2-x1)+abs(y2-y1)

def part2(normal, cheat, crit):
    sumx = 0
    counter = Counter()
    # For each pair of points, how much would be gained by shortcutting them?
    for a,b in permutations(normal.keys(), 2):
        if normal[a] >= normal[b]:
            continue
        # Compute manhattan distance
        md = mandist(a,b)
        if md <= cheat:
            ad = normal[b]-normal[a]
            gain = ad-md
            if gain >= crit:
                counter[gain] += 1
                sumx += 1
    if DEBUG:
        print(counter)
    return sumx

print("Part 1:", part2(normal,  2, 20 if TEST else 100))
print("Part 2:", part2(normal, 20, 50 if TEST else 100))
