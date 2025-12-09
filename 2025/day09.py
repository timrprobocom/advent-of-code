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

def makePolygon(data):
    rows = {}
    for x,y in data:
        if y not in rows:
            rows[y] = []
        rows[y].append(x)

    for row in rows.values():
        row.sort()

    yaxis = sorted(rows)

    # OK, so
    # 0
    # 1  7-11
    # 3  2-11
    # 5  9-11
    # 7  None

    row = []
    for y in yaxis:
        l,r = rows[y]
        matches = 0
        nrow = []
        for cl,cr in row:
            if (cl,cr) == (l,r):
                matches = 1
            elif cr == l:
                if matches:
                    nrow[-1] = (cl, nrow[-1][1])
                else:
                    nrow.append( (cl, r) )
                matches += 1
            elif cr == r:
                nrow.append( (cl, l) )
                matches += 1
            elif cl == r:
                if matches:
                    nrow[-1] = (nrow[-1][0],cr)
                else:
                    nrow.append( (l, cr) )
                matches += 1
            elif cl == l:
                nrow.append( (r, cr) )
                matches += 1
            else:
                nrow.append( (cl, cr) )
        if not matches:
            nrow.append( (l, r) )
        rows[y] = row = sorted(nrow)    
    return rows

# The figure is a circle with a slit, like a Pacman.

# This one takes 22 seconds.

def part2(data):
    scans = makePolygon(data)
    if DEBUG:
        for y in sorted(scans):
            print(y,scans[y])
        print("**")
 
    best = 0
    for a,b in itertools.combinations(data,2):
        area = (abs( b[1]-a[1])+1) * (abs(b[0]-a[0])+1)
        if area < best:
            continue
        x1,x2 = sorted((a[0],b[0]))
        y1,y2 = sorted((a[1],b[1]))
        for y in range(y1,y2):
            if y in scans:
                for l,r in scans[y]:
                    if (x1 >= l and x2 <= r):
                        break
                else:
                    break
        else:
            if DEBUG:
                print(area,a,b)
            best = area
    return best

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

print("Part 1:", part1(data))
print("Part 2:", part2(data)) # 1429075575