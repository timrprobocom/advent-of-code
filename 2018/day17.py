#
# Think I need to build a grid.
#

import re
import sys

# Parse the input.

expr = r"([xy])=(\d*), ([xy])=(\d*)\.\.(\d*)"
def findextrema( f ):
    tuples = []
    xmin, xmax, ymin, ymax = 9999, 0, 9999, 0
    for ln in f:
        parts = re.match( expr, ln )
        g = parts.groups()
        n1 = int(g[1])
        n2 = int(g[3])
        n3 = int(g[4])
        tuples.append( (g[0],n1,g[2],n2,n3) )
        if g[0] == 'x':
            if n1 < xmin:
                xmin = n1
            if n1 > xmax:
                xmax = n1
            if n2 < ymin:
                ymin = n2
            if n3 > ymax:
                ymax = n3
    return tuples,(xmin,xmax,ymin,ymax)

def makegrid( tuples, sides ):
    grid = []
    xmin,_,ymin,_ = sides
    for y in range(0,sides[3]+1):
        grid.append( ['.']*(sides[1]+3) )
    for axis,n1,_,n2,n3 in tuples:
        if axis == 'x':
            for y in range(n2,n3+1):
                grid[y][n1] = '#'
        else:
            for x in range(n2,n3+1):
                grid[n1][x] = '#'
    return grid

def printgrid( grid, sides ):
    print "Grid:"
    for row in grid:
#        print ''.join(row[sides[0]:sides[0]+80])
#        print ''.join(row[450:])
        print ''.join(row[sides[0]:])

# Go down until we hit a # or ~
# Back up 1, probe to left and right until we hit # or .
# If #, stop trace
# If . , mark it | and it becomes a new drop point.

def flood( grid, x0, y ):
    print "Flooding at", x0, y
    pour = []
    x = x0
    grid[y][x] = '~'
    while 1:
        x -= 1
        if grid[y][x] in '#~|':
            break
        if grid[y][x] == '.':
            if grid[y+1][x] == '.':
                print "New pour point", x, y+1
                pour.append( (x,y) )
                break
            else:
                grid[y][x] = '~'

    x = x0
    while 1:
        x += 1
        if grid[y][x] in '#~':
            break
        if grid[y][x] == '.':
            if grid[y+1][x] == '.':
                print "New pour point", x, y+1
                pour.append( (x,y) )
                break
            else:
                grid[y][x] = '~'
    return pour

def done( grid, x0, y ):
    # Spreading out both ways, if we hit . before #, then go on.
    x = x0
    # Check left.
    while 1:
        x -= 1
        if grid[y][x] == '.':
            return True
        if grid[y][x] == '#':
            break
    x = x0
    while 1:
        x += 1
        if grid[y][x] == '.':
            return True
        if grid[y][x] == '#':
            break
    return False





# Recursive?

def fill( grid, sides, pour ):
    xmin,xmax,ymin,ymax = sides
    x,y = pour
    print "filling", pour

    # Descend until # or off the bottom.

    while 1:
        print "checking", x, y
        if y > ymax:
#            print "hit bottom", pour
            return
        if grid[y][x] in '|~':
#            print "hit water", pour
            if done(grid,x,y):
                return
            else:
                break
        if grid[y][x] == '#':
#            print "hit container", pour
            break
        grid[y][x] = '|'
        y += 1

#    print "back out"
    while y >= pour[1]:
        y -= 1
        newpours = flood( grid, x, y )
        if newpours:
            print "new pours", newpours
            for p in newpours:
                fill( grid, sides, p )
        if done(grid,x,y):
            break
    print "Done with", pour
#    printgrid(grid,sides)


tuples,sides = findextrema(sys.stdin)
grid = makegrid(tuples, sides)
printgrid( grid, sides )
print sides
fill( grid, sides, (500,0) )
printgrid( grid, sides )

filled = 0
for row in grid[sides[2]:]:
    for c in row:
        if c in '~|':
            filled += 1
print sides
print filled

# Part 2
# Remove |
# Replace .~ by ..

newgrid = []
for row in grid:
    row = ''.join(row).replace('|','.')
    for m in re.finditer( r"\.~+", row ):
        i,j = m.span()
        row = row[:i] + ('.'*(j-i)) + row[j:]
    for m in re.finditer( r"~+\.", row ):
        i,j = m.span()
        row = row[:i] + ('.'*(j-i)) + row[j:]
    newgrid.append( list(row) )
        
printgrid(newgrid,sides)

filled = 0
for row in newgrid[sides[2]:]:
    for c in row:
        if c in '~|':
            filled += 1
print filled
