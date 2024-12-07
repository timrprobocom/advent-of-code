import os
import sys
from collections import defaultdict

test = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

dx = []
for row in data:
    dx.append( list(int(k.rstrip(':')) for k in row.split()) )

def part1(data):
    sumx = 0
    for row in data:
        k = row[0]
        maybe = [row[1]]
        for v1 in row[2:]:
            maybe = [ s 
                for m in maybe
                for s in (m+v1, m*v1)
                if s <= k
            ]
        if k in maybe:
            sumx += k
    return sumx

def part2(data):
    sumx = 0
    for row in data:
        k = row[0]
        maybe = [row[1]]
        for v1 in row[2:]:
            maybe = [ s 
                for m in maybe
                for s in (m+v1, m*v1, int(str(m)+str(v1)))
                if s <= k
            ]
        if k in maybe:
            sumx += k
    return sumx

print("Part 1:", part1(dx))
print("Part 2:", part2(dx))
