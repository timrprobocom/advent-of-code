import os
import sys
import math
import collections

test = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test.strip()
else:
    data = open(day+'.txt').read().strip()

data = data.splitlines()
WIDTH = len(data[0])
HEIGHT = len(data)

DEBUG = 'debug' in sys.argv

N,E,S,W = (0,-1),(1,0),(0,1),(-1,0)
U,R,D,L = N,E,S,W
dirs = {'R':R, 'L':L, 'U':U, 'D':D,
        '0':R, '1':D, '2':L, '3':U }

rocks = set()
origin = None
for y,row in enumerate(data):
    for x,c in enumerate(row):
        if c == 'S':
            origin = (x,y)
        elif c == '#':
            rocks.add((x,y))

# 40 rocks in test
# 2290 rocks in real
            
def printgrid(s,dx=0,dy=0):
    grid = [list('.'*WIDTH) for _ in range(HEIGHT)]
    for x,y in s:
        if x-dx in range(WIDTH) and y-dy in range(HEIGHT):
            grid[y-dy][x-dx] = 'O'
    sumx = 0
    for row in grid:
        sumx += row.count('O')
#        print(''.join(row))
#    print(sumx)
    return sumx
            
def countgrid(s,dx=0,dy=0):
    sumx = 0
    for x,y in s:
        if x-dx in range(WIDTH) and y-dy in range(HEIGHT):
            sumx += 1
    return sumx

def part1(data):
    steps = 6 if 'test' in sys.argv else 64
    queue = set()
    queue.add(origin)
    for _ in range(steps):
        newq = set()
        while queue:
            x,y = queue.pop()
            for dx,dy in N,E,W,S:
                x1 = x+dx
                y1 = y+dy
                pt = (x1,y1)
                if x1 in range(WIDTH) and y1 in range(HEIGHT) and pt not in rocks: 
                    newq.add(pt)
        printgrid(newq)
        queue = newq
    return len(newq)

# So every grid reaches a stasis point, flipping between 39 and 42.
# There's a cycle here.  When does a new layer fill up?  It takes
# 13 to fill the center, and 35 steps to fill the next layer. 
# We only need to handle the outermost layers. 
#
# NOTE that we need to compute the stasis point -- 39/42 is for the
# sample data.  7427/7434 for the real data.
#
# How fast does the circle expand?  Should be approximately steps.

def part2(data):
    steps = 5000 if 'test' in sys.argv else 26501365
    skips = 4 if 'test' in sys.argv else 1
    offset = steps % WIDTH
    queue = set()
    queue.add(origin)
    diffs = []
    # Gather up the first 4 multiples of the width.
    for i in range(steps):
        if i % WIDTH == offset:
            print(i,len(queue))
            diffs.append(len(queue))
            if len(diffs) == skips+3:
                break
        newq = set()
        while queue:
            x,y = queue.pop()
            for dx,dy in N,E,W,S:
                x1 = x+dx
                y1 = y+dy
                pt = (x1,y1)
                ptm = (x1%WIDTH,y1%HEIGHT)
                if ptm not in rocks: 
                    newq.add(pt)
        queue = newq
    
    # Given those, compute first and second differences to make
    # a quadratic.  
    
    b0 = diffs[skips]
    b1 = diffs[skips+1]-diffs[skips]
    b2 = diffs[skips+2]-diffs[skips+1]
    n = steps//WIDTH-skips
    return b0 + b1*n + (n*(n-1)//2)*(b2-b1)

print("Part 1:", part1(data))
print("Part 2:", part2(data))
