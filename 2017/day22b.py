
# row, col

class sets(object):
    pass

def makeTest():
    grid = sets()
    grid.bad = set(((0,2),(1,0)))
    grid.weak = set()
    grid.flag = set()
    return 3,3,grid

def makeLive():
    bad = set()
    for lno,ln in enumerate(open('day22.txt').readlines()):
        for cno,ch in enumerate(ln):
            if ch=='#':
                bad.add((lno,cno))
    grid = sets()
    grid.bad = bad
    grid.weak = set()
    grid.flag = set()
    return lno+1,cno,grid


#   -1,0
# 0,-1   0,1
#    1,0


class virus(object):
    def __init__(self,rows,cols,grid):
        print rows, cols
        self.posn = (rows/2,cols/2)
        self.grid = grid
        self.direc = (-1,0)
        self.infected = 0

    def cycle( self ):
        posn = self.posn
        grid = self.grid
        if posn in grid.weak:
            grid.weak.remove(posn)
            grid.bad.add(posn)
            self.infected += 1
        elif posn in grid.bad:
            # infected - turn right
            if self.direc[0]:
                self.direc = (0,-self.direc[0])
            else:
                self.direc = (self.direc[1],0)
            grid.bad.remove(posn)
            grid.flag.add(posn)
        elif posn in grid.flag:
            self.direc = (-self.direc[0],-self.direc[1])
            grid.flag.remove(posn)
        else:
            if self.direc[0]:
                self.direc = (0,self.direc[0])
            else:
                self.direc = (-self.direc[1],0)
            grid.weak.add(posn)

        self.posn = (posn[0]+self.direc[0], posn[1]+self.direc[1] )

grid = virus( *makeTest() )

for i in range(10000000):
    grid.cycle()
print grid.infected
