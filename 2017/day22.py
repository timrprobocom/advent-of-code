
# row, col

def makeTest():
    test = set()
    test.add((0,2))
    test.add((1,0))
    return 3,3,test

def makeLive():
    s = set()
    for lno,ln in enumerate(open('day22.txt').readlines()):
        for cno,ch in enumerate(ln):
            if ch=='#':
                s.add((lno,cno))
    return lno+1,cno,s


#   -1,0
# 0,-1   0,1
#    1,0


class virus(object):
    def __init__(self,rows,cols,grid):
        self.posn = (rows/2,cols/2)
        self.grid = grid
        self.direc = (-1,0)
        self.infected = 0

    def cycle( self ):
        if self.posn in self.grid:
            # infected - turn right
            if self.direc[0]:
                self.direc = (0,-self.direc[0])
            else:
                self.direc = (self.direc[1],0)
            self.grid.remove(self.posn)
        else:
            # turn left
            if self.direc[0]:
                self.direc = (0,self.direc[0])
            else:
                self.direc = (-self.direc[1],0)
            self.infected += 1
            self.grid.add(self.posn)
        self.posn = (self.posn[0]+self.direc[0], self.posn[1]+self.direc[1] )

rows,cols,bad = makeLive()
print rows, cols
grid = virus( rows, cols, bad )

for i in range(10000):
    grid.cycle()
print grid.infected
