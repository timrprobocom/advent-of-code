from __future__ import print_function
import sys

# So, here's the magic.  Rather than build all of the possible strings
# up to this point, pos simply holds the list of coordinates we might be
# at, based on all the alternatives to this point.  When we get an 
# alternative, we start again with the list of starting positions for 
# this set of alternatives.
#
# That's really clever.

def createMaze( paths ):
    base = (0,0)
    maze = {base:0}
    pos = {base}  # the current positions that we're building on
    stack = []  # a stack keeping track of (starts, ends) for groups
    starts, ends = {base}, set()   # current possible starting and ending positions

    for c in paths:
        if c == '|':
            # An alternate: update possible ending points, and restart the group
            ends.update(pos)
            pos = starts
        elif c in 'NESW':
            # Move in a given direction, by updating all of possible positions
            # we might have started at.  Add these edges to the graph.
            direction = {'N': (0,-1), 'E': (1,0), 'S': (0,1), 'W': (-1,0)}[c]
            newpos = {(p[0]+direction[0],p[1]+direction[1]) for p in pos}
            for opt,npt in zip(pos,newpos):
                if npt not in maze:
                    maze[npt] = maze[opt] + 1
            pos = newpos
        elif c == '(':
            # Start of group.  Push the current starting set so we can use
            # it later, and start a new group.
            stack.append(starts)
            starts, ends = pos, set()
        elif c == ')':
            # End of group.  Add the current positions as possible endpoints,
            # and pop the last start positions off the stack.
            pos.update(ends)
            starts = stack.pop()
    return maze

# Build the graph of all possible movements.

graph = createMaze( sys.stdin.read() )
#printgraph(graph)

print( "Part 1:", max(pt for pt in graph.values()) )
print( "Part 2:", sum(1 for pt in graph.values() if pt >= 1000) )
