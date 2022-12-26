import sys
from collections import defaultdict, deque

test = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [k.strip() for k in open('day24.txt').readlines()]

DEBUG = 'debug' in sys.argv

try:
    from math import lcm
except ImportError:
    def lcm(a,b):
        aa, bb = a, b
        while aa != bb:
            if aa < bb:
                aa += a
            else:
                bb += b
        return aa


WID = len(data[0])-2
HGT = len(data)-2
IN = (0,-1)
OUT = (WID-1,HGT)
CYCLE = lcm(WID,HGT)

def parse(data):
    new = defaultdict(list)
    for y,row in enumerate(data[1:-1]):
        for x,col in enumerate(row[1:-1]):
            if col == '#':
                print(x,y)
                assert col!='#'
            if col != '.':
                new[(x,y)].append(col)
    return new

data = parse(data)

dircodes = {
    '>': (1,0),
    'v': (0,1),
    '<': (-1,0),
    '^': (0,-1)
}

direcs = ((1,0),(0,1),(-1,0),(0,-1),(0,0))

def shift(data):
    new = defaultdict(list)
    for (x,y),dirs in data.items():
        for v in dirs:
            dx,dy = dircodes[v]
            x0 = (x + dx) % WID
            y0 = (y + dy) % HGT
            new[(x0,y0)].append(v)
    return new

def plot(grid):
    plt = [['.']*WID for _ in range(HGT)]
    for (x,y),v in grid.items():
        if len(v) > 1:
            plt[y][x] = str(len(v))
        else:
            plt[y][x] = v[0]
    print('#'*(WID+2))
    for row in plt:
        print('#'+(''.join(row))+'#' )
    print('#'*(WID+2))

def solve( startpt, endpt, t ):
    start = startpt + (t,)
    q = deque()
    q.append(start)
    seen = []
    while q:
        x,y,t = q.popleft()
        if DEBUG:
            print(x,y,t)
        t += 1
        while t >= len(seen):
            seen.append(set())
        grid = patterns[t % CYCLE]

        for dx,dy in direcs:
            x0 = x + dx
            y0 = y + dy
            if (x0,y0) == endpt:
                return t
            if x0 in range(WID) and y0 in range(HGT) and (x0,y0) not in grid and (x0,y0) not in seen[t]:
                seen[t].add( (x0,y0) )
                q.append( (x0,y0,t) )
        
        # As a last resort, stay at home.

        if (x,y) == startpt:
            q.append( (x,y,t) )

    print("fail at",t)
    return -1

patterns = []
for i in range(CYCLE):
    patterns.append(data)
    data = shift(data)

def part1(data):
    t = solve( (0,-1), OUT, 0 )
    yield t
    t = solve( (WID-1,HGT), (0,0), t-1 )
    assert t > 0
    t = solve( (0,-1), OUT, t-1 )
    yield t

for p,t in enumerate(part1(data)):
    print(f"Part {p+1}: {t}")

# should be 322 974
