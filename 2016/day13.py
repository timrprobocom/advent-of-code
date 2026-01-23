import sys

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    MAGIC = 10
    SIZE = (10,10)
    TARGET = (7,4)
else:
    MAGIC = 1358
    SIZE = (45,45)
    TARGET = 31, 39

def parity(n):
    parity = 0
    while n:
        parity += n & 1
        n = n >> 1
    return parity

# returns 1 wall, 0 open

def isWall(x,y):
    p1 = x*x + 3*x + 2*x*y + y + y*y + MAGIC
    return parity(p1) & 1

def buildgrid(w,h):
    grid = []
    for row in range(h):
        gridrow = []
        for col in range(w):
            gridrow.append( '#' if isWall(col,row) else '.' )
        grid.append( gridrow )
    return grid

def rendergrid(grid):
    return '\n'.join( ''.join( k ) for k in grid )

#print buildgrid( 50, 50 )

# Now, how to traverse a maze?
# How can we tell we are in the weeds?
# 

directions = ( (-1,0), (0,-1), (1,0), (0,1) )


def traverse1( x, y, step ):
    if (x,y) == TARGET:
        if DEBUG:
            print( "REACHED TARGET at ", step )
        solutions.append( step )
        return True
    for dxy in directions:
        nx = x + dxy[0]
        ny = y + dxy[1]

        if nx == 0 or ny == 0 or nx >= SIZE[0] or ny >= SIZE[1]:
            continue
        if MAP[ny][nx] != '.':
            continue
        MAP[ny][nx] = 'O'
        traverse1( nx, ny, step+1 )
        MAP[ny][nx] = '.'

    return False


def traverse2( x, y, step ):
    solutions[(x,y)] = 1
    if step == 50:
        if DEBUG:
            print( rendergrid(MAP) )
        return True
    for dxy in directions:
        nx = x + dxy[0]
        ny = y + dxy[1]

        if nx < 0 or ny < 0 or nx >= SIZE[0] or ny >= SIZE[1]:
            continue
        if MAP[ny][nx] != '.':
            continue
        MAP[ny][nx] = 'O'
        traverse2( nx, ny, step+1 )
        MAP[ny][nx] = '.'

    return False
 
 
MAP = buildgrid(*SIZE)
if DEBUG:
    print( rendergrid(MAP) )

solutions = []
traverse1( 1, 1, 0 )
if DEBUG:
    print( solutions )
print( 'Part 1:', min(solutions) )

MAP[1][1] = 'O'
solutions = {}
traverse2( 1, 1, 0 )
if DEBUG:
    print( solutions )
print( 'Part 2:', len(solutions) )
