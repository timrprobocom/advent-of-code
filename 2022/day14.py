import ast
import sys
from functools import cmp_to_key

test = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [s.rstrip() for s in open('day14.txt').readlines()]

DEBUG = 'debug' in sys.argv

maxy = 0

def fill(xmap,line):
    segment = []
    for point in line.split(" -> "):
        x,y = point.split(',')
        segment.append( (int(x),int(y)) )
    fillsegment(xmap,segment)

def fillsegment(xmap,segment):
    global maxy
    x,y = segment[0]
    xmap[y][x] = 1
    for x0,y0 in segment[1:]:
        if x0 == x:
            dx = 0
        elif x0 < x:
            dx = -1
        else:
            dx = 1
        if y0 < y:
            dy = -1
        elif y0 == y:
            dy = 0
        else:
            dy = 1
        while x0 != x or y0 != y:
            x += dx
            y += dy
            xmap[y][x] = 1
            maxy = max(maxy,y)

dirs = ((0,1),(-1,1),(1,1))

def part1(part,data):
    xmap = [[0]*700 for _ in range(200)]
    for line in data:
        fill(xmap,line)
    if part == 2:
        fillsegment(xmap,[[0,maxy+2],[699,maxy+2]])

    sand = 0
    while xmap[0][500] == 0:
        sx = 500
        sy = 0
        while sy <= maxy:
            for dx,dy in dirs:
                sx0=sx+dx
                sy0=sy+dy
                if xmap[sy0][sx0] == 0:
                    sx,sy = sx0,sy0
                    break
            else:
                if DEBUG:
                    print("placed",sx,sy)
                sand += 1
                xmap[sy][sx] = 1
                break
        else:
            break
    return sand
    
print("Part 1:", part1(1,data))
print("Part 2:", part1(2,data))
