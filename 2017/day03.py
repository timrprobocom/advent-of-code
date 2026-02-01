import sys
import math
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

live = 368078

# 17  16  15  14  13
# 18   5   4   3  12
# 19   6   1   2  11
# 20   7   8   9  10
# 21  22  23  24  25  26

# So ring 1 ends at 9, ring 2 ends at 25.

# 16  15  14  13  12  29
# 17   4   3   2  11  28
# 18   5   0   1  10  27
# 19   6   7   8   9  26
# 20  21  22  23  24  25

# Can we figure x,y for a value?
# The ring number is int(sqrt(n-1))

def getRing(n):
    return (int(math.sqrt(n-1))+1)//2

# The NE corner of ring N  is (2N-1)**2 + 2N-1
# The NW corner of ring N  is (2N-1)**2 + 2N-1 + 2N

def corners(r):
    rb = (r+r-1)*(r+r-1)
    ne = rb + r+r-1
    nw = ne + r+r
    sw = nw + r+r
    se = sw + r+r
    return (ne,nw,sw,se)

# The size of ring N is 2N+1 by 2N+1.

def part1(n):
    ring = getRing(n)
    ne, nw, sw, se = corners(ring)
    n -= 1
    if n <= ne:
        dx = ring
        dy = ring - (ne - n)
    elif n <= nw:
        dy = ring
        dx = ring - (nw - n)
    elif n <= sw:
        dx = ring
        dy = ring - (sw - n)
    elif n <= se:
        dy = ring
        dx = ring - (se - n)
    return abs(dx)+abs(dy)

def part2(n):
    # We only need about 5 rings.
    x,y = 10, 10
    grid = [[0]*(x+x) for _ in range(y+y)]
    grid[y][x] = 1
    x += 1
    side = 2
    while 1:
        for length, dx, dy in (side-1, 0, -1), (side, -1, 0), (side, 0, 1), (side+1, 1, 0):
            for _ in range(length):
                s = grid[y-1][x-1] + grid[y-1][x] + grid[y-1][x+1] + grid[y][x-1] + grid[y][x+1] + grid[y+1][x-1] + grid[y+1][x] + grid[y+1][x+1]
                if s > n:
                    return s
                grid[y][x] = s
                x += dx
                y += dy
        side += 2
        if DEBUG:
            for row in grid:
                print(row)
        

print("Part 1:", part1(live))
print("Part 2:", part2(live))