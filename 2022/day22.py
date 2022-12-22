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

def part1(data):
    mymap, codes = parse(data)

    # Pad the rows.
    maxw = max(len(row) for row in mymap)
    for y in range(len(mymap)):
        if len(mymap[y]) < maxw:
            mymap[y] += ' '*(maxw-len(mymap[y]))

    direcs = (1,0),(0,1),(-1,0),(0,-1)
    direc = 0

    # Find the start.
    x,y = (0, 0)
    while mymap[y][x] == ' ':
        x += 1

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
                if dx:
                    if dx > 0 and (x0 >= len(mymap[y0]) or mymap[y0][x0] == ' '):
                        x0 = 0
                        while mymap[y0][x0] == ' ':
                            x0 += 1
                    if dx < 0 and (x0 < 0 or mymap[y0][x0] == ' '):
                        x0 = len(mymap[y0])-1
                        while mymap[y0][x0] == ' ':
                            x0 -= 1
                else:
                    if dy > 0 and (y0 >= len(mymap) or mymap[y0][x0] == ' '):
                        y0 = 0
                        while mymap[y0][x0] == ' ':
                            y0 += 1
                    if dy < 0 and (y0 < 0 or mymap[y0][x0] == ' '):
                        y0 = len(mymap)-1
                        while mymap[y0][x0] == ' ':
                            y0 -= 1
                if mymap[y0][x0] == '#':
                    break
                x,y = x0,y0
                if DEBUG:
                    print(x,y)
                # R D L U
                    

    print(x,y)
    return 1000*(y+1)+4*(x+1)+direc

# This is relatively tacky, because we have built these transitions by hand,
# after looking at a physical cube with printed sides.
#
# There should be a way to come up with the cube face transitions automatically.

# For TEST map, 
#      1
#  2 3 4
#      5 6 
#

# For DATA map:
#    1 2
#    3
#  4 5
#  6

# Dirs are R D L U,  > v < ^

tboxes = [ (2,0), (0,1), (1,1), (2,1), (2,2), (3,2)]
dboxes = [ (1,0), (2,0), (1,1), (0,2), (1,2), (0,3)]

# These cube numbers start counting at 1.

#      R     D     L     U
ttrans = [
    [(6,2),(4,1),(3,1),(2,1)], # 1
    [(3,0),(5,3),(6,3),(1,1)], # 2
    [(4,0),(5,0),(2,2),(1,0)], # 3
    [(6,1),(5,1),(3,2),(1,3)], # 4
    [(6,0),(2,3),(3,3),(4,3)], # 5
    [(1,2),(2,0),(5,2),(4,2)]  # 6
]
dtrans = [
    [(2,0),(3,1),(4,0),(6,0)],
    [(5,2),(3,2),(1,2),(6,3)],
    [(2,3),(5,1),(4,1),(1,3)],
    [(5,0),(6,1),(1,0),(3,0)],
    [(2,2),(6,2),(4,2),(3,3)],
    [(5,3),(2,1),(1,1),(4,3)]
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

def edgeover(d1,d2,x,y):
    if d1 == 0:         # RIGHT
        if d2 == 1:
            x = BOX - 1 - y
        elif d2 == 2:
            y = BOX - 1 - y
        elif d2 == 3:
            x = y
    elif d1 == 1:       # DOWN
        if d2 == 0:
            y = BOX - 1 - x
        elif d2 == 2:
            y = x
        elif d2 == 3:
            x = BOX - 1 - x
    elif d1 == 2:       # LEFT
        if d2 == 0:
            y = BOX - 1 - y
        elif d2 == 1:
            x = y
        elif d2 == 3:
            x = BOX - 1 - y
    elif d1 == 3:       # UP
        if d2 == 0:
            y = x
        elif d2 == 1:
            x = BOX - 1 - x
        elif d2 == 2:
            y = BOX - 1 - x

    if d2 == 0:
        x = 0
    elif d2 == 1:
        y = 0
    elif d2 == 2:
        x = BOX - 1
    elif d2 == 3:
        y = BOX - 1
    return x, y

            
# For MY map,
#      1 2
#      3
#    4 5
#    6



def part2(data):
    mymap, codes = parse(data)

    # Pad the rows.
    maxw = max(len(row) for row in mymap)
    for y in range(len(mymap)):
        if len(mymap[y]) < maxw:
            mymap[y] += ' '*(maxw-len(mymap[y]))

    direcs = (1,0),(0,1),(-1,0),(0,-1)
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

    print(x,y)
    return 1000*(y+1)+4*(x+1)+direc


print("Part 1:", part1(data))
print("Part 2:", part2(data))
