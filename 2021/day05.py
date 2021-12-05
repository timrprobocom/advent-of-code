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
    p1,_,p2 = line.partition(' -> ')
    return eval(p1)+eval(p2)

data = [parse(line) for line in data]

def part(part, data):
    grid = Counter()
    for x0,y0,x1,y1 in data:
        dx = ddx = x1-x0
        dy = ddy = y1-y0

        if ddx < 0:
            dx = -1
        elif ddx > 0:
            dx = 1
        if ddy < 0:
            dy = -1
        elif ddy > 0:
            dy = 1

        if part == 1 and dx and dy:
            continue
        cnt = max( abs(ddx), abs(ddy) ) + 1
        for _ in range(cnt):
            grid[(x0,y0)] += 1
            x0 += dx
            y0 += dy
    return sum(1 for k in grid.values() if k > 1)


print("Part 1:", part(1, data) )
print("Part 2:", part(2, data) )

