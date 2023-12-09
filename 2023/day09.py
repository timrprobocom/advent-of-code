import os
import sys
import itertools

test = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open(day+'.txt').readlines()

DEBUG = 'debug' in sys.argv

data = [ [int(x) for x in line.split()] for line in data]


def part1(part,data):
    sumx = 0
    for row in data:
        stack = [row]
        # Determine differences
        while not all(r == row[0] for r in row):
            row = [b-a for a,b in itertools.pairwise(row)]
            stack.append( row )
        incr = 0
        for row in reversed(stack):
            incr = row[-1]+incr if part==1 else row[0]-incr
        sumx += incr  

    return sumx

print("Part 1:", part1(1,data))
print("Part 2:", part1(2,data))
