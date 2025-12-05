import os
import sys

test = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read()

d1,d2 = [s.splitlines() for s in data.split('\n\n')]
d1 = list(tuple(int(k) for k in line.split('-')) for line in d1)
d2 = tuple(int(line) for line in d2)
data = (d1,d2)

def part1(ranges,codes):
    count = 0
    for r in codes:
        for lo,hi in ranges:
            if lo <= r <= hi:
                count += 1
                break
    return count

def part2(ranges, _):
    ranges.sort()
    count = 0
    high = 0
    for lo,hi in ranges:
        if DEBUG:
            print(high,lo,hi)
        if high < lo:
            count += hi - lo + 1
            high = hi + 1
        elif high <= hi:
            count += hi - high + 1
            high = hi + 1
    return count

print("Part 1:", part1(*data))
print("Part 2:", part2(*data))
