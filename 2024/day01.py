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

l1 = []
l2 = []
for line in data:
    a,b = (int(x) for x in line.split())
    l1.append(a)
    l2.append(b)

def part1(l1,l2):
    l1.sort()
    l2.sort()
    return sum(abs(a-b) for a,b in zip(l1,l2))

def part2(l1,l2):
    return sum( a*l2.count(a) for a in l1)

print("Part 1:", part1(l1,l2))
print("Part 2:", part2(l1,l2))
