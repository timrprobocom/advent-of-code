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
        print(''.join(row))
    print(sumx)
    return sumx
            
def countgrid(s,dx=0,dy=0):
    sumx = 0
    for x,y in s:
        if x-dx in range(WIDTH) and y-dy in range(HEIGHT):
            sumx += 1
    return sumx

def part1(rocks):
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
        queue = newq
    return len(newq)

# Once we get past an initial start up time, The number of cells at
# each multiple of the grid width, is quadratic.  If the 2nd derivative
# is N, then the first derivative is k
#  f''(x) = N
#  f'(x)  = Nx + b
#  f(x)   = (N/2)x**2 + bx + c
#
# If you look up how to derive a quadratic from differences, you'll find
#  a = d2[0]/2
#  b = d1[0] - 3a
#  c = d0[0] - a - b
# Oddly, this starts counting with 1, so we have to compensate for that.
#
# We gather the counts where (step % width) == (steps % width), so we're
# always at the same point in the cycle.  Note that the offset is where
# the S is, so we're sampling just as we reach the edge of a grid.
#
# It takes about 45 seconds to compute enough differences to ensure
# we know the second differences have stabilized.

def part2(rocks):
    steps = 5000 if 'test' in sys.argv else 26501365
    offset = steps % WIDTH
    queue = set()
    queue.add(origin)
    nums = []
    diff1 = []
    diff2 = []

    for i in range(steps):
        if i % WIDTH == offset:
            nums.append(len(queue))
            if len(nums) > 1:
                diff1.append( nums[-1]-nums[-2] )
            if len(diff1) > 1:
                diff2.append( diff1[-1]-diff1[-2] )
            if DEBUG:
                print(i,nums,diff1,diff2)
            if len(diff2) > 1 and diff2[-1] == diff2[-2]:
                break
        newq = set()
        while queue:
            x,y = queue.pop()
            for dx,dy in N,E,W,S:
                x1 = x+dx
                y1 = y+dy
                if (x1%WIDTH,y1%HEIGHT) not in rocks: 
                    newq.add((x1,y1))
        queue = newq
    
    # Use the first and second differences to find the quadratic
    # coefficients.

    skips = len(nums) - 4
    a = diff2[skips] // 2
    b = diff1[skips] - 3*a
    c = nums[skips] - a - b
    if DEBUG:
        print(skips,a,b,c)
    n = steps//WIDTH-skips+1
    return (a * n + b) * n + c

print("Part 1:", part1(rocks))
print("Part 2:", part2(rocks))
