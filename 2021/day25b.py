import sys
import time

test = """\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day25.txt').readlines()

HEIGHT = len(data)
WIDTH = len(data[0].rstrip())

# Convert the map to a of lists.

grid = [ list(row.rstrip()) for row in data ]

def printgrid(grid):
    for row in grid:
        print(''.join(row))

# Modify the list in place.

def generation(grid):
    changes = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != '>':
                continue
            dx = 0 if x==WIDTH-1 else x+1
            if grid[y][dx] == '.':
                changes.append((x, y, '.'))
                changes.append((dx, y, '>'))
    for x,y,c in changes:
        grid[y][x] = c

    chgs = len(changes)

    changes = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != 'v':
                continue
            dy = 0 if y==HEIGHT-1 else y+1
            if grid[dy][x] == '.':
                changes.append((x, y, '.'))
                changes.append((x, dy, 'v' ))
    for x,y,c in changes:
        grid[y][x] = c

    return chgs+len(changes)


if DEBUG:
    printgrid(grid)
    print('---')
for gen in range(999):
    n = generation(grid)
    if DEBUG:
        printgrid(grid)
        print(n)
        time.sleep(0.1)
    if not n:
        break

print("Part 1:", gen+1)
