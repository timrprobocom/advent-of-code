import os
import sys
import itertools

test = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

test1 = """\
.....
.S-7.
.|.|.
.L-J.
....."""

test2 = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test2.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

DEBUG = 'debug' in sys.argv

N = (0,-1)
W = (-1,0)
S = (0,1)
E = (1,0)

dirs = {
    '|': (N,S),
    '-': (E,W),
    'F': (S,E),
    'L': (N,E),
    'J': (N,W),
    '7': (S,W),
    '.': {}
}

WIDTH = range(len(data[0]))
HEIGHT = range(len(data))

data = [list(row) for row in data]

# Find the S.

for Y,row in enumerate(data):
    if 'S' in row:
        X = row.index('S')
        break

# What's below the S?

poss = []
if Y-1 in WIDTH and S in dirs[data[Y-1][X]]:
    poss.append(N)
if Y+1 in WIDTH and N in dirs[data[Y+1][X]]:
    poss.append(S)
if X+1 in WIDTH and W in dirs[data[Y][X+1]]:
    poss.append(E)
if X-1 in WIDTH and E in dirs[data[Y][X-1]]:
    poss.append(W)
poss = tuple(poss)

base = '?'
for k,v in dirs.items():
    if v == poss:
        base = k
        break

if DEBUG:
    print(X,Y,poss,base)

# Replace it.

data[Y][X] = base

# This contains the coordinates of the loop path.

found = {}

def part1(data):
    sumx = 0
    pending = [(X,Y,0)]
    
    # This is a BFS.

    while pending:
        x,y,c = pending.pop(0)
        found[(x,y)] = c
        ch = data[y][x]
        for dx,dy in dirs[ch]:
            x0 = x+dx
            y0 = y+dy
            if x0 in WIDTH and y0 in HEIGHT and (x0,y0) not in found:
                pending.append((x0,y0,c+1))
    return max(found.values())

def blank_path(data,found):
    for y in HEIGHT:
        for x in WIDTH:
            if (x,y) not in found:
                data[y][x] = '.'

def print_data(data):
    for row in data:
        print(''.join(row))

def part2(data,found):
    # Erase all cells not part of the path.
    blank_path(data,found)
    if DEBUG:
        print_data(data)

    # Use the winding rule.  Scanning from the left, if we have 
    # encountered an odd number of edges, then the point is inside.
     
    cells = 0
    for row in data:
        inside = False
        for c in row:
            if c in 'JL|':
                inside = not inside
            if inside and c == '.':
                cells += 1
    return cells
                
        
print("Part 1:", part1(data))
print("Part 2:", part2(data,found))
