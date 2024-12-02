import os
import sys

test = """\
3   4
4   3
2   5
1   3
3   9
3   3"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').readlines()

data = [ [int(i) for i in l.split()] for l in data ]
data = list(sorted(k) for k in zip(*data))

def part1(data):
    return sum(abs(a-b) for a,b in zip(*data))

def part2(l1,l2):
    return sum( a*l2.count(a) for a in l1 )

print("Part 1:", part1(data))
print("Part 2:", part2(*data))
