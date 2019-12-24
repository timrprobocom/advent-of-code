import sys
import itertools

real="""\
...#.
#.##.
#..##
#.###
##..."""

test = """\
....#
#..#.
#..##
..#..
#...."""

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
#grid = inp.splitlines()

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
    (
     (  (1,2,-1), (2,1,-1), (1,0,0), (0,1,0)),
     (  (0,0,0),  (2,1,-1), (2,0,0), (1,1,0)),
     (  (1,0,0),  (2,1,-1), (3,0,0), (2,1,0)),
     (  (2,0,0),  (2,1,-1), (4,0,0), (3,1,0)),
     (  (3,0,0),  (2,1,-1), (3,2,-1),(4,1,0)),
    ),
    (
     (  (1,2,-1), (0,0,0),  (1,1,0), (0,2,0)),
     (  (0,1,0),  (1,0,0),  (2,1,0), (1,2,0)),
     (  (1,1,0),  (2,0,0),  (3,1,0),          (0,0,1), (1,0,1), (2,0,1), (3,0,1), (4,0,1)),
     (  (2,1,0),  (3,0,0),  (4,1,0), (3,2,0)),
     (  (3,1,0),  (4,0,0),  (3,2,-1),(4,2,0))
    ),
    (
     (  (1,2,-1), (0,1,0),  (1,2,0), (0,3,0)),
     (  (0,2,0),  (1,1,0),           (1,3,0), (0,0,1), (0,1,1), (0,2,1), (0,3,1), (0,4,1)),
     (  (2,2,0),  (2,2,0)),
     (            (3,1,0),  (4,2,0), (3,3,0), (4,0,1), (4,1,1), (4,2,1), (4,3,1), (4,4,1)), 
     (  (3,2,0),  (4,1,0),  (3,2,-1),(4,3,0)),
    ),
    (
     (  (1,2,-1), (0,2,0),  (1,3,0), (0,4,0)),
     (  (0,3,0),  (1,2,0),  (2,3,0), (1,4,0)),
     (  (1,3,0),            (3,3,0), (2,4,0), (0,4,1), (1,4,1), (2,4,1), (3,4,1), (4,4,1)),
     (  (2,3,0),  (3,2,0),  (4,3,0), (3,4,0)),
     (  (3,3,0),  (4,2,0),  (3,2,-1),(4,4,0)),
    ),
    (
     (  (1,2,-1), (0,3,0),  (1,4,0), (2,3,-1)),
     (  (0,4,0),  (1,3,0),  (2,4,0), (2,3,-1)),
     (  (1,4,0),  (2,3,0),  (3,4,0), (2,3,-1)),
     (  (2,4,0),  (3,3,0),  (4,4,0), (2,3,-1)),
     (  (3,4,0),  (4,3,0),  (3,2,-1),(2,3,-1)),
    )
)


def makegrids( depth ):
    grid = []
    for i in range(depth+1):
        grid.append( ["....."]*5 )
    return grid


def onelevel(grid,lvl):
    depth = len(grid)
    new = []
    for y in range(5):
        row = []
        for x in range(5):
            ch = grid[lvl][y][x]
            nbrs = sum( 1 for xx,yy,zz in coords[y][x] if 0 <= lvl+zz < depth and grid[lvl+zz][yy][xx] == '#' )
            if nbrs == 1 or (nbrs == 2 and ch == '.'):
                row.append('#')
            else:
                row.append('.')
        new.append(''.join(row))
    return new

def doall(grid):
    new = []
    for i in range(len(grid)):
        new.append( onelevel(grid,i) )
    return new

def printgrid(grid):
    depth = len(grid) // 2
    sumx = 0
    for i,sub in enumerate(grid):
        print( "Level", i-depth )
        print( '\n'.join(sub) )
        sumx += sum( s.count('#') for s in sub)
    print( sumx )
    return sumx

def fancyrow( depth, i, subgrids ):
    sumx = 0
    print( '   '.join("%4d" % (i+ii-depth) for ii in range(len(subgrids)) ) )
    for y in range(5):
        s = '  '.join(g[y] for g in subgrids)
        sumx += s.count('#')
        print( s )
    print( )
    return sumx

def fancyprint(grid):
    depth = len(grid) // 2
    sumx = 0
    for i in range(0,len(grid),10):
        if i+10 < len(grid):
            sumx += fancyrow( depth, i, grid[i:i+10] )
        else:
            sumx += fancyrow( depth, i, grid[i:] )
    return sumx


def doit( inp, depth ):
    grids = makegrids( depth )
    grids[depth//2] = inp.splitlines()
    for i in range(depth):
        grids = doall(grids)
    return fancyprint(grids)

if 'test' in sys.argv:
    print( doit( test, 10 ) )
else:
    print( "Part 2:", doit( real, 200 ) )


