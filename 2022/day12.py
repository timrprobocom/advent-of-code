import sys

test = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [s.rstrip() for s in open('day12.txt').readlines()]

DEBUG = 'debug' in sys.argv


def part1(data,pick):
    w = len(data[0])
    h = len(data)

    visited = set()
    q = []
    for y,row in enumerate(data):
        for x,c in enumerate(row):
            if c in pick:
                visited.add((x,y))
                q.append( (x,y,0) )
    while q:
        x,y,d = q.pop(0)
        if data[y][x] == 'E':
            return d
        c = data[y][x]
        if c == 'S':
            c = 'a'
        for dx,dy in (-1,0),(1,0),(0,-1),(0,1):
            x0=x+dx
            y0=y+dy
            if not y0 in range(h) or not x0 in range(w) or (x0,y0) in visited:
                continue
            if (data[y0][x0] == 'E' and c >= 'y') or \
               (data[y0][x0] != 'E' and ord(data[y0][x0]) <= ord(c)+1):
                visited.add((x0,y0))
                q.append((x0,y0,d+1))
    return -1
    
print("Part 1:", part1(data,'S'))
print("Part 2:", part1(data,'Sa'))

