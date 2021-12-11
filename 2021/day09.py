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

class Neighbors:
#    dirs = (   # For diagonals too
#        (-1,-1), (0,-1), (1,-1),
#        (-1,0),          (1,0),
#        (-1,1),  (0,1),  (1,1)
#    )
    dirs = ( (-1,0), (1,0), (0,1), (0,-1) )

    def __init__( self, w, h ):
        self.w = w
        self.h = h

    def nextto( self, x, y ):
        for dx,dy in self.dirs:
            x0,y0 = x+dx,y+dy
            if 0 <= x0 < WIDTH and 0 <= y0 < HEIGHT:
                yield x0,y0

def printgrid(grid):
    for row in grid:
        for cell in row:
            print( "%5d"%cell, end = '')
        print()

def part1(data):
    adj = Neighbors(WIDTH,HEIGHT)
    risk = 0
    for y0 in range(HEIGHT):
        for x0 in range(WIDTH):
            fail = False
            this = data[y0][x0]
            for x,y in adj.nextto(x0,y0):
                if data[y][x] <= this:
                    fail = True
                    break
            if not fail:
                risk += this + 1
                if DEBUG:
                    print( x0, y0, this )
    return risk

def part2(data):
    region = 0
    counts = Counter()
    adj = Neighbors(WIDTH,HEIGHT)

    # Find all regions surrounded by 9s.

    for y0 in range(HEIGHT):
        for x0 in range(WIDTH):
            if data[y0][x0] == 9:
                continue

            # This cell is not part of a region.  Spread to its neighbors
            # and count them.

            counts[region] = 1
            data[y0][x0] = 9
            unchecked = [(x0,y0)]
            while unchecked:
                x1,y1 = unchecked.pop(0)
                for x,y in adj.nextto(x1,y1):
                    if data[y][x] < 9:
                        counts[region] += 1
                        data[y][x] = 9
                        unchecked.append( (x,y) )
            region += 1

    # Grab the top three.

    del counts[-1]
    if DEBUG:
        print(counts)
    best = counts.most_common(3)
    return best[0][1]*best[1][1]*best[2][1]

print("Part 1:", part1(data) ) # 600
print("Part 2:", part2(data) ) # 987840
