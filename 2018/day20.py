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

    for y in range(n,s+1):
        for x in range(w,e+1):
            print( maze[x+y*1j], end=' | ')
        print()

def createMaze( paths ):
    maze = defaultdict(set)
    pos = {0}  # the current positions that we're building on
    stack = []  # a stack keeping track of (starts, ends) for groups
    starts, ends = {0}, {0}   # current possible starting and ending positions

    points = []
    for c in paths:
        if c == '|':
            # an alternate: update possible ending points, and restart the group
            ends.update(pos)
            pos = starts
        elif c in 'NESW':
            # move in a given direction: add all edges and update our current positions
            direction = {'N': 1, 'E': 1j, 'S': -1, 'W': -1j}[c]
#            print( tuple((p,p+direction) for p in pos) )
            for p in pos:
                maze[p].add( p+direction )
                maze[p+direction].add( p )
            pos = {p + direction for p in pos}
        elif c == '(':
            # start of group: add current positions as start of a new group
            stack.append((starts, ends))
            starts, ends = pos, set()
        elif c == ')':
            # end of group: finish current group, add current positions as possible ends
            starts, ends = stack.pop()
            ends.update(pos)
    return maze

# Build the graph of all possible door movements.

graph = createMaze( sys.stdin.read() )

print( len(graph) )

# Determine the path lengths.

lengths = defaultdict(int)

visits = [0]
lengths[0] = 0
steps = 0
while visits:
    steps += 1
    nextstep = []
    for v in visits:
        print(v, graph[v])
        for p in graph[v]:
            if p not in lengths:
                lengths[p] = steps
                nextstep.append( p )
    visits = nextstep

print( lengths )

# find the shortest path lengths from the starting room to all other rooms

print('part1:', max(lengths.values()))
print('part2:', sum(1 for length in lengths.values() if length >= 1000))
