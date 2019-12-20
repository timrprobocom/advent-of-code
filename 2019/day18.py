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

# Answer 136.
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

# Answer 81.
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
                if ch.islower() and steps:
                    found[ch] = (cur, steps, intheway[:])
                if ch.isupper():
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

# Stats key is char, value is (pt,steps,doors in the way)
#
# We need to do a depth-first search to weed out duplicates.

def sub(s,i,c):
    return s[0:i]+c+s[i+1:]

def ssort(s):
    return ''.join(sorted(list(s)))

def bfs( start, found ):
    unchecked = {(start,found): 0 }
    result = 0

    # Keep going as long as there are paths we haven't tested.
    # Because this is "breadth-first", each time through this loop
    # processed all of the paths of a single length.  The next pass
    # will be one step longer.
    while unchecked:
        if TRACE:
            print('Depth',len(next(iter(unchecked.keys()))[1]))
        more = {}
        paths = []

        # For each path that needs to be checked:
        for (sitting, found), steps in unchecked.items():
            paths.append( steps )
            # For each robot:
            for si,s in enumerate(sitting):
                # For each key this robot can see:
                for k,v in stats[s].items():
                    # If we've already picked it up, ignore.
                    if k in found or k < 'a':
                        continue
                    # If any intervening doors are locked, ignore.
                    _, dstep, doors = v
                    if any( d.lower() not in found for d in doors ):
                        continue
                    # If this new path has alread been enumerated, and
                    # this path to the same state is shorter, keep it.
                    newsit = (sub(sitting,si,k),ssort(found+K))
                    if newsit in more and more[newsit] <= steps+dstep:
                        continue
                    more[newsit] = steps+dstep
        # When we have nothing new, we have our answer.
        if not more:
            return min(paths)
        unchecked = more
    return None


def search( sitting, found ):
    if TRACE:
        print( "New search", sitting, found )
    found = ssort(found)

    # If we've been in this situation before, we don't need to go again.
    if sitting+found in search.seen:
        return search.seen[sitting+found]

    paths = []

    # For each robot:
    for si,s in enumerate(sitting):
        # For each key the robot can see:
        for k,v in stats[s].items():
            # If we've already picked it up, ignore.
            if k in found:
                continue
            _, dstep, doors = v
            # If there's a door in the way without a key, ignore.
            if any( d.lower() not in found for d in doors ):
                continue
            # Go explore this path.
            paths.append( dstep + search(sub(sitting,si,k), found+k) )
    ans = min(paths) if paths else 0
    if TRACE:
        print( sitting+found, ans )
    search.seen[sitting+found] = ans
    return ans

search.seen = {}

for arg in sys.argv[1:]:
    if arg == 'trace':
        TRACE = True
    elif arg == 'bfs':
        search = bfs
    elif arg.isdigit():
        maze = Maze(test[int(arg)-1])
    elif arg[-4:] == '.txt':
        maze = Maze(open(arg))

maze.print()
print( maze.adit )

# Find all of the targets.

stats = {}
for i,adit in enumerate(maze.adit):
    stats[str(i)] = maze.findall( adit )

print( sum(len(v) for v in stats.values() ))

# Find the distance betweeen targets.

for v in list(stats.values()):
    for key,ptx in v.items():
        if key >= 'a':
            stats[key] = maze.findall(ptx[0])

if TRACE:
    pprint( stats )

begin = time.time()
if len(maze.adit) == 1:
    print( "Part 1:", search( '0', '@' ) )
else:
    print( "Part 2:", search( '0123', '@' ) )
delta = time.time() - begin
print( "Elapsed:", delta )
