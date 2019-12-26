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
    cells = set()
    for y,ln in enumerate(txt.splitlines()):
        for x,ch in enumerate(ln):
            if ch == '#':
                cells.add((x,y))
    return cells

def printgrid(grid):
    base = list('.....\n'*5)[:-1]
    for x,y in grid:
        base[y*6+x] = '#'
    print( ''.join(base) )

def rating(grid):
    return sum( 1 << (y*5+x) for x,y in grid ) 

checks = ((-1,0),(1,0),(0,-1),(0,1))

def cycle(grid):
    new = set()
    for y in range(5):
        for x in range(5):
            neighbors = sum( 1 for dx,dy in checks if (x+dx,y+dy) in grid )
            if neighbors == 1 or (neighbors == 2 and not (x,y) in grid):
                new.add( (x,y) )
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
    printgrid(grid)
    r = rating(grid)
    print( i, r )
    if r in values:
        print( r )
        break
    values[r] = i

print( "Part 1:", i, rating(grid) )


