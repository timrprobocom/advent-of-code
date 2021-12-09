import sys
from collections import Counter
from statistics import median

test = """\
2199943210
3987894921
9856789892
8767896789
9899965678"""

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day09.txt').readlines()

ndata = []
for line in data:
    ndata.append( [int(k) for k in line.rstrip()] )
data = ndata
WIDTH = len(data[0])
HEIGHT = len(data)

dirs = ( (-1,0), (1,0), (0,1), (0,-1) )

def printgrid(grid):
    for row in grid:
        for cell in row:
            print( "%5d"%cell, end = '')
        print()

def part1(data):
    risk = 0
    for y0 in range(HEIGHT):
        for x0 in range(WIDTH):
            fail = False
            this = data[y0][x0]
            for dir in dirs:
                x,y = x0+dir[0],y0+dir[1]
                if 0 <= x < WIDTH and 0 <= y < HEIGHT and data[y][x] <= this:
                    fail = True
                    break
            if not fail:
                risk += this + 1
                if DEBUG:
                    print( x0, y0, this )
    return risk

def part2(data):
    region = [[-1]*WIDTH for _ in range(HEIGHT)]
    reg_no = 0

    # Find all regions surrounded by 9s.

    for y0 in range(HEIGHT):
        for x0 in range(WIDTH):
            if region[y0][x0] >= 0 or data[y0][x0] == 9:
                continue

            # This cell is not part of a region.  Spread to its neighbors.
            # We could do this by counting the cells and setting data to 9,
            # instead of doing a post-processing step.

            unchecked = [(x0,y0)]
            region[y0][x0] = reg_no
            while unchecked:
                x1,y1 = unchecked.pop(0)
                for dir in dirs:
                    x,y = x1+dir[0],y1+dir[1]
                    if 0 <= x < WIDTH and 0 <= y < HEIGHT and data[y][x] < 9 and region[y][x] < 0:
                        region[y][x] = reg_no
                        unchecked.append( (x,y) )
            reg_no += 1
    if DEBUG:
        printgrid(data)
        print()
        printgrid(region)

    # Count the region sizes.

    counts = Counter()
    for y0 in range(HEIGHT):
        for x0 in range(WIDTH):
            counts[region[y0][x0]] += 1

    # Grab the top three.

    del counts[-1]
    if DEBUG:
        print(counts)
    best = counts.most_common(3)
    return best[0][1]*best[1][1]*best[2][1]

print("Part 1:", part1(data) )
print("Part 2:", part2(data) )
