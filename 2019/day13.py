import sys
import time
import itertools
from intcode import Program
TRACE = 0


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
    for row in grid:
        print( ''.join(row) )

score = 0

def updatecell( pgm, grid, x, y, t ):
    if x == -1:
        global score
        score = t
        print( "Score: ", t )
    else:
        if t > 4:
            print(x,y,t)
        grid[y][x] = ' #x-o'[t]
        if t == 3 and pgm.xpaddle == 0:
#            print( "Paddle now at ", x )
            pgm.xpaddle = x
        if t == 4:
#            print( "Ball now at ", x )
            pgm.xball = x
            display(grid)


class Prog13( Program ):
    def __init__(self, program):
        Program.__init__(self,program)
        self.xball = 0
        self.xpaddle = 0

    def read_input(self):
        while not self.output.empty():
            time.sleep(0.05)
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
    pgm = Program(real)
    pgm.run()
    queue = list(take(pgm.dump(),3))
    w =  max(k[0] for k in queue)+1
    h =  max(k[1] for k in queue)+1
    print( w, h )

    grid = []
    for i in range(h):
        grid.append([' '] * w)
    
    for x,y,t in queue:
        grid[y][x] = ' #x-o'[t]

    display(grid)

    joy = 0
    real[0] = 2
    pgm = Prog13(real)
    pgm.start()
    while pgm.is_alive():
        x = pgm.pop()
        y = pgm.pop()
        t = pgm.pop()
        updatecell( pgm, grid, x, y, t )
    while not pgm.output.empty():
        x = pgm.pop()
        y = pgm.pop()
        t = pgm.pop()
        updatecell( pgm, grid, x, y, t )
    print( "Part 2:", score )  # 10776


#part1()
part2()
