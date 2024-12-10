import os
import sys
from pprint import pprint
from collections import defaultdict
from itertools import permutations

test = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

data = [[int(d) for d in row] for row in data]

WIDTH = len(data[0])
HEIGHT = len(data)

dirs = ( (-1,0), (1,0), (0,-1), (0,1) )

def part1(data):
    # Find the zeros.
    zeros = []
    for y,row in enumerate(data):
        for x,c in enumerate(row):
            if not c:
                zeros.append( (x,y) )
    
    queue = []
    part1 = 0
    part2 = 0
    for zx,zy in zeros:
        queue.append( (zx, zy, 0) )
        solutions = set()
        while queue:
            x,y,c = queue.pop(0)
            c += 1
            for dx,dy in dirs:
                x0,y0 = x+dx,y+dy
                if x0 in range(WIDTH) and y0 in range(HEIGHT) and data[y0][x0] == c:
                    if c == 9:
                        part2 += 1
                        solutions.add( (x0,y0) )
                    else:
                        queue.append( (x0, y0, c))
        part1 += len(solutions)
    return part1, part2

p1,p2 = part1(data)
print("Part 1:", p1)
print("Part 2:", p2)
