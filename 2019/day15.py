import sys
import random
from collections import defaultdict
from tools import Point

DEBUG = 'debug' in sys.argv
IMAGE = 'IMAGE' in sys.argv

live = [int(k) for k in open("day15.txt").read().split(',')]

from intcode import Program

# Inputs:
#   1
# 3   4
#   2
#
# Responses:
#   0 = wall ahead
#   1 = moved
#   2 = found home

# start position

# so, at every position:
# Try 1, 2, 3, 4


movement = ( Point(0,0), Point(0,-1),Point(0,1),Point(-1,0),Point(1,0) )
nextleft  = ( 0, 3, 4, 2, 1 )
nextright = ( 0, 4, 3, 1, 2 )
opposite  = ( 0, 2, 1, 4, 3 )

def add(a,b):
    return (a[0]+b[0],a[1]+b[1])

class Prog15( Program ):
    def __init__(self, program):
        Program.__init__(self,program)
        self.position = Point(0,0)
        self.dir = 1
        self.push( self.dir )
        self.walls = set()
        self.target = None
        self.count = 0

    def printmap(self):
        if not IMAGE:
            return
        if not self.walls:
            return

        # Estblish the bounds.

        xmin = min(min(t.x  for t in self.walls),self.position.x)
        xmax = max(max(t.x  for t in self.walls),self.position.x) + 1
        ymin = min(min(t.y  for t in self.walls),self.position.y)
        ymax = max(max(t.y  for t in self.walls),self.position.y) + 1

        # Create empty grid

        grid = []
        for i in range(ymin,ymax):
            grid.append( [' ']*(xmax-xmin))

        # Fill in the walls.

        for w in self.walls:
            grid[w.y-ymin][w.x-xmin] = '#'

        # Fill in the base, the droid, and the oxygen.

        grid[-ymin][-xmin] = '@'
        grid[self.position.y-ymin][self.position.x-xmin] = 'D'
        if self.target:
            grid[self.target.y-ymin][self.target.x-ymin] = '$'
        print( '\n'.join(''.join(row) for row in grid) )

    # We follow the left-hand rule.

    def read_input(self):
        if not self.input.empty():
            return self.input.get()

        self.count += 1
        if IMAGE:
            print( "\nIteration", self.count )
            self.printmap()

        # We're done when return to base (after leaving base).

        if self.count > 4 and self.position == Point(0,0):
            return 5

        # This is the cell we are facing.

        facing = self.position + movement[self.dir]

        # Get the next result.  If 0, mark a wall, and turn right.
        # Otherwise, turn left.

        code = self.pop()
        if code == 0:
            self.walls.add( facing )
            self.dir = nextright[self.dir]
        else:
            self.position = facing
            self.dir = nextleft[self.dir]
            if code == 2:
                self.target = facing

        return self.dir

# Run the program to produce the maze.

pgm = Prog15( live )
pgm.run()
if DEBUG:
    print( pgm.walls, file=open('maze.txt','w') )
    print( "Target", pgm.target )

# Now, given the maze, we can do a breadth-first search for the oxygen.

# We track a visited list.  From each point, add all the points we can visit
# that haven't been visited.  When we reach the oxygen, we win.

def process( start, target = None ):
    visited = set()
    upcoming = set([start])
    step = -1

    while upcoming:
        step += 1
        more = set()
        for cur in upcoming:
            if target and cur == target:
                return step
            visited.add( cur )
            for dir in (1,2,3,4):
                facing = cur + movement[dir]
                if not facing in pgm.walls and not facing in visited:
                    more.add( facing )
        upcoming = more

    # This comes out one step too large because we count the final
    # step that actually produces nothing.

    return step

print( "Part 1:", process(Point(0,0), pgm.target) )
print( "Part 2:", process(pgm.target) )
