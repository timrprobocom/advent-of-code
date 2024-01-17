import os
import sys
import math
import collections

test = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test.strip()
else:
    data = open(day+'.txt').read().strip()

data = data.splitlines()

DEBUG = 'debug' in sys.argv

Brick = collections.namedtuple('Brick',['x0','y0','z0','x1','y1','z1'])
Brick.drop = lambda self, dz: Brick(self.x0,self.y0,self.z0-dz,self.x1,self.y1,self.z1-dz)

def makebrick(row):
    a,b = row.split('~')
    p1 = [int(k) for k in a.split(',')]
    p2 = [int(k) for k in b.split(',')]
    return Brick(*(p1+p2))

bricks = [makebrick(row) for row in data]
bricks.sort( key=lambda b: b.z0)

# How far can this brick drop?  Find the tallest brick
# below us.

def how_much_drop(top,brick):
    peak = max( top[(x,y)]
            for x in range(brick.x0,brick.x1+1)
            for y in range(brick.y0,brick.y1+1)
    )
    return brick.z0-peak-1

# Drop all the bricks that can be dropped.  We remember the
# highest brick for each x,y in `top`.  We sorted the bricks
# by y, so we're always building from bottom to top.

def drop(bricks):
    dropped = 0
    newstack = []
    top = collections.defaultdict(int)
    for brick in bricks:
        dz = how_much_drop(top,brick)
        if dz:
            dropped += 1
        # If it can be dropped, drop it.
        new = brick.drop(dz)
        newstack.append(new)
        # Register the new peak.
        for x in range(brick.x0, brick.x1 + 1):
            for y in range(brick.y0, brick.y1 + 1):
                top[(x, y)] = new.z1
    return newstack

def countdrops(bricks):
    dropped = 0
    top = collections.defaultdict(int)
    for brick in bricks:
        dz = how_much_drop(top,brick)
        if dz:
            dropped += 1
        # If it can be dropped, drop it.
        z1 = brick.z1 - dz
        # Register the new peak.
        for x in range(brick.x0, brick.x1 + 1):
            for y in range(brick.y0, brick.y1 + 1):
                top[(x, y)] = z1
    return dropped

def part1(bricks):
    sum1, sum2 = 0, 0
    # Eliminate all the gaps.
    bricks = drop(bricks)
    # For each brick, if we remove the brick, how many will fall?
    for i in range(len(bricks)):
        bx = bricks[:i] + bricks[i+1:]
        dropped = countdrops(bx)
        sum1 += not dropped
        sum2 += dropped
    return sum1, sum2

p1, p2 = part1(bricks)
print("Part 1:", p1)
print("Part 2:", p2)
