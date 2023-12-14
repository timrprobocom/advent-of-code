import os
import sys
import itertools

test = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test
else:
    data = open(day+'.txt').read()

DEBUG = 'debug' in sys.argv

# This is one case where the fancy data structure did not help.  I converted
# the grid to a list of coordinate pairs.  69 seconds vs 0.5 seconds.

def makegrid(data):
    return [list(row) for row in data.splitlines()]

grid = makegrid(data)
H = len(grid)
W = len(grid[0])

def tilt_n(grid):
    for x in range(W):
        dy = 0
        for y in range(H):
            c = grid[y][x]
            if c == '.':
                dy += 1
            elif c == '#':
                dy = 0
            elif c == 'O':
                grid[y][x] = '.'
                grid[y-dy][x] = 'O'

def tilt_s(grid):
    for x in range(W):
        dy = 0
        for y in range(H-1,-1,-1):
            c = grid[y][x]
            if c == '.':
                dy += 1
            elif c == '#':
                dy = 0
            elif c == 'O':
                grid[y][x] = '.'
                grid[y+dy][x] = 'O'

def tilt_w(grid):
    for y in range(H):
        dx = 0
        for x in range(W):
            c = grid[y][x]
            if c == '.':
                dx += 1
            elif c == '#':
                dx = 0
            elif c == 'O':
                grid[y][x] = '.'
                grid[y][x-dx] = 'O'

def tilt_e(grid):
    for y in range(H):
        dx = 0
        for x in range(W-1,-1,-1):
            c = grid[y][x]
            if c == '.':
                dx += 1
            elif c == '#':
                dx = 0
            elif c == 'O':
                grid[y][x] = '.'
                grid[y][x+dx] = 'O'

def weight(grid):
    return sum((H-y)*row.count('O') for y,row in enumerate(grid))

def unique(grid):
    return hash(tuple([''.join(row) for row in grid]))

def part1(data):
    grid = makegrid(data)
    tilt_n(grid)
    return weight(grid)

def part2(data):
    grid = makegrid(data)
    seen = [0]
    scores = [0]
    want = -1
    for i in itertools.count():
        tilt_n(grid)
        tilt_w(grid)
        tilt_s(grid)
        tilt_e(grid)
        cur = unique(grid)
        scores.append(weight(grid))
        if DEBUG:
            print(i+1,scores[-1])
        if cur in seen:
            break
        seen.append(cur)
    pat0 = seen.index(cur)
    cycle = len(seen) - pat0
    want =  (1000000000 - pat0) % cycle + pat0
    return scores[want]

print("Part 1:", part1(data)) # 110821
print("Part 2:", part2(data)) # 83516