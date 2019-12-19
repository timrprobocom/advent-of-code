import os
import sys
import time
import itertools
import collections
from pprint import pprint
from tools import Point

TRACE = False

# Answer 8.
test = ("""\
#########
#b.A.@.a#
#########""",

# Answer 86.
"""\
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################""",

"""\
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""",

"""\
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""",

# Part 2, answer 72.
"""\
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############"""
)

movements = ( Point(0,-1),Point(0,1),Point(-1,0),Point(1,0) )
lower = 'abcdefghijklmnopqrstuvwxyz'
upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Maze(object):
    def __init__(self,source):
        if not isinstance(source,str):
            source = source.read()
        maze = []
        self.adit = []
        for ln in source.splitlines():
            maze.append( list(ln.strip()) )
            for i,ch in enumerate(ln):
                if ch == '@':
                    self.adit.append( Point(i,len(maze)-1 ))
        self.maze = maze
        self.size = len(maze)

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

    def __getitem__(self,pt):
        """ Allow indexing by a Point. """
        return self.maze[pt.y][pt.x]

for arg in sys.argv[1:]:
    if arg == 'trace':
        TRACE = True
    elif arg in '123456789':
        maze = Maze(test[int(arg)-1])
    elif arg[-4:] == '.txt':
        maze = Maze(open(arg))

maze.print()
print( maze.adit )

# Find all of the targets.

#stats = {'@': {}}
stats = {}
for i,adit in enumerate(maze.adit):
    ch = str(i)
#    stats['@'][ch] = (adit, 0, [] )
    stats[ch] = maze.findall( adit )
print( sum(len(v) for v in stats.values() ))

# Find the distance betweeen targets.

for v in list(stats.values()):
    for key,ptx in v.items():
        if key >= 'a':
            stats[key] = maze.findall(ptx[0])

# Stats key is char, value is (pt,steps,doors in the way)
#
# We need to do a depth-first search to weed out duplicates.

def sub(s,i,c):
    return s[0:i]+c+s[i+1:]

seen = {}
def search( sitting, found ):
#    print( "New search", sitting, found )
    f = ''.join(sorted(list(found)))
    if sitting+f in seen:
        return seen[sitting+f]
    paths = []
    for si,s in enumerate(sitting):
        for k,v in stats[s].items():
            if k in found:
                continue
            _, dstep, doors = v
            if any( d.lower() not in found for d in doors ):
                continue
            paths.append( dstep + search(sub(sitting,si,k), f+k) )
    ans = min(paths) if paths else 0
#    print( sitting+f, ans )
    seen[sitting+f] = ans
    return ans

pprint( stats )
if len(maze.adit) == 1:
    print( "Part 1:", search( '0', '@' ) )
else:
    print( "Part 2:", search( '0123', '@' ) )