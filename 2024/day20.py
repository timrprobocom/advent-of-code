import os
import sys
import math
import numpy as np
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

path = makemap(walls)

def part2(path, cheat, crit):
    sumx = 0
    counter = Counter()
    apath = np.array(list(path.keys()))
    # For each pair of points, how much would be gained by shortcutting them?
    for i,a in enumerate(path.keys()):
        mandist = np.abs(apath[i+1:,0]-a[0]) + np.abs(apath[i+1:,1]-a[1])
        for n in np.argwhere(mandist <= cheat):
            # I don't understand why I need the [0] here.  apath[i+1+n] should return
            # [11,22] but it returns [[11,22]].
            op = tuple(apath[i+1+n][0])
            ad = path[op] - path[a]
            gain = ad-mandist[n][0]
            if gain >= crit:
                counter[gain] += 1
                sumx += 1
    if DEBUG:
        print(counter)
    return sumx

print("Part 1:", part2(path,  2, 20 if TEST else 100))
print("Part 2:", part2(path, 20, 50 if TEST else 100))
