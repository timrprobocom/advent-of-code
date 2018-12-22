from __future__ import print_function
import sys
from collections import defaultdict

# So this is making a graph out of the map, not the regex!
# He is using complex numbers to store the coordinates.
# My map is only 100x100.

def printgraph(maze):
    n = int(min(c.imag for c in maze))
    s = int(max(c.real for c in maze))
    w = int(min(c.imag for c in maze))
    e = int(max(c.real for c in maze))
    wid = e-w+1
    hgt = s-n+1

    basewall = ['#','#'] * wid + ['#']
    baseroom = ['#','.'] * wid + ['#']
    for y in range(hgt):
        wall = basewall[:]
        room = baseroom[:]
        for x in range(wid):
            me = (x+w)+(y+n)*1j
            nn = me - 1j
            ww = me - 1
            if nn in maze[me]:
                wall[x+x+1] = "-"
            if ww in maze[me]:
                room[x+x] = "|"
        print( ''.join(wall) ) 
        print( ''.join(room) )
            
    print(''.join(basewall))

# So, here's the magic.  Rather than build all of the possible strings
# up to this point, pos simply holds the list of coordinates we might be
# at, based on all the alternatives to this point.  When we get an 
# alternative, we start again with the list of starting positions for 
# this set of alternatives.
#
# That's really clever.


def createMaze( paths ):
    maze = defaultdict(set)
    pos = {0}  # the current positions that we're building on
    stack = []  # a stack keeping track of (starts, ends) for groups
    starts, ends = {0}, {0}   # current possible starting and ending positions

    for c in paths:
        if c == '|':
            # An alternate: update possible ending points, and restart the group
            ends.update(pos)
            pos = starts
        elif c in 'NESW':
            # Move in a given direction, by updating all of possible positions
            # we might have started at.  Add these edges to the graph.
            direction = {'N': -1j, 'E': 1, 'S': 1j, 'W': -1}[c]
            for p in pos:
                maze[p].add( p+direction )
                maze[p+direction].add( p )
            pos = {p+direction for p in pos}
        elif c == '(':
            # Start of group.  Push the current starting set so we can use
            # it later, and start a new group.
            stack.append((starts, ends))
            starts, ends = pos, set()
        elif c == ')':
            # End of group.  Add the current positions as possible endpoints,
            # and pop the last positions off the stack.
            starts, ends = stack.pop()
            ends.update(pos)
    return maze

# Determine the path lengths.

def shortestPaths(graph):
    lengths = {0:0}
    visits = [0]
    steps = 0
    while visits:
        steps += 1
        nextstep = []
        for v in visits:
            for p in graph[v]:
                if p not in lengths:
                    lengths[p] = steps
                    nextstep.append( p )
        visits = nextstep
    return lengths

# Build the graph of all possible door movements.

graph = createMaze( sys.stdin.read() )
#printgraph(graph)

# find the shortest path lengths from the starting room to all other rooms

lengths = shortestPaths( graph )
#print( lengths )

print('part1:', max(lengths.values()))
print('part2:', sum(1 for length in lengths.values() if length >= 1000))
