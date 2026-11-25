import itertools
import sys
from pprint import pprint

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

test = """\
....#
#..#.
#..##
..#..
#...."""

live="""\
...#.
#.##.
#..##
#.###
##..."""

if TEST:
    data = test
    depth = 10
else:
    data = live
    depth = 200


def makegrid(txt):
    grid = []
    for ln in txt.splitlines():
        grid.append( list(".#".index(c) for c in ln) )
    return grid

def rating(grid):
    return sum( cell << i for i,cell in enumerate(sum(grid,[])))

valid = (0,1,2,3,4)

checks = ((-1,0),(1,0),(0,-1),(0,1))

def cycle(grid):
    new = []
    for y in range(len(grid)):
        row = []
        for x in range(len(grid[0])):
            neighbors = sum(
                (grid[y+dy][x+dx] 
                for dx,dy in checks
                if x+dx in valid and y+dy in valid)
            )
            if neighbors == 1 or (neighbors == 2 and grid[y][x] == 0):
                row.append(1)
            else:
                row.append(0)
        new.append( row )
    return new


def part1(grid):
    values = {rating(grid): 0}
    for i in itertools.count(1):
        grid = cycle(grid)
        r = rating(grid)
        if DEBUG:
            pprint( grid )
            print( i, r )
        if rating(grid) in values:
            if DEBUG:
                print( r )
            break
        values[r] = i
    return rating(grid)


#     |     |         |     |     
# 0,0 | 1,0 |   2,0   | 3,0 | 4,0 
#     |     |         |     |     
#-----+-----+---------+-----+-----
#     |     |         |     |     
# 0,1 | 1,1 |   2,1   | 3,1 | 4,1 
#     |     |         |     |     
#-----+-----+---------+-----+-----
#     |     |A|B|C|D|E|     |     
#     |     |-+-+-+-+-|     |     
#     |     |F|G|H|I|J|     |     
#     |     |-+-+-+-+-|     |     
# 0,2 | 1,2 |K|L|?|N|O| 3,2 | 4,2 
#     |     |-+-+-+-+-|     |     
#     |     |P|Q|R|S|T|     |     
#     |     |-+-+-+-+-|     |     
#     |     |U|V|W|X|Y|     |     
#-----+-----+---------+-----+-----
#     |     |         |     |     
# 0,3 | 1,3 |   2,3   | 3,3 | 4,3 
#     |     |         |     |     
#-----+-----+---------+-----+-----
#     |     |         |     |     
# 0,4 | 1,4 |   2,4   | 3,4 | 4,4 
#     |     |         |     |     
#Tile 19 has four adjacent tiles: 14, 18, 20, and 24.
#Tile G has four adjacent tiles: B, F, H, and L.
#Tile D has four adjacent tiles: 8, C, E, and I.
#Tile E has four adjacent tiles: 8, D, 14, and J.
#Tile 14 has eight adjacent tiles: 9, E, J, O, T, Y, 15, and 19.
#Tile N has eight adjacent tiles: I, O, S, and five tiles within the sub-grid marked ?.

#  0,0 has 4:  (1,2,-1)  (2,1,-1)  (1,0,0)  (0,1,0)
#  1,0 has 4:  (0,0,0)   (2,1,-1)  (2,0,0)  (1,1,0)
#  2,0 has 4:  (1,0,0)   (2,1,-1)  (3,0,0)  (2,1,0)
#  3,0 has 4:  (2,0,0)   (2,1,-1)  (4,0,0)  (3,1,0)
#  4,0 has 4:  (3,0,0)   (2,1,-1)  (3,2,-1) (4,1,0)

#  0,1 has 4:  (1,2,-1)  (0,0,0)   (1,1,0)  (0,2,0)
#  1,1 has 4:  (0,1,0)   (1,0,0)   (2,1,0)  (1,2,0)
#  2,1 has 8:  (1,1,0)   (2,0,0)   (3,1,0)  (*,0,1)
#  3,1 has 4:  (2,1,0)   (3,0,0)   (4,1,0)  (3,2,0)
#  4,1 has 4:  (3,1,0)   (4,0,0)   (3,2,-1) (4,2,0)

#  0,2 has 4:  (1,2,-1)  (0,1,0)   (1,2,0)  (0,3,0)
#  1,2 has 8:  (0,2,0)   (1,1,0)   (0,*,0)  (1,2,0)
#  2,2 has 0:  (2,2,0)
#  3,2 has 8:  (4,*,0)   (3,1,0)   (4,2,0)  (3,3,0)
#  4,2 has 4:  (3,2,0)   (4,1,0)   (1,2,-1) (4,3,0)

#  0,3 has 4:  (1,2,-1)  (0,2,0)   (1,3,0)  (0,4,0)
#  1,3 has 4:  (0,1,0)   (1,2,0)   (2,3,0)  (1,4,0)
#  2,3 has 8:  (1,1,0)   (2,2,0)   (3,3,0)  (*,0,1)
#  3,3 has 4:  (2,1,0)   (3,2,0)   (4,3,0)  (3,4,0)
#  4,3 has 4:  (3,1,0)   (4,2,0)   (3,2,-1) (4,4,0)

#  0,4 has 4:  (1,2,-1)  (0,3,0)   (1,4,0)  (2,3,-1)
#  1,4 has 4:  (0,4,0)   (1,3,0)   (2,4,0)  (2,3,-1)
#  2,4 has 4:  (1,4,0)   (2,3,0)   (3,4,0)  (2,3,-1)
#  3,4 has 4:  (2,4,0)   (3,3,0)   (4,4,0)  (2,3,-1)
#  4,4 has 4:  (3,4,0)   (4,3,0)   (3,2,-1) (2,3,-1)


coords = (
#         W         N         E        S
    (
     ( (1,2,-1), (2,1,-1), (1,0,0), (0,1,0)),
     ( (0,0,0),  (2,1,-1), (2,0,0), (1,1,0)),
     ( (1,0,0),  (2,1,-1), (3,0,0), (2,1,0)),
     ( (2,0,0),  (2,1,-1), (4,0,0), (3,1,0)),
     ( (3,0,0),  (2,1,-1), (3,2,-1),(4,1,0)),
    ),
    (
     ( (1,2,-1), (0,0,0),  (1,1,0), (0,2,0)),
     ( (0,1,0),  (1,0,0),  (2,1,0), (1,2,0)),
     ( (1,1,0),  (2,0,0),  (3,1,0),          (0,0,1), (1,0,1), (2,0,1), (3,0,1), (4,0,1)),
     ( (2,1,0),  (3,0,0),  (4,1,0), (3,2,0)),
     ( (3,1,0),  (4,0,0),  (3,2,-1),(4,2,0))
    ),
    (
     ( (1,2,-1), (0,1,0),  (1,2,0), (0,3,0)),
     ( (0,2,0),  (1,1,0),           (1,3,0), (0,0,1), (0,1,1), (0,2,1), (0,3,1), (0,4,1)),
     ( (2,2,0), ),
     (           (3,1,0),  (4,2,0), (3,3,0), (4,0,1), (4,1,1), (4,2,1), (4,3,1), (4,4,1)), 
     ( (3,2,0),  (4,1,0),  (3,2,-1),(4,3,0)),
    ),
    (
     ( (1,2,-1), (0,2,0),  (1,3,0), (0,4,0)),
     ( (0,3,0),  (1,2,0),  (2,3,0), (1,4,0)),
     ( (1,3,0),            (3,3,0), (2,4,0), (0,4,1), (1,4,1), (2,4,1), (3,4,1), (4,4,1)),
     ( (2,3,0),  (3,2,0),  (4,3,0), (3,4,0)),
     ( (3,3,0),  (4,2,0),  (3,2,-1),(4,4,0)),
    ),
    (
     ( (1,2,-1), (0,3,0),  (1,4,0), (2,3,-1)),
     ( (0,4,0),  (1,3,0),  (2,4,0), (2,3,-1)),
     ( (1,4,0),  (2,3,0),  (3,4,0), (2,3,-1)),
     ( (2,4,0),  (3,3,0),  (4,4,0), (2,3,-1)),
     ( (3,4,0),  (4,3,0),  (3,2,-1),(2,3,-1)),
    )
)

def makegrids( depth ):
    grids = []
    for lvl in range(depth+1):
        grids.append( [[0]*5 for i in range(5)] )
    return grids

def onelevel(grid,lvl):
    depth = len(grid)
    new = [[0]*5 for i in range(5)]
    for y in range(5):
        for x in range(5):
            nbrs = sum( grid[lvl+zz][yy][xx] for xx,yy,zz in coords[y][x] if 0 <= lvl+zz < depth )
            if nbrs == 1 or (nbrs == 2 and not grid[lvl][y][x]):
                new[y][x] = 1
    return new

def doall(grid):
    return list( onelevel(grid,i) for i in range(len(grid)))

def fancyrow( depth, i, subgrids ):
    sumx = 0
    if DEBUG:
        print( '   '.join("%4d" % (i+ii-depth) for ii in range(len(subgrids)) ) )
    for y in range(5):
        s = ""
        for g in subgrids:
            s += '  '
            for x in range(5):
                s += ".#"[g[y][x]]
                sumx += g[y][x]
        if DEBUG:
            print( s )
    if DEBUG:
        print( )
    return sumx

def fancyprint(grid):
    depth = len(grid) // 2
    sumx = 0
    for i in range(0,len(grid),10):
        sumx += fancyrow( depth, i, grid[i:i+10] )
    return sumx


def part2( grid, depth ):
    grids = makegrids( depth )
    grids[depth//2] = grid
    for _ in range(depth):
        grids = doall(grids)
    return fancyprint(grids)

grid = makegrid(data)
if DEBUG:
    pprint( grid )
    print( rating( grid) )

print( "Part 1:", part1(grid))
print( "Part 2:", part2(grid,depth))


