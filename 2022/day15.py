import re
import sys
from functools import cmp_to_key

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

def convert(line):
    res = pattern.match(line)
    return [int(k) for k in res.groups()]

data = [convert(line) for line in data]

#miny = min( min(k[1],k[3]) for k in data)
#maxy = max( max(k[1],k[3]) for k in data)
#minx = min( min(k[0],k[2]) for k in data)
#maxx = max( max(k[0],k[2]) for k in data)


def part1(data):
    filled = set()
    beacons = set()
    for x0,y0,x1,y1 in data:
        if y0 == target:
            beacons.add(x0)
        if y1 == target:
            beacons.add(x1)
        fromtgt = abs(target-y0)
        # So, from 8,7 to 2,10 distance is 9
        #   7:-1 to 17  19
        #   8: 0 to 16  17
        #   9: 1 to 15  15
        #  10: 2 to 14  13
        #  11: 3 to 13  11
        #  12: 4 to 12  9

        dx = abs(x1-x0)+abs(y1-y0)
        if dx < fromtgt:
            continue
        
        x00 = x0 - dx + fromtgt
        x99 = x0 + dx - fromtgt
        if DEBUG:
            print(x0,y0,x1,y1,dx,x00,x99)
        for i in range(x00,x99+1):
            filled.add(i)
    filled -= beacons
    return len(filled)

def part2(data):
    rows = [[] for _ in range(target+target+2)]
    for x0,y0,x1,y1 in data:
        print(x0,y0,x1,y1)
        dist = abs(x1-x0)+abs(y1-y0)
        for dy in range(-dist,dist+1):
            if y0+dy not in range(target+target+1):
                continue
            x0t = max( 0, min( target+target, x0 - (dist-abs(dy))))
            x1t = max( 0, min( target+target, x0 + (dist-abs(dy))))
            rows[y0+dy].append( (x0t, x1t) )

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

print("Part 1:", part1(data))
print("Part 2:", part2(data))
