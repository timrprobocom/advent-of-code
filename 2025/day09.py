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

# So, what's the largest subrectangle contains entirely within the polygon?
# Should I describe the polygon with rows of X pairs?

def part2(data):
    p1 = Polygon( data )
    d = 0
    for a,b in itertools.combinations(data,2):
        p2 = Polygon( [(a[0],a[1]),(a[0],b[1]), (b[0],b[1]), (b[0],a[1])])
        if p1.contains(p2):
            area = (abs( b[1]-a[1]) + 1) * (abs(b[0]-a[0])+1)
            d = max(d, area)
    return d

print("Part 1:", part1(data))
print("Part 2:", part2(data))