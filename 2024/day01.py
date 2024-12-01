import sys
import re

test = """\
3   4
4   3
2   5
1   3
3   9
3   3"""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day01.txt').readlines()

data = ((int(a),int(b)) for a,b in (z1.split() for z1 in data))
data = list(sorted(k) for k in zip(*data))

def part1(data):
    return sum(abs(a-b) for a,b in zip(*data))

def part2(l1,l2):
    return sum( a*l2.count(a) for a in l1 )

print("Part 1:", part1(data))
print("Part 2:", part2(*data))
