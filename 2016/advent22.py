#
# First parse the data.
#
# 33 x 28 grid
#/dev/grid/node-x0-y0     85T   67T    18T   78%

grid = []
row = []

for ln in open('day22.txt'):
    if ln[0] != '/':
        continue
    parts = ln.strip().split()
    subp = parts[0].split('-')
    x = int(subp[1][1:])
    y = int(subp[2][1:])
    used = int(parts[2][:-1])
    avail = int(parts[3][:-1])
    print x, y, used, avail
    row.append( (used,avail) )
    if y == 28:
        grid.append(row)
        row = []

# Find pairs of nodes where:
#   A used not empty
#   A != B
#   A used <= B avail

def countViable():
    count = 0
    for x in range(33):
        for y in range(29):
            if not grid[x][y][0]:
                continue
            # Only 12,14 qualifies for x1,y1
            for x1 in range(33):
                for y1 in range(29):
                    if x1 == x and y1 == y:
                        continue
                    if grid[x][y][0] <= grid[x1][y1][1]:
                        count += 1
    return  count

# Now I want to read from x=32 y=0
# Empty space is at x=12 y=14
# There is a wall at y=13 with an opening at x=0.
# Two phases:
#  1. Move to x=31 y=0
#  2. Use scoot-around movements to get to x=0 y=0
#
# How would you automate this?
#   
