import sys

test = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

test2 = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

if 'test' in sys.argv:
    data = test.splitlines()
    data2 = test2.splitlines()
else:
    data = [s.rstrip() for s in open('day09.txt').readlines()]
    data2 = data

DEBUG = 'debug' in sys.argv

dirs = {
    'L': (-1, 0),
    'U': (0, -1),
    'R': (1, 0),
    'D': (0, 1)
}

def move(h,t):
    if abs(h[0]-t[0]) <= 1 and abs(h[1]-t[1]) <= 1:
        return t
    if h[0] == t[0]:
        tail = (t[0],(h[1]+t[1])//2)
    elif h[1] == t[1]:
        tail = ((h[0]+t[0])//2, t[1])
    # So one of them is off by 2.
    elif abs(h[0]-t[0]) == 2:
        if abs(h[1]-t[1]) == 2:
            tail = ((h[0]+t[0])//2, (h[1]+t[1])//2)
        else:
            tail = ((h[0]+t[0])//2, h[1])
    else:
        tail = (h[0],(h[1]+t[1])//2)
    return tail

def plot(visit):
    minx = min(k[0] for k in visit)
    miny = min(k[1] for k in visit)
    maxx = max(k[0] for k in visit)
    maxy = max(k[1] for k in visit)
    w = maxx - minx + 1
    h = maxy - miny + 1
    mapx = [['.']*w for _ in range(h)]
    for pt in visit:
        mapx[pt[1]-miny][pt[0]-minx] = '#'
    mapx[-miny][-minx] = 's'
    for row in mapx:
        print(''.join(row))

def part1(data,n):
    ropes = [(0,0)]*n
    visited = set((ropes[-1],))
    for line in data:
        delta = dirs[line[0]]
        nnn = int(line[2:])
        for n in range(nnn):
            ropes[0] = ropes[0][0]+delta[0],ropes[0][1]+delta[1]
            for i in range(len(ropes)-1):
                ropes[i+1] = move(ropes[i],ropes[i+1])
            visited.add(ropes[-1])
    if DEBUG:
        plot(visited)
    return len(visited)

print("Part 1:", part1(data,2))
print("Part 2:", part1(data2,10))

