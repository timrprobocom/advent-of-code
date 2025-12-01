import os
import sys

test = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').readlines()

def part1(data):
    pos = 50
    count = 0
    for line in data:
        c = int(line[1:])
        if line[0] == 'L':
            pos = (pos - c) % 100
        else:
            pos = (pos + c) % 100
        count += (pos == 0)
    return count

def part2(data):
    pos = 50
    count = 0
    for line in data:
        line = line.strip()
        c = int(line[1:])
        if line[0] == 'L':
            count -= not pos
            pos -= c
            count += abs(pos // 100)
            pos %= 100
            count += not pos
        else:
            pos += c
            count += pos // 100
            pos %= 100
    return count

print("Part 1:", part1(data))
print("Part 2:", part2(data))
