import os
import sys
import math
from collections import defaultdict
import heapq

test = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

test = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

walls = set()
start = None
finish = None
for y, line in enumerate(data):
    for x, c in enumerate(line):
        if c == '#':
            walls.add((x,y))
        elif c == 'S':
            start = (x,y)
        elif c == 'E':
            finish = (x,y)

def printgrid(path):
    xpath=set(path)
    for y,row in enumerate(data):
        s = []
        for x,c in enumerate(row):
            if (x,y) in xpath:
                s.append( 'O' )
            else:
                s.append( c )
        print(''.join(s))

def left(pt):
    return (pt[1],-pt[0])
def right(pt):
    return (-pt[1],pt[0])

def part2(walls):
    queue = [(0, start, (1,0), [start])]
    visited = {}
    best = math.inf
    seen = set()
    while queue:
        score,point,dir,path = heapq.heappop(queue)
        if DEBUG:
            print(score,end='\r')
        if score > best:
            break
        visited[(point,dir)] = score
        if point == finish:
            best = score
            seen = seen.union(path)
        for pain,d2 in (1,dir),(1001,right(dir)),(1001,left(dir)):
            p2 = (point[0]+d2[0],point[1]+d2[1])
            if p2 not in walls and visited.get((p2,d2),999999) > score+pain:
                heapq.heappush(queue, (score+pain, p2, d2, path+[p2]))
    if DEBUG:
        printgrid(seen)
    return best,len(seen)

p1,p2 = part2(walls)
print("Part 1:", p1)
print("Part 2:", p2)