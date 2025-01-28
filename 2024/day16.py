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

def part1(walls):
    # Do a simple BFS forward.

    queue = [(0, start, (1,0))]
    visited = {start: 0}

    while queue:
        score, point, dir = queue.pop(0)
        if DEBUG:
            print(score,end='\r')
        for pain,d2 in (1,dir),(1001,right(dir)),(1001,left(dir)):
            p2 = (point[0]+d2[0],point[1]+d2[1])
            if p2 not in walls and visited.get(p2, 999999) > score+pain:
                visited[p2] = score+pain
                queue.append( (score+pain, p2, d2 ))
    return visited

def part2(walls, visited):
    # Do a backwards BFS.

    queue = [
        (visited[finish], finish, (-1,0)),
        (visited[finish], finish, (0,1))
    ]
    goods = set()
    goods.add( finish )

    while queue:
        score,point, dir = queue.pop(0)
        for pain,d2 in (1,dir),(1001,right(dir)),(1001,left(dir)):
            p2 = (point[0]+d2[0],point[1]+d2[1])
            if p2 not in walls and visited[p2] <= score-pain and p2 not in goods:
                queue.append( (score-pain, p2, d2) )
                goods.add( p2 )
    return len(goods)

visited = part1(walls)
print("Part 1:", visited[finish])
print("Part 2:", part2(walls, visited))
