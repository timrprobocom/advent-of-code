import os
import sys
import itertools
from shapely.geometry import Polygon

test = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read()

data = list(tuple(int(k) for k in ln.split(',')) for ln in data.splitlines())

def part1(data):
    d = 0
    for a,b in itertools.combinations(data,2):
        area = (abs( b[1]-a[1]) + 1) * (abs(b[0]-a[0])+1)
        d = max(d, area)
    return d

# The figure is a circle with a slit, like a Pacman.

# This one takes 11 seconds.

def part2(data):
    p1 = Polygon( data )
    best = 0
    for a,b in itertools.combinations(data,2):
        area = (abs( b[1]-a[1]) + 1) * (abs(b[0]-a[0])+1)
        if area >= best:
            p2 = Polygon( [(a[0],a[1]),(a[0],b[1]), (b[0],b[1]), (b[0],a[1])])
            if p1.contains(p2):
                if DEBUG:
                    print(area,a,b)
                best = area
    return best

# This one takes 3 seconds.

def part2(data):
    best = 0
    for a,b in itertools.combinations(data,2):
        area = (abs( b[1]-a[1]) + 1) * (abs(b[0]-a[0])+1)
        if area < best:
            continue
        x1,x2 = sorted((a[0],b[0]))
        y1,y2 = sorted((a[1],b[1]))
        maybe = True
        for p1,p2 in zip(data, data[1:]+data[:1]):
            if p1[0] == p2[0]:
                # Vertical.
                py0,py1 = sorted((p1[1],p2[1]))
                if x1 < p1[0] < x2 and py0 <= y2 and py1 >= y1:
                    maybe = False
                    break
            else:
                # Horizontal.
                px0,px1 = sorted((p1[0],p2[0]))
                if y1 < p1[1] < y2 and px0 <= x2 and px1 >= x1:
                    maybe = False
                    break
        if maybe:
            if DEBUG:
                print(area,a,b)
            best = area
    return best
                

print("Part 1:", part1(data))
print("Part 2:", part2(data)) # 1429075575