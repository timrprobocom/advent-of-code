import os
import sys
import re
from collections import defaultdict, Counter

test = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
    WIDTH,HEIGHT = 11,7
else:
    data = open(day+'.txt').read().splitlines()
    WIDTH,HEIGHT = 101,103

match1 = re.compile(r"p=(\d*),(\d*) v=(-?\d*),(-?\d*)")

info = []
for line in data:
    m = match1.match(line)
    info.append( list(int(i) for i in m.groups()))

data = info

def printgrid(data):
    grid = [[0]*WIDTH for _ in range(HEIGHT)]
    for bot in data:
        grid[bot[1]][bot[0]] += 1
    for row in grid:
        for c in row:
            print('.1234]'[c],end='')
        print()

def move(data):
    for bot in data:
        bot[0] = (bot[0]+bot[2]) % WIDTH
        bot[1] = (bot[1]+bot[3]) % HEIGHT

def detect_tree(data):
    x = Counter((bot[0] for bot in data))
    y = Counter((bot[1] for bot in data))
    if x.most_common()[0][1] > 33 and y.most_common()[0][1] > 31:
        if DEBUG:
            printgrid(data)
        return True
   
def part1(data):
    for _ in range(100):
        move(data)
    hw = WIDTH//2
    hh = HEIGHT//2
    counts = Counter()
    for bot in data:
        (x,y,_,_) = bot
        quadrant = 0
        if x < hw:
            quadrant += 1
        elif x > hw:
            quadrant += 2
        if y < hh:
            quadrant += 4
        elif y > hh:
            quadrant += 8
        counts[quadrant] += 1    
    return counts[5]*counts[9]*counts[6]*counts[10]

def part2(data):
    for i in range(100,10000):
        move(data)
        if detect_tree(data):
            return i+1

print("Part 1:", part1(data))
if not TEST:
    print("Part 2:", part2(data))