import math
import sys

# 3,4 with 8

t1 = """\
.#..#
.....
#####
....#
...##
"""

# 5,6 with 33

t2 = """\
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""


# 1,2 with 35

t3 = """\
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""

# 6,3 with 41

t4 = """\
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""

# 11,13 with 210

t5 = """\
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

# So, for each location, I should probe in units of the max coordinate.
# In that direction, only look at the integral multiples.  If I find
# one, stop counting.

def read(t):
    return list(list(ln.strip()) for ln in t)

def gcd(x,y):
    while y:
        x,y = y,x%y
    return x

def visible( t, x0, y0, x1, y1 ):
    dx = x1 - x0
    dy = y1 - y0
    
    div = gcd(abs(dx),abs(dy))
    if div == 1:
        return True

    sx = dx // div
    sy = dy // div

    x0 += sx
    y0 += sy

    while (x0,y0) != (x1,y1):
        if t[y0][x0] == '#':
            return False
        x0 += sx
        y0 += sy
    return True


def check( t, tx, ty ):
#    print( "Checking", tx, ty )
    dim = len(t)
    found = set()
    for y1 in range(dim):
        for x1 in range(dim):
            if (x1,y1) == (tx,ty):
                continue
            if t[y1][x1] != '#':
                continue
            if visible( t, tx,ty, x1,y1 ):
                found.add( (x1, y1) )
#    print( len(found) )
    return found



def scan(t):
    maxcount = 0
    for y,ln in enumerate(t):
        for x,cell in enumerate(ln):
#            print( x, y, ln, cell )
            if cell == '.':
                continue
            count = len(check( t, x, y ))
            if count > maxcount:
                maxcount = count
                maxelem = (x,y)
    print( maxelem, " sees ", maxcount )
    return maxcount,maxelem


def laser(t,x0,y0):
    blasted = 200
    while blasted:
        found = check(t,x0,y0)
# If we don't catch them all in one round, eliminate these.
        if len(found) < blasted:
            for x1,y1 in found:
                t[y1][x1] = '.'
            blasted -= len(found)
            continue
        break

# Compute the angle from north.
    data = list(
        ((math.pi/4 - math.atan2((x1-x0),(y1-y0))), x1, y1)
        for x1,y1 in found
    )

# Sort by the angle, pick the 200th.
    data.sort()
    print( "Number 200 is", data[blasted-1] )
    return data[blasted-1][1] * 100 + data[blasted-1][2]

    

def part1():
    scan(read(t1.splitlines()))
    scan(read(t2.splitlines()))
    scan(read(t3.splitlines()))
    scan(read(t4.splitlines()))
    (k5,x5,y0) = scan(read(t5.splitlines()))
    print( "Part 1: ", scan(read(open('day10.txt').readlines())) )

# Answer was 26, 29.
        
def part2():
    laser( read(t5.splitlines()), 11, 13 )
    print( "\nPart 2: ", laser(read(open('day10.txt').readlines()), 26, 29) )

part1()
print()
part2()
