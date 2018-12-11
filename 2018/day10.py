import re

test = 'day10test.txt'
live = 'day10.txt'

# Parse

#         i123456           j123456
#position=< 9,  1> velocity=< 0,  2>

class Point(object):
    def __init__(self,xx,yy,dx,dy):
        self.xx = xx
        self.yy = yy
        self.dx = dx
        self.dy = dy
    def advance(self):
        self.xx += self.dx
        self.yy += self.dy

match = r'< *([0-9-]*), *([0-9-]*)>.*< *([0-9-]*), *([0-9-]*)>'

def parse(ln):
    res = re.search(match,ln)
    xx,yy,dx,dy = list(int(x) for x in res.groups())
    return Point(xx,yy,dx,dy)


def makegrid( w, h ):
    gridline = ['.'] * w
    grid = []
    for i in range(h):
        grid.append( gridline[:] )
    return grid

def printgrid( points ):
    # Find min, max
    minx = 99999
    maxx = -99999
    miny = 99999
    maxy = -99999
    
    for pt in points:
        if pt.xx > maxx: maxx = pt.xx
        if pt.xx < minx: minx = pt.xx
        if pt.yy > maxy: maxy = pt.yy
        if pt.yy < miny: miny = pt.yy
        
    if maxx-minx > 100:
        pass #print "too large in X"
    elif maxy-miny > 500:
        pass #print "too large in y"
    else:
        grid = makegrid( maxx-minx+1, maxy-miny+1 )
        fillgrid( grid, points, minx, miny )
    
        print minx, maxx, miny, maxy
        for ln in grid:
            print ''.join(ln)
        print

def fillgrid( grid, points, offx, offy):
    for p in points:
        grid[p.yy-offy][p.xx-offx] = '*'

def advance( points ):
    for p in points:
        p.advance()

#points = list( parse(ln) for ln in open(test) )
points = list( parse(ln) for ln in open(live) )
for i in range(100000):
    print i, 
    printgrid( points )
    advance( points )
