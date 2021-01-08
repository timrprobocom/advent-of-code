import numpy as np


def xy0(s):
    x = s.split(',')
    return int(x[0]),int(x[1])

def xy1(s):
    x = s.split(',')
    return int(x[0])+1,int(x[1])+1

def setx(grid,tl,br,val):
    grid[tl[0]:br[0],tl[1]:br[1]] = val

def tog(grid,tl,br):
    grid[tl[0]:br[0],tl[1]:br[1]] = 1 - grid[tl[0]:br[0],tl[1]:br[1]]

def bump(grid,tl,br,val):
    grid[tl[0]:br[0],tl[1]:br[1]] = np.clip( grid[tl[0]:br[0],tl[1]:br[1]] + 2 * val - 1, 0, 999 )

def bump2(grid,tl,br):
    grid[tl[0]:br[0],tl[1]:br[1]] += 2

def process( setx, tog ):
    grid = np.zeros((1000,1000),dtype=np.int32)
    for ln in open('day06.txt'):
        words = ln.strip().split()
        if words[0] == 'toggle':
            tl = xy0(words[1])
            br = xy1(words[3])
            tog( grid, tl, br )
        elif words[1] == 'on':
            tl = xy0(words[2])
            br = xy1(words[4])
            setx( grid, tl, br, 1 )
        elif words[1] == 'off':
            tl = xy0(words[2])
            br = xy1(words[4])
            setx( grid, tl, br, 0 )

    return grid.sum()

print( "Part 1:", process( setx, tog ) )
print( "Part 2:", process( bump, bump2 ) )
