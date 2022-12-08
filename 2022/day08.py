import sys

test = """\
30373
25512
65332
33549
35390"""


if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [s.rstrip() for s in open('day08.txt').readlines()]

DEBUG = 'debug' in sys.argv

def part1(data):
    w = len(data[0])
    h = len(data)
    vis = [[0]*len(data[0]) for _ in range(len(data))]
    vis[0] = [1] * w
    vis[-1] = [1] * w
    for y in range(h):
        vis[y][0] = 1
        vis[y][-1] = 1

    for y in range(1,h-1):
        ll = data[y][0]
        rr = data[y][-1]
        for x in range(1,w-1):
            if data[y][x] > ll:
                vis[y][x] = 1
                ll = data[y][x]
            if data[y][w-x-1] > rr:
                vis[y][w-x-1] = 1
                rr = data[y][w-x-1]

    for x in range(1,w-1):
        ll = data[0][x]
        rr = data[-1][x]
        for y in range(1,h-1):
            if data[y][x] > ll:
                vis[y][x] = 1
                ll = data[y][x]
            if data[h-y-1][x] > rr:
                vis[h-y-1][x] = 1
                rr = data[h-y-1][x]

    return sum(sum(row) for row in vis)

def part2(data):
    w = len(data[0])
    h = len(data)
    vis = [[0]*len(data[0]) for _ in range(len(data))]
    vis[0] = [1] * w
    vis[-1] = [1] * w
    for y in range(h):
        vis[y][0] = 1
        vis[y][-1] = 1

    dirs = ((-1,0),(1,0),(0,-1),(0,1))
    
    maxx = 1
    for y in range(h):
        for x in range(w):
            mult = 1
            # In each direction:
            for dy,dx in dirs:
                x0,y0,delta = x,y,0
                while True:
                    x0 += dx
                    y0 += dy
                    if not x0 in range(w) or not y0 in range(h):
                        break
                    delta += 1
                    if data[y0][x0] >= data[y][x]:
                        break
                mult *= delta
            maxx = max(maxx,mult)
    return maxx

print("Part 1:", part1(data))
print("Part 2:", part2(data))
