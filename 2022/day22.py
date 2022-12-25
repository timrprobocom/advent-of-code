import sys
from collections import defaultdict

test = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

if 'test' in sys.argv:
    data = test.splitlines()
    BOX = 4 
else:
    data = [l.rstrip() for l in open('day22.txt').readlines()]
    BOX = 50

DEBUG = 'debug' in sys.argv

def parse(data):
    mymap = []
    for row in data:
        if not row:
            continue
        if row[0] == '1':
            codes = row
        else:
            mymap.append(row)
    return mymap, codes

def instruct(codes):
    accum = 0
    for c in codes:
        if c in 'LR':
            if accum:
                yield accum
                accum = 0
            yield c
        else:
            accum = accum * 10 + ord(c) - ord('0')
    if accum:
        yield accum

R,D,L,U = range(4)
direcs = (1,0),(0,1),(-1,0),(0,-1)

# Discover the layout,

boxes = []
for y in range(0,len(data)-2,BOX):
    for x in range(0,len(data[y]),BOX):
        if data[y][x] != ' ':
            boxes.append( (x,y) )

# For TEST map, 
#      0
#  1 2 3
#      4 5 

# For DATA map:
#    0 1
#    2
#  3 4
#  5

# Apply rules to find the other connections.  This table says that,
# from a cube at x,y, we can get to cube at x-1,x+1 from our left,
# entering going down.  We can also get to it from our down, 
# entering going left.

rules = [
    (-1, +1, L, D),
    (-1, +1, D, L),
    (-2, +1, U, D),
    (-2, +1, D, U),
    (+1, +1, R, D),
    (+1, +1, D, R),
    (+2, +1, D, U),
    (+3, +1, L, U),
    (+1, +2, R, L),
    (-1, +2, L, R),
    (-1, +2, R, L),
    (-1, +3, U, R),
    (-2, +3, U, U),
]

# Find the cube structure.

def find_cube(data):
    trans = {}
    boxint = [(x//BOX,y//BOX) for x,y in boxes]

    # This finds all the direct connections, both directions.

    for n,(x,y) in enumerate(boxint):
        for c,(dx,dy) in enumerate(direcs):
            if (x+dx,y+dy) in boxint:
                bi = boxint.index((x+dx,y+dy))
                trans[(n,c)] = (bi,c)
                trans[(bi,c^2)] = (n,c^2)


    for b in range(6):
        for d in range(4):
            if (b,d) in trans:
                continue
            x,y = boxint[b]
            for dx,dy,md,od in rules:
                if (b,md) in trans:
                    continue
                x0 = x+dx
                y0 = y+dy
                if (x0,y0) not in boxint:
                    continue
                b0 = boxint.index((x0,y0))
                if (b,md) not in trans:
                    trans[b,md] = (b0,od)
                if (b0,od^2) not in trans:
                    trans[b0,od^2] = (b,md^2)

    return trans

# Find the box ordinal that contains the point x,y.

def findbox(x,y):
    for bn,(bx,by) in enumerate(boxes):
        if x in range(bx,bx+BOX) and y in range(by,by+BOX):
            return bn
    return -1

# Right to up: y becomes x
# Up to right
# Left to down
# Down to left

# \ d2 
#  \        R       D       L       U
#d1 \ sets  y       x       y       x
#-------------------------------------------
# R  |      y      N-y     N-y      y
#    |
# D  |     N-x      x       x      N-x
#    |
# L  |     N-y      y       y      N-y
#    |
# U  |      x      N-x     N-x      x

# This implements the truth table, but I don't think this is either
# easier to read nor more efficient than an if/elif chain.

def edgeover(d1,d2,x,y):
    if d1 in (R,L):
        xy = y
    else:
        xy = x
    if d1 ^ d2 in (1,2):
        xy = BOX - 1 - xy

    if d2 in (R,L):
        x = 0 if d2==R else BOX-1
        y = xy
    else:
        x = xy
        y = 0 if d2==D else BOX-1

    return x, y


def part1(data):
    mymap, codes = parse(data)

    # Pad the rows.
    maxw = max(len(row) for row in mymap)
    for y in range(len(mymap)):
        if len(mymap[y]) < maxw:
            mymap[y] += ' '*(maxw-len(mymap[y]))

    direc = 0

    # Find the start.
    x,y = boxes[0]

    for code in instruct(codes):
        if DEBUG:
            print('---',code)
        if code == 'L':
            direc = (direc + 3) % 4
        elif code == 'R':
            direc = (direc + 1) % 4
        else:
            dx,dy = direcs[direc]
            for i in range(code):
                x0 = x+dx
                y0 = y+dy

                # Handle wraps.

                if dx > 0 and (x0 >= len(mymap[y0]) or mymap[y0][x0] == ' '):
                    x0 = 0
                if dx < 0 and (x0 < 0 or mymap[y0][x0] == ' '):
                    x0 = len(mymap[y0])-1
                if dy > 0 and (y0 >= len(mymap) or mymap[y0][x0] == ' '):
                    y0 = 0
                if dy < 0 and (y0 < 0 or mymap[y0][x0] == ' '):
                    y0 = len(mymap)-1

                while mymap[y0][x0] == ' ':
                    x0 += dx
                    y0 += dy

                # Check for a wall.
                if mymap[y0][x0] == '#':
                    break

                x,y = x0,y0
                if DEBUG:
                    print(x,y)

    if DEBUG:
        print("final",x,y)
    return 1000*(y+1)+4*(x+1)+direc

def part2(data):
    mymap, codes = parse(data)
    trans = find_cube(data)

    # Pad the rows.
    maxw = max(len(row) for row in mymap)
    for y in range(len(mymap)):
        if len(mymap[y]) < maxw:
            mymap[y] += ' '*(maxw-len(mymap[y]))

    direc = 0

    # Find the start.
    x,y = boxes[0]
    box = findbox(x,y)

    for code in instruct(codes):
        if DEBUG:
            print('---',code)
        if code == 'L':
            direc = (direc + 3) % 4
        elif code == 'R':
            direc = (direc + 1) % 4
        else:
            for i in range(code):
                dx,dy = direcs[direc]
                x0 = x+dx
                y0 = y+dy
                if box == findbox(x0,y0):
                    if mymap[y0][x0] == '#':
                        break
                    x,y = x0,y0
                    continue

                newbox,newdir = trans[box,direc]
                xoff = x0 - boxes[box][0]
                yoff = y0 - boxes[box][1]
                if DEBUG:
                    print(f'FROM {box+1} d{direc} {xoff},{yoff} {x0},{y0}')
                xoff,yoff = edgeover( direc, newdir, xoff, yoff )
                x0 = xoff + boxes[newbox][0]
                y0 = yoff + boxes[newbox][1]
                if DEBUG:
                    print(f'  TO {newbox+1} d{newdir} {xoff},{yoff} {x0},{y0}')

                if mymap[y0][x0] == '#':
                    break
                x,y,box,direc = x0,y0,newbox,newdir
                if DEBUG:
                    print(x,y)

    if DEBUG:
        print("final",x,y)
    return 1000*(y+1)+4*(x+1)+direc

print("Part 1:", part1(data))
print("Part 2:", part2(data))
