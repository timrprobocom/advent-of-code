import math
import sys

DEBUG = 'debug' in sys.argv
TEST = 'test' in sys.argv

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

live = open('day10.txt').read()

def read(t):
    t = t.splitlines()
    return [list(ln.strip()) for ln in t]

def gcd(x,y):
    while y:
        x,y = y,x%y
    return x

def visible( graph, x0, y0, x1, y1 ):
    # Get the slope of the line.
    dx = x1 - x0
    dy = y1 - y0
    
    # Compute the GCD.  If they are relatively prime, then this star is visible.
    div = gcd(abs(dx),abs(dy))
    if div == 1:
        return True

    # Compute the steps at which stars will interfere.
    sx = dx // div
    sy = dy // div

    # until we reach the target (which we always will), check for blocks.
    x0 += sx
    y0 += sy
    while (x0,y0) != (x1,y1):
        if graph[y0][x0] == '#':
            return False
        x0 += sx
        y0 += sy
    return True


def check( graph, tx, ty ):
    if DEBUG:
        print( "Checking", tx, ty )
    dim = len(graph)
    found = set()
    for y1 in range(dim):
        for x1 in range(dim):
            if (x1,y1) == (tx,ty):
                continue
            if graph[y1][x1] != '#':
                continue
            if visible( graph, tx,ty, x1,y1 ):
                found.add( (x1, y1) )
    if DEBUG:
        print( len(found) )
    return found



def scan(graph):
    maxcount = 0
    for y,ln in enumerate(graph):
        for x,cell in enumerate(ln):
            if DEBUG:
                print( x, y, ln, cell )
            if cell == '.':
                continue
            count = len(check( graph, x, y ))
            if count > maxcount:
                maxcount = count
                maxelem = (x,y)
    if DEBUG:
        print( maxelem, "sees", maxcount )
    return maxcount, maxelem


def laser(graph,x0,y0):
    remains = 200
    while remains:
        found = check(graph,x0,y0)
# If we don't catch them all in one round, eliminate these.
        if len(found) < remains:
            for x1,y1 in found:
                graph[y1][x1] = '.'
            remains -= len(found)
            continue
        break

# Compute the angle from north.
    data = [
        ((math.pi/4 - math.atan2((x1-x0),(y1-y0))), x1, y1)
        for x1,y1 in found
    ]

# Sort by the angle, pick the 200th.
    data.sort()
    if DEBUG:
        print( "Number 200 is", data[remains-1] )
    return data[remains-1][1] * 100 + data[remains-1][2]


def part1t():
    print('Part 1:',scan(read(t1)))
    print('Part 1:',scan(read(t2)))
    print('Part 1:',scan(read(t3)))
    print('Part 1:',scan(read(t4)))
    print('Part 1:',scan(read(t5)))

def part1():
    return scan(read(live))[0]

# Answer was 26, 29.
        
def part2(data):
    best = scan(read(live))[1]
    return laser(read(live), *best)

if TEST:
    data = t5
    part1t()
else:
    data = live
    print( "Part 1:", part1())

print( "Part 2:", part2(data))
