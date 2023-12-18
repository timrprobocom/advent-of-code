import os
import sys
import heapq

test = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test.strip()
else:
    data = open(day+'.txt').read().strip()

data = data.splitlines()

DEBUG = 'debug' in sys.argv

N,E,S,W = (0,-1),(1,0),(0,1),(-1,0)
U,R,D,L = N,E,S,W
dirs = {'R':R, 'L':L, 'U':U, 'D':D,
        '0':R, '1':D, '2':L, '3':U }

# This implements Green's theorem for integrating the area in a surface
# enclosed by a curve.
#
# Gauss's "shoelace forumula", is a special case of this.

def part1(part,data):
    area = 0
    perim = 0
    x,y = 0,0
    for row in data:
        dir,dist,clr = row.split()
        if part == 1:
            dist = int(dist)
        else:
            dist = int(clr[2:7],16)
            dir = clr[7]
        dx = dist * dirs[dir][0]
        dy = dist * dirs[dir][1]
        area += x * dy
        perim += dist
        x,y = x+dx,y+dy
    if DEBUG:
        print(area,perim)
    return area + perim // 2 + 1
       
print("Part 1:", part1(1,data))
print("Part 2:", part1(2,data))
