import sys

def parity(n):
    parity = 0
    while n:
        if n & 1:
            parity += 1
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

solutions = {}

def traverse( x, y, step ):
    solutions[(x,y)] = 1
    if step == 50:
        print
        print rendergrid(MAP)
        return True
    for dxy in directions:
        nx = x + dxy[0]
        ny = y + dxy[1]

        if nx < 0 or ny < 0 or nx >= SIZE[0] or ny >= SIZE[1]:
            continue
        if MAP[ny][nx] != '.':
            continue
        MAP[ny][nx] = 'O'
        traverse( nx, ny, step+1 )
        MAP[ny][nx] = '.'

    return False
 
#MAGIC = 10
#SIZE = (10,10)
#TARGET = (7,4)

MAGIC = 1358
SIZE = (45,45)
TARGET = 31, 39
MAP = buildgrid(*SIZE)
print rendergrid(MAP)

MAP[1][1] = 'O'
print traverse( 1, 1, 0 )
print solutions
print len(solutions)
