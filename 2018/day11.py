import time
before = time.time()

live = 3613 #7672

# Grid is 300x300, based at 1
# Rack is X + 10
# Start power is rack times Y
# Add my input
# power *= rack
# Keep hundreds digit
# Subtract 5

def findPower(x,y,serial):
    rack = x+10
    power = (rack * y + serial) * rack
    return ord(str(power)[-3]) - 48 - 5


print( findPower(3,5,8),4 )
print( findPower(122,79,57),-5 )
print( findPower(217,196,39),0 )
print( findPower(101,153,71),4 )

grid = []
for y in range(300):
    print( y, end=' ')
    row = []
    for x in range(300):
        row.append( findPower( x+1, y+1, live ) )
    grid.append(row)

print()
print( len(grid), len(grid[0]) )

def convolve( grid, sq ):
    maxx = len(grid) - sq
    row = []
    for y in range(0,maxx):
        base = 0
        for cvy in range(sq):
            for cvx in range(sq):
                base += grid[y+cvy][cvx]
        row.append(base)
        for x in range(1,maxx):
            for cvy in range(sq):
                base = base - grid[y+cvy][x-1] + grid[y+cvy][x+sq-1]
            row.append(base)

    mr = max(row)
    ri = row.index(max(row))
    yy = ri // maxx + 1
    xx = ri % maxx + 1

    return mr, xx, yy

maxes = []

for square in range(99):
    c = convolve( grid, square )
    print( square, c )
    if c[0] < 0:
            break
    maxes.append( c )

print( max(maxes), maxes.index(max(maxes)) )
print( time.time() - before )
