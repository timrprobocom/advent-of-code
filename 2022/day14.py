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

def cmp(l,r):
    if l < r:
        return 1
    if l > r:
        return -1
    return 0

def fill(xmap,line):
    segment = []
    for point in line.split(" -> "):
        x,y = point.split(',')
        segment.append( (int(x),int(y)) )
    fillsegment(xmap,segment)

def fillsegment(xmap,segment):
    x,y = segment[0]
    xmap.add( (x,y) )
    for x0,y0 in segment[1:]:
        dx = cmp(x,x0)
        dy = cmp(y,y0)
        while x0 != x or y0 != y:
            x += dx
            y += dy
            xmap.add((x,y))

def plot(xmap):
    minx = min(pt[0] for pt in xmap)
    maxx = max(pt[0] for pt in xmap)
    miny = min(pt[1] for pt in xmap)
    maxy = max(pt[1] for pt in xmap)
    themap = [['.']*(maxx-minx+1) for _ in range(maxy-miny+1)]
    for x,y in xmap:
        themap[y-miny][x-minx] = '#'
    for row in themap:
        print(''.join(row))

dirs = ((0,1),(-1,1),(1,1))

def part1(part,data):
    xmap = set()
    for line in data:
        fill(xmap,line)
    maxy = max(pt[1] for pt in xmap)
    if part == 2:
        maxy += 2
        fillsegment(xmap,[[0,maxy],[699,maxy]])

    sand = 0
    while (500,0) not in xmap:
        sx = 500
        sy = 0
        while sy <= maxy:
            for dx,dy in dirs:
                sx0=sx+dx
                sy0=sy+dy
                if (sx0,sy0) not in xmap:
                    sx,sy = sx0,sy0
                    break
            else:
                if DEBUG:
                    print("placed",sx,sy)
                sand += 1
                xmap.add( (sx,sy) )
                break
        else:
            break
    if DEBUG:
        plot(xmap)
    return sand
    
print("Part 1:", part1(1,data))
print("Part 2:", part1(2,data))
