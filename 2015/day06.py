


def xy(s):
    return tuple( int(i) for i in s.split(',') )

def set(grid,tl,br,val):
    for y in range(tl[1],br[1]+1):
        for x in range(tl[0],br[0]+1):
            grid[y][x] = val

def tog(grid,tl,br):
    for y in range(tl[1],br[1]+1):
        for x in range(tl[0],br[0]+1):
            grid[y][x] = 1 - grid[y][x]

def bump(grid,tl,br,val):
    delta = 2 * val - 1
    for y in range(tl[1],br[1]+1):
        for x in range(tl[0],br[0]+1):
            grid[y][x] = max( 0, grid[y][x]+delta )

def bump2(grid,tl,br):
    for y in range(tl[1],br[1]+1):
        for x in range(tl[0],br[0]+1):
            grid[y][x] += 2

def process( set, tog ):
    grid = []
    for i in range(1000):
        grid.append( [0]*1000 )
    for ln in open('day06.txt'):
        words = ln.strip().split()
        if words[0] == 'toggle':
            tl = xy(words[1])
            br = xy(words[3])
            tog( grid, tl, br )
        elif words[1] == 'on':
            tl = xy(words[2])
            br = xy(words[4])
            set( grid, tl, br, 1 )
        elif words[1] == 'off':
            tl = xy(words[2])
            br = xy(words[4])
            set( grid, tl, br, 0 )

    return sum( sum(row) for row in grid )

print( "Part 1:", process( set, tog ) )
print( "Part 1:", process( bump, bump2 ) )
