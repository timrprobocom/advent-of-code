import os
import sys
import time
import collections
from pprint import pprint
from tools import Point

# Answer 8.
test1 = """\
#########
#b.A.@.a#
#########"""

# Answer 86.
test2 = """\
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

test3 = """\
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""

test4 = """\
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""

movements = ( Point(0,-1),Point(0,1),Point(-1,0),Point(1,0) )
lower = 'abcdefghijklmnopqrstuvwxyz'
upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Maze(object):
    def __init__(self,source):
        if not isinstance(source,str):
            source = open('day18.txt').read()
        maze = []
        for ln in source.splitlines():
            maze.append( list(ln.strip()) )
            i = ln.find('@')
            if i >= 0:
                self.adit = Point(i,len(maze)-1)
        self.maze = maze
        self.size = len(maze)

        self.steps = 0
        self.location = self.adit
        self.unlocked = []
        self.grabbed = []
        self.visited = set()

    def print(self):
        print( '\n'.join(''.join(ln) for ln in self.maze) )

    def findall( self, start ):
        upcoming = {start: []}
        possibles = []
        visited = set()
        found = {}
        steps = 0

        while upcoming:
            more = {}
            for cur,intheway in upcoming.items():
                ch = self[cur]
                if ch in lower and steps:
                    found[ch] = (cur, steps, intheway[:])
                if ch in upper:
                    intheway.append( ch )
                visited.add( cur )
                for facing in movements:
                    next = cur + facing
                    ch = self[next]
                    if next in visited or ch == '#':
                        continue
                    more[next] = intheway[:]
            upcoming = more
            steps += 1
        return found

    def commit( self, possible ):
        cur,steps = possible
        self.steps = steps
        self.grabbed.append( self[cur] )
        self.unlocked.append( self[cur].upper() )

    def __getitem__(self,pt):
        """ Allow indexing by a Point. """
        return self.maze[pt.y][pt.x]

    def erase(self, pt):
        self.maze[pt.y][pt.x] = '.'

    def state( self ):
        return (self.steps, self.unlocked[:], self.grabbed[:], self.visited.copy())

    def restore( self, state ):
        self.steps, self.unlocked, self.grabbed, self.visited = state

#maze = Maze(open('day18.txt'))
maze = Maze(test3)
maze.print()
print( maze.adit )
targets = maze.findall(maze.adit)
count = len(targets)

stats = { '@': targets }
for key,ptx in targets.items():
    tgt = maze.findall(ptx[0])
    stats[key] = tgt

# We no longer need the points.

print( count )

#  Stats key is char, value is (pt,steps,doors in the way)

def traverse( sitting ):
    minim = 99999999
    unchecked = [(sitting,0,sitting)]
    depth = 0
    while unchecked:
        more = []
        for sitting,steps,found in unchecked:
            if len(found) > depth:
                depth = len(found)
                print( "Now at depth", depth )
#            print( sitting, steps, found )
            if len(found) == count+1:
                if steps < minim:
                    print( "NEW MINIMUM", steps )
                    minim = steps
            for k,v in stats[sitting].items():
                if k in found:
                    continue
                _, dstep, doors = v
                if any( d.lower() not in found for d in doors ):
                    continue
                if steps+dstep < minim:
                    more.append( (k, steps+dstep, found+k) )
        unchecked = more
    return minim

def reachable(sitting, found):
    unchecked = collections.deque(sitting)
    while unchecked:
        xxx = unchecked.popleft()
        for k,v in stats[sitting].items():
            if k in found:
                continue
            if any( d.lower() not in found for d in doord ):
                continue
            # THis is stupid.




pprint( stats )
print( traverse( '@' ) )


sys.exit(0)


# So, at each step, find ALL the moves.
# If there is one, take it.
# If there are several, push state, try each one.
# If a complete path is already longer than the shortest, skip it.
