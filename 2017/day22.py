import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

# row, col

class sets:
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

def printgrid(virus):
    grid = virus.grid
    xs = sorted(k[0] for k in grid.bad)
    ys = sorted(k[1] for k in grid.bad)
    xs0 = min(xs)
    xs9 = max(xs)
    ys0 = min(ys)
    ys9 = max(ys)
    for y in range(ys0,ys9+1):
        for x in range(xs0,xs9+1):
            if (x,y) in grid.bad:
                print('# ',end='')
            elif (x,y) in grid.weak:
                print('W ',end='')
            elif (x,y) in grid.flag:
                print('F ',end='')
            else:
                print('. ',end='')
        print()

class virus:
    def __init__(self,rows,cols,grid):
        self.posn = (rows//2,cols//2)
        self.grid = grid
        self.direc = (-1,0)
        self.infected = 0

    def cycle( self ):
        posn = self.posn
        grid = self.grid
        if posn in grid.bad:
            # infected - turn right
            self.direc = (self.direc[1], -self.direc[0])
            grid.bad.remove(self.posn)
        else:
            # turn left
            self.direc = (-self.direc[1], self.direc[0])
            self.infected += 1
            grid.bad.add(self.posn)
        self.posn = (posn[0]+self.direc[0], posn[1]+self.direc[1] )

    def cycle2( self ):
        posn = self.posn
        grid = self.grid
        if posn in grid.weak:
            grid.weak.remove(posn)
            grid.bad.add(posn)
            self.infected += 1
        elif posn in grid.bad:
            # infected - turn right
            self.direc = (self.direc[1], -self.direc[0])
            grid.bad.remove(posn)
            grid.flag.add(posn)
        elif posn in grid.flag:
            # flagged - reverse
            self.direc = (-self.direc[0],-self.direc[1])
            grid.flag.remove(posn)
        else:
            # clean - turn left
            self.direc = (-self.direc[1], self.direc[0])
            grid.weak.add(posn)

        self.posn = (posn[0]+self.direc[0], posn[1]+self.direc[1] )

def part1(maker):
    grid = virus( *maker() )
    for i in range(10000):
        grid.cycle()
    return grid.infected

def part2(maker):
    grid = virus( *maker() )
    for i in range(10000000):
        grid.cycle2()
    return grid.infected

maker = makeTest if TEST else makeLive
print('Part 1:', part1(maker))
print('Part 2:', part2(maker))
