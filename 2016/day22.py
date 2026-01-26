import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

#
# First parse the data.
#
# 33 x 28 grid
#/dev/grid/node-x0-y0     85T   67T    18T   78%

grid = []

for ln in open('day22.txt'):
    if ln[0] != '/':
        continue
    parts = ln.strip().split()
    subp = parts[0].split('-')
    x = int(subp[1][1:])
    y = int(subp[2][1:])
    used = int(parts[2][:-1])
    avail = int(parts[3][:-1])
    if DEBUG:
        print( x, y, used, avail )
    if y >= len(grid):
        grid.append([])
    grid[y].append( (used,avail) )

# Find pairs of nodes where:
#   A used not empty
#   A != B
#   A used <= B avail

def part1(grid):
    count = 0
    for y,row in enumerate(grid):
        for x,(used,_) in enumerate(row):
            if not used:
                continue
            for y1,row1 in enumerate(grid):
                for x1,(_,avail) in enumerate(row1):
                    if x1 == x and y1 == y:
                        continue
                    count += used <= avail
    return count

def printgrid(grid):
    for row in grid:
        for col in row:
            print( "%3d/%3d" % col, end=' ')
        print()

print('Part 1:', part1(grid))
if DEBUG:
    printgrid(grid)

# Now I want to read from x=32 y=0
# Empty space is at x=12 y=14
# There is a wall at y=13 with an opening at x=0.
# Two phases:
#  1. Move to x=31 y=0
#  2. Use scoot-around movements to get to x=0 y=0
#
# How would you automate this?
#
# There is an answer by observation.  The hole is at x=12, but sits
# right below the wall  We move left 12 to x=0, up 2, right 32, up 12.
# That puts us just to the left of the target.  5 swaps moves the 
# target one unit left and positions us in front (R, D, L, L, U).

# 5 x 33 + 12 + 2 + 32 + 12 = 165 + 58 = 213

# Part 2 is 213
print('Part 2:', 213)
