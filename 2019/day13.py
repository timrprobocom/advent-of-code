import sys
import time
import itertools
from intcode import Program

TRACE = 'trace' in sys.argv
SLOW = 'slow' in sys.argv


def run( base, blacks, whites ):
    pgm = Program(real)
    loc = base
    facing = 0
    pgm.start()

    while pgm.is_alive():
        pgm.push( 1 if loc in whites else 0 )
        color = pgm.pop()
        newdir = pgm.pop()
        if TRACE:
            print( color, newdir )
        if color:
            whites.add( loc )
            blacks.discard( loc )
        else:
            blacks.add( loc )
            whites.discard( loc )
        facing = (facing+[1,3][newdir]) % 4
        loc += directions[facing]
        if TRACE:
            print( loc )
    pgm.join()

def take(data,n):
    return zip(*[iter(data)]*n)

def part1():
    real = list(eval(open('day13.txt').read()))
    pgm = Program(real)
    pgm.run()
    queue = pgm.dump()
    print( len(queue) )
    twos = [1 for k in take(queue,3) if k[2] == 2]
    print( len(twos) ) # 228


def display(grid):
    print()
    print( '\n'.join(''.join(row) for row in grid) )
    if SLOW:
        time.sleep( 0.05 )

class Prog13( Program ):
    def __init__(self, program):
        Program.__init__(self,program)
        self.xball = 0
        self.xpaddle = 0
        self.score = 0

    def updatecell( self, x, y, t ):
        if x == -1:
            self.score = t
            print( "Score: ", t )
        else:
            if t > 4:
                print(x,y,t)
            self.grid[y][x] = ' #x-o'[t]
            if t == 3 and self.xpaddle == 0:
#            print( "Paddle now at ", x )
                self.xpaddle = x
            if t == 4:
#            print( "Ball now at ", x )
                self.xball = x
                display(self.grid)

    def clear_queue( self ):
        while not self.output.empty():
            x = self.pop()
            y = self.pop()
            t = self.pop()
            self.updatecell( x, y, t )

    def read_input(self):
        self.clear_queue()

#        print( f"Ball {self.xball}, paddle {self.xpaddle}" )
        if not self.xball or not self.xpaddle:
#            print( "Joy: 0" )
            return 0
        if self.xball < self.xpaddle: 
#            print( "Joy: -1" )
            self.xpaddle -= 1
            return -1
        if self.xball > self.xpaddle: 
#            print( "Joy: 1" )
            self.xpaddle += 1
            return 1
        print( "Joy: 0" )
        return 0

def part2():
    real = list(eval(open('day13.txt').read()))

    # Make one run to determine the limits of the grid.

    pgm = Program(real)
    pgm.run()
    queue = list(take(pgm.dump(),3))
    w =  max(k[0] for k in queue)+1
    h =  max(k[1] for k in queue)+1
    print( w, h )

    # Create the printable grid.

    grid = []
    for i in range(h):
        grid.append([' '] * w)

    # Populate it from the part 1 output.
    
    for x,y,t in queue:
        grid[y][x] = ' #x-o'[t]

    display(grid)

    # Insert a quarter.

    real[0] = 2
    
    # Go run the app.

    pgm = Prog13(real)
    pgm.grid = grid
    pgm.run()

    # Pop any unfinished output.

    pgm.clear_queue()

    display(grid)

    print( "Part 2:", pgm.score )  # 10776

part1()
part2()
