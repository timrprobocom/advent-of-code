import sys
from collections import deque

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
    data = open('day22.txt').readlines()
    BOX = 50

DEBUG = 'debug' in sys.argv

def parse(data):
    mymap = []
    for row in data:
        row = row.rstrip()
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

# This is relatively tacky, because we have built these transitions by hand,
# after looking at a physical cube with printed sides.
#
# There should be a way to come up with the cube face transitions automatically.
# But that's hard...

# For TEST map, 
#      1
#  2 3 4
#      5 6 

# For DATA map:
#    1 2
#    3
#  4 5
#  6

tboxes = [ (2,0), (0,1), (1,1), (2,1), (2,2), (3,2)]
dboxes = [ (1,0), (2,0), (1,1), (0,2), (1,2), (0,3)]

# These cube numbers start counting at 1.

# The first row tells about the transitions at each edge of box #1.
# The columns are as labeled.  So, the first entry says, if we leave 
# box #1 while moving right, that transitions to box #6 moving left.
# This is a comfusing way to look at it, because "moving left" means 
# we're entering at the RIGHT edge.

#      R     D     L     U
ttrans = [
    [(6,L),(4,D),(3,D),(2,D)], # 1
    [(3,R),(5,U),(6,U),(1,D)], # 2
    [(4,R),(5,R),(2,L),(1,R)], # 3
    [(6,D),(5,D),(3,L),(1,U)], # 4
    [(6,R),(2,U),(3,U),(4,U)], # 5
    [(1,L),(2,R),(5,L),(4,L)]  # 6
]
dtrans = [
    [(2,R),(3,D),(4,R),(6,R)],
    [(5,L),(3,L),(1,L),(6,U)],
    [(2,U),(5,D),(4,D),(1,U)],
    [(5,R),(6,D),(1,R),(3,R)],
    [(2,L),(6,L),(4,L),(3,U)],
    [(5,U),(2,D),(1,D),(4,U)]
]


if "test" in sys.argv:
    boxes = [(BOX*x,BOX*y) for x,y in tboxes]
    trans = ttrans
else:
    boxes = [(BOX*x,BOX*y) for x,y in dboxes]
    trans = dtrans

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
# easier to read nor more efficient than the if/elif chain.

def edgeover(d1,d2,x,y):
    if d1 in (R,L):
        xy = y
    else:
        xy = x
    if d1 ^ d2 in (1,2):
        xy = BOX - 1 - xy

    if d2 in (R,L):
        y = xy
    else:
        x = xy

    if d2 == 0:
        x = 0
    elif d2 == 1:
        y = 0
    elif d2 == 2:
        x = BOX - 1
    elif d2 == 3:
        y = BOX - 1
    return x, y


def edgeover1(d1,d2,x,y):
    if d1 == R:         # RIGHT
        if d2 == D:
            x = BOX - 1 - y
        elif d2 == L:
            y = BOX - 1 - y
        elif d2 == U:
            x = y
    elif d1 == D:       # DOWN
        if d2 == R:
            y = BOX - 1 - x
        elif d2 == L:
            y = x
        elif d2 == U:
            x = BOX - 1 - x
    elif d1 == L:       # LEFT
        if d2 == R:
            y = BOX - 1 - y
        elif d2 == D:
            x = y
        elif d2 == U:
            x = BOX - 1 - y
    elif d1 == U:       # UP
        if d2 == R:
            y = x
        elif d2 == D:
            x = BOX - 1 - x
        elif d2 == L:
            y = BOX - 1 - x

    if d2 == R:
        x = 0
    elif d2 == D:
        y = 0
    elif d2 == L:
        x = BOX - 1
    elif d2 == U:
        y = BOX - 1
    return x, y


def part2(data):
    mymap, codes = parse(data)

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

                newbox,newdir = trans[box][direc]
                newbox -= 1
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
