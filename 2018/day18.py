import sys

grid = []
for ln in sys.stdin:
    grid.append( list(ln.strip()) )

def printgrid( grid ):
    print "Grid:"
    for row in grid:
        print ''.join(row)

def neighbors( grid, x, y ):
    counts = { '.': 0, '#': 0, '|': 0 }
    for dy in (-1,0,1):
        if y+dy < 0 or y+dy >= len(grid):
            continue
        for dx in (-1,0,1):
            if not dy and not dx:
                continue
            if x+dx < 0 or x+dx >= len(grid[0]):
                continue
            counts[grid[y+dy][x+dx]] += 1
    return counts

def countall( grid ):
    counts = { '.': 0, '#': 0, '|': 0 }
    for row in grid:
        for here in row:
            counts[here] += 1
    return counts

def generate( grid ):
    out = []
    for y,row in enumerate(grid):
        orow = []
        for x,here in enumerate(row):
            cnt = neighbors( grid, x, y )
            if here == '.' and cnt['|'] >= 3:
                orow.append('|')
            elif here == '|' and cnt['#'] >= 3:
                orow.append('#')
            elif here == '#' and (cnt['#'] < 1 or cnt['|'] < 1):
                orow.append('.')
            else:
                orow.append(here)
        out.append(orow)
    return out

def target(k):
    return ((k-466) % 28) + 466

# Could you automate finding the cycle?

printgrid(grid)
remember = []
tgt = target(1000000000)
print tgt, target(496), target(524), target(552)
for i in range(600):
    grid = generate(grid)
#    printgrid(grid)
    cnts = countall(grid)
    data = cnts['|'],cnts['#'],cnts['|']*cnts['#']
    if i == 10-1: 
        print "Part 1:", i, cnts, cnts['|']*cnts['#']
    if i == tgt-1: 
        print "Part 2:", i, cnts, cnts['|']*cnts['#']
        break
#    if data in remember:
#        print i, cnts, cnts['|']*cnts['#']
#        print "FOUND", i, remember.index(data)
    remember.append( data )

# So the cycle is 28 starting at 466.

