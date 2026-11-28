import sys

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

#
# OK, on a 350x350 grid
# Find the distance from each point in the grid to each point in the 
#

# Start with 10x10.

test = (
    (1, 1),
    (1, 6),
    (8, 3),
    (3, 4),
    (5, 5),
    (8, 9)
)

live = tuple(tuple(int(p) for p in ln.split(' ')) for ln in open('day06.txt').read().splitlines())

data   = test if TEST else live
SQ     = 10   if TEST else 360
TARGET = 32   if TEST else 10000
MAXD   = 25   if TEST else 500

# Create a square grid of size sq containing -1.

def create( sq, data ):
    mat = []
    for i in range(sq):
        mat.append( [-1]*sq )
    for i,p in enumerate(data):
        x,y = p
        mat[y][x] = i
    return mat

mat = create(SQ, data)

def ham(x0,y0,x1,y1):
    return abs(x0-x1) + abs(y0-y1)

for y in range(SQ):
    for x in range(SQ):
        mind = 9999
        minxy = []
        for i,pts in enumerate(data):
            man = abs(x-pts[0]) + abs(y-pts[1])
            if man == mind:
                minxy.append( i )
            elif man < mind:
                mind = man
                minxy = [i]
        if len(minxy) == 1:
            mat[y][x] = minxy[0]

def printgrid(mat):
    for y in range(min(SQ,80)):
        s = ''
        for x in range(min(SQ,80)):
            c = mat[y+50][x+50]
            if c < 0:
                s += '.'
            else:
                s += chr(64+c)
        print(s)

def part1(data):
    tots = [0]*len(data)
    for y in range(SQ):
        for x in range(SQ):
            if mat[y][x] >= 0:
                tots[mat[y][x]] += 1

    for x in range(SQ):
        if mat[x][0] >= 0:  tots[mat[x][0]] = 0
        if mat[x][-1] >= 0: tots[mat[x][-1]] = 0
        if mat[0][x] >= 0:  tots[mat[0][x]] = 0
        if mat[-1][x] >= 0: tots[mat[-1][x]] = 0
    if DEBUG:
        print(tots)
    return max(tots)

def part2(data):
    knt = 0
    for y in range(-MAXD,MAXD):
        if DEBUG:
            print("%d" % y, end='r', flush=True)
        for x in range(-MAXD,MAXD):
            sumh = 0
            for px,py in data:
                sumh += ham(x,y,px,py)
                if sumh >= TARGET:
                    break
            if sumh < TARGET:
                if DEBUG:
                    print(x,y)
                knt += 1
    return knt

print( "Part 1:", part1(data))
print( "Part 2:", part2(data))
