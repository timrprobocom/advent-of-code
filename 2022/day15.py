import re
import sys
import time
from collections import Counter

test = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

if 'test' in sys.argv:
    data = test.splitlines()
    target = 10
else:
    data = [s.rstrip() for s in open('day15.txt').readlines()]
    target = 2000000

DEBUG = 'debug' in sys.argv

pattern = re.compile("Sensor at x=([\d-]*), y=([\d-]*): closest beacon is at x=([\d-]*), y=([\d-]*)")

class Sensor:
    def __init__( self, line ):
        res = pattern.match(line)
        self.x0, self.y0, self.x1, self.y1 = [int(k) for k in res.groups()]
        self.dist = abs(self.x1-self.x0)+abs(self.y1-self.y0)

    def within(self, x, y):
        return (abs(x-self.x0)+abs(y-self.y0)) <= self.dist

data = [Sensor(line) for line in data]

def get_limits(data):
    miny = min( min(k.y0,k.y1) for k in data)
    maxy = max( max(k.y0,k.y1) for k in data)
    minx = min( min(k.x0,k.x1) for k in data)
    maxx = max( max(k.x0,k.x1) for k in data)
    return minx, miny, maxx, maxy

def part1(data):
    filled = set()
    beacons = set()
    for s in data:
        if s.y0 == target:
            beacons.add(s.x0)
        if s.y1 == target:
            beacons.add(s.x1)
        fromtgt = abs(target-s.y0)
        # So, from 8,7 to 2,10 distance is 9
        #   7:-1 to 17  19
        #   8: 0 to 16  17
        #   9: 1 to 15  15
        #  10: 2 to 14  13
        #  11: 3 to 13  11
        #  12: 4 to 12  9

        if s.dist < fromtgt:
            continue
        
        x00 = s.x0 - s.dist + fromtgt
        x99 = s.x0 + s.dist - fromtgt
        if DEBUG:
            print(s.x0,s.y0,s.x1,s.y1,s.dist,x00,x99)
        for i in range(x00,x99+1):
            filled.add(i)
    filled -= beacons
    return len(filled)

# This one handles each sensor, then each scanline within the sensor.

def findrows1(data):
    rows = [[] for _ in range(target+target+2)]

    for s in data:
        print('.',end='',flush=True)
        for dy in range(-s.dist,s.dist+1):
            if s.y0+dy not in range(target+target+1):
                continue
            x0t = max( 0, min( target+target, s.x0 - (dist-abs(dy))))
            x1t = max( 0, min( target+target, s.x0 + (dist-abs(dy))))
            rows[s.y0+dy].append( (x0t, x1t) )
    print('',end='\r')
    return rows
    
# This one loops for each possible line, then scans the sensors for that line.
# I thought this would be faster.  It is about 5% slower.

def findrows2(data):
    rows = []

    for y in range(target+target):
        row = []
        for s in data:
            dy = abs(s.y-s.y0)
            # Does this sensor impact this row?
            if dy < dist:
                x0t = max( 0, min( target+target, s.x0 - (s.dist-dy)))
                x1t = max( 0, min( target+target, s.x0 + (s.dist-dy)))
                row.append((x0t,x1t))
        rows.append(row)
    return rows

def part2(data):
    if "2" in sys.argv:
        rows = findrows2(data)
    else:
        rows = findrows1(data)

    # Now combine the ranges.

    for y, row in enumerate(rows):
        row.sort()
        combine = []
        xlo, xhi = row[0]
        for x0, x1 in row:
            if x0-1 <= xhi:
                xhi = max(xhi, x1)
            else:
                combine.append( (xlo, xhi) )
                xlo, xhi = x0, x1
        combine.append( (xlo, xhi) )
        if len(combine) > 1:
            assert len(combine) == 2
            assert combine[0][1]+2 == combine[1][0]
            return (combine[0][1]+1) * 4000000 + y

# This one runs instantaneously.  If we draw a line parallel to each
# surface of the diamonds but one pixel out, then the unseen beacon 
# will be at an intersection of four of those lines.  Handline these
# lines is each, because the slope is either +1 or -1.

def part2(data):

    lines = Counter()
    for s in data:

        # The tuple here is m and b for y=mx+b.

        nw = ( 1, s.y0 - s.dist - 1 - s.x0 )
        ne = (-1, s.y0 - s.dist - 1 + s.x0 )
        se = ( 1, s.y0 + s.dist + 1 - s.x0 )
        sw = (-1, s.y0 + s.dist + 1 + s.x0 )

        lines.update((nw,ne,se,sw))

    # To be the spot, we need 4 lines to intersect.  Thus, there
    # will be two with +1 slope and two with -1 slope.  So, only keep
    # the duplicates.

    slopes = { 1: [], -1: [] }
    for line,count in lines.items():
        if count > 1:
            slopes[line[0]].append(line[1])

    # All the lines have slope of 1 or -1 so intersection is easy.
    # +x + b0 == -x + b1 so 2x = b1 - b0.

    points = []
    for up in slopes[1]:
        for dn in slopes[-1]:
            x = (dn - up) // 2
            y = x + up
            if x in range(0, target+target) and \
               y in range(0, target+target) and \
               not any( s.within(x,y) for s in data):
                return x * 4000000 + y

    return -1


print("Part 1:", part1(data))
print("Part 2:", part2(data))
