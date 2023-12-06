import os
import sys
from functools import reduce

test = """\
Time:      7  15   30
Distance:  9  40  200"""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open(day+'.txt').readlines()

DEBUG = 'debug' in sys.argv

time = (int(k) for k in data[0].split()[1:])
dist = (int(k) for k in data[1].split()[1:])
time2 = int(''.join(data[0].split()[1:]))
dist2 = int(''.join(data[1].split()[1:]))

data = zip(time,dist)
data2 = time2,dist2

# So, for the first race, hold time vs distance:
#  0  1  2  3  4  5  6  7
#  0  6 10 12 12 10  6  0
# It's a Pascal's triangle thing

#  0  1  2  3  4  5  6
#  0  5  8  9  8  5  0

def part1(data):
    return reduce((lambda m,n: m*n), (part2(t,d) for t,d in data))

def part2(time,dist):
    d = 0
    i = 0
    n = time-1
    while d <= dist:
        i += 1
        d += n
        n -= 2
    return time+1-i-i

print("Part 1:", part1(data))
print("Part 2:", part2(*data2))
