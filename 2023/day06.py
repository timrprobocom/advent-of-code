import os
import sys

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
data2 = ((time2,dist2),)

# So, for the first race, hold time vs distance:
#  0  1  2  3  4  5  6  7
#  0  6 10 12 12 10  6  0
# It's a Pascal's triangle thing

def part1(data):
    mult = 1
    for time,dist in data:
        wins = 0
        d = 0
        n = time-1
        for i in range(1,time+1):
            d += n
            n -= 2
            wins += d > dist
        mult *= wins
    return mult

print("Part 1:", part1(data))
print("Part 2:", part1(data2))
