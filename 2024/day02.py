import sys
import re

test = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

if 'test' in sys.argv:
    lines = test.splitlines()
else:
    lines = open('day02.txt').readlines()

DEBUG = 'debug' in sys.argv

data = [ [int(i) for i in l.split()] for l in lines ]

def is_safe(row):
    for x,y in zip(row[:-1],row[1:]):
        if (y-x) * (row[1]-row[0]) < 0:
            return 0
        if abs(y-x) not in (1,2,3):
            return 0
    return 1

def part1(data):
    return sum(map(is_safe,data))

def part2(data):
    safe = 0
    for row in data:
        if is_safe(row):
            if DEBUG:
                print(row,"safe")
            safe += 1
        else:
            for i in range(len(row)):
                newrow = row[0:i] + row[i+1:]
                if is_safe(newrow):
                    if DEBUG:
                        print(newrow,"without",i,"safe")
                    safe += 1
                    break
    return safe

print("Part 1:", part1(data))
print("Part 2:", part2(data))
