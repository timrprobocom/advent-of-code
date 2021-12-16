import sys
from collections import Counter

test = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [line.rstrip() for line in open('day05.txt')]

def parse(line):
    return eval(line.replace(' -> ',','))

data = [parse(line) for line in data]

def cmp(a,b):
    return (a>b)-(a<b)

def part(part, data):
    grid = Counter()
    for x0,y0,x1,y1 in data:
        cnt = max( abs(x1-x0), abs(y1-y0) ) + 1
        dx = cmp(x1,x0)
        dy = cmp(y1,y0)

        if part == 1 and dx and dy:
            continue

        for _ in range(cnt):
            grid[(x0,y0)] += 1
            x0 += dx
            y0 += dy
    return sum(k > 1 for k in grid.values())


print("Part 1:", part(1, data) ) # 6564
print("Part 2:", part(2, data) ) # 19172

