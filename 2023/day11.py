import os
import sys
import itertools

test = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

DEBUG = 'debug' in sys.argv

# Find the rows without galaxies.

nogrow = [n for n,row in enumerate(data) if '#' not in row]

# Find the columns without galaxies.

counts = [0]*len(data[0])
for row in data:
    for n,col in enumerate(row):
        if col == '#':
            counts[n] += 1

nogcol = [n for n,val in enumerate(counts) if not val]

def expand(data, delta):
    stars = []
    dy = 0
    for y,row in enumerate(data):
        if y in nogrow:
            dy += delta
            continue
        dx = 0
        for x,col in enumerate(row):
            if x in nogcol:
                dx += delta
            elif col == '#':
                stars.append( (x+dx,y+dy))
    return stars

def part1(data,delta):
    stars = expand(data,delta-1)
    mandist = 0
    for i in range(len(stars)-1):
        for j in range(i,len(stars)):
            mandist += abs(stars[i][0]-stars[j][0]) + abs(stars[i][1]-stars[j][1])
    return mandist

print("Part 1:", part1(data,2))
if 'test' in sys.argv:
    print("Test 10:", part1(data,10))
    print("Test 100:", part1(data,100))
print("Part 2:", part1(data,1000000))
