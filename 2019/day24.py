import itertools
import sys
from pprint import pprint

inp="""\
...#.
#.##.
#..##
#.###
##..."""

test = """\
....#
#..#.
#..##
..#..
#...."""

def makegrid(txt):
    grid = []
    for ln in txt.splitlines():
        grid.append( list(".#".index(c) for c in ln) )
    return grid


def rating(grid):
    return sum( cell << i for i,cell in enumerate(sum(grid,[])))

valid = (0,1,2,3,4)

checks = ((-1,0),(1,0),(0,-1),(0,1))

def cycle(grid):
    new = []
    for y in range(len(grid)):
        row = []
        for x in range(len(grid[0])):
            neighbors = sum(
                (grid[y+dy][x+dx] 
                for dx,dy in checks
                if x+dx in valid and y+dy in valid)
            )
            if neighbors == 1 or (neighbors == 2 and grid[y][x] == 0):
                row.append(1)
            else:
                row.append(0)
        new.append( row )
    return new


if 'test' in sys.argv:
    grid = makegrid(test)
else:
    grid = makegrid(inp)
pprint( grid )
print( rating( grid) )

values = {rating(grid): 0}
for i in itertools.count(1):
    grid = cycle(grid)
    pprint( grid )
    r = rating(grid)
    print( i, r )
    if rating(grid) in values:
        print( r )
        break
    values[r] = i

print( "Part 1:", i, rating(grid) )


