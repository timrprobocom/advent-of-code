import sys
from intcode import Program
from tools import Point


class Maze(object):
    """ Absorbs the output from intcode and turns it into a stringable maze. """
    def __init__( self, dump ):
        self.ints = dump
        self.string = ''.join(chr(i) for i in dump)
        self.maze = self.string.strip().splitlines()
        self.size = len(self.maze)

    def __getitem__(self,pt):
        """ Allow indexing by a Point. """
        if pt.x < 0 or pt.x >= self.size or pt.y < 0 or pt.y >= self.size:
            return '.'
        return self.maze[pt.y][pt.x]


TRACE = 'trace' in sys.argv

# Run the program once to get the path.

real = list(eval(open('day17.txt').read()))

pgm = Program(real)
pgm.run()
maze = Maze( pgm.dump() )
print(maze.string)

def part1():
    # Find the robot.

    robot = Point(maze.maze[-1].find('^'), len(maze.maze)-1)
    lastturn = robot

    # Robot starts facing north.

    facing = Point(0,-1) 

    crossings = set()
    turns = []
    while 1:
        #  If we are facing empty space, turn.
        if maze[robot+facing] == '.':
            if robot != lastturn:
                turns.append( robot.dist(lastturn) )
            if maze[robot+facing.left()] == '#':
                facing = facing.left()
                turns.append( "L" )
            elif maze[robot+facing.right()] == '#':
                facing = facing.right()
                turns.append( "R" )
            else:
                # End of the scaffold.
                break
            lastturn = robot
            robot += facing

        # Otherwise, look for a crossing.
        else:
            if maze[robot+facing.left()] == '#' and maze[robot+facing.right()] == '#':
                crossings.add( robot )
            robot += facing

        if TRACE:
            print( robot )
    # We return the set of crossings and the record of turns.
    return crossings, turns

def part2():
    pgm = Program(real)
    pgm.pgm[0] = 2
    instructions = (
        "A,B,A,C,C,A,B,C,B,B\n",
        "L,8,R,10,L,8,R,8\n",
        "L,12,R,8,R,8\n",
        "L,8,R,6,R,6,R,10,L,8\n",
        "n\n"
    )
    for c in ''.join(instructions):
        pgm.push(ord(c))
    pgm.run()
    d = pgm.dump()
    if TRACE:
        print( Maze(d[:-1]).string )
    return d[-1]

crossings, turns = part1()

# Dump this to see the sequence of moves we took.
print( ','.join( str(x) for x in turns) )
print( )

print( "Part 1:", sum( pt.x*pt.y for pt in crossings ) )
print( "Part 2:", part2() )
