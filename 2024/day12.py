import os
import sys
from collections import defaultdict

test = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

WIDTH = len(data[0])
HEIGHT = len(data)

dirs = ((-1,0),(0,1),(0,-1),(1,0))

def getregion( region, x, y ):
    queue = [(x,y)]
    found = set(queue)
    while queue:
        (x,y) = queue.pop(0)
        for dx,dy in dirs:
            x0 = x+dx
            y0 = y+dy
            if (x0,y0) in region and (x0,y0) not in found:
                found.add( (x0,y0) )
                queue.append((x0,y0))
    return found

def distinctsets(region):
    regions = []
    while region:
        (x,y) = region.pop()
        newreg = getregion( region, x, y )
        regions.append( newreg )
        region -= newreg
    return regions

# Process the map.  First, collect all similar cells.  Then, split letters thatn
# have multiple distinct regions.

stats = defaultdict(set)
for y,row in enumerate(data):
    for x,c in enumerate(row):
        stats[c].add( (x,y) )

regions = []
for k,v in stats.items():
    for i,s in enumerate(distinctsets(v)):
        regions.append( (f"{k}{i}", s) )

if DEBUG:
    for k,v in regions:
        print(k,v)

def perimeter(region):
    return sum(
        (x+dx,y+dy) not in region
        for x,y in region
        for dx,dy in dirs
    )

# Find all of the border edges.  This includes all of the sides where they border, so
# it includes and x,y and a direction.

def find_border(region):
    border = set()
    for (x,y) in region:
        for (dx,dy) in dirs:
            if x in range(WIDTH) and y in range(HEIGHT) and (x+dx,y+dy) not in region:
                border.add( (x,y,dx,dy) )
    return border

# Looking in a direction perpendicular to the outside edge(s), remove any edges
# that are also on the same border.

def sides(border):
    sides = 0
    while border:
        x,y,dx,dy = border.pop()
        for pdx,pdy in (-dy,dx),(dy,-dx):
            x0 = x+pdx
            y0 = y+pdy
            while (x0,y0,dx,dy) in border:
                border.remove( (x0,y0,dx,dy) )
                x0 += pdx
                y0 += pdy
        sides += 1
    return sides

def part1(regions):
    sumx = 0
    for _,v in regions:
        sumx += len(v) * perimeter(v)
    return sumx

def part2(data):
    sumx = 0
    for _,v in regions:
        border = find_border(v)
        sumx += len(v) * sides(border)
    return sumx

print("Part 1:", part1(regions))
print("Part 2:", part2(regions))