import sys
from collections import deque
from itertools import permutations

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

grid = """\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########""".splitlines()

if not TEST:
    grid = [k.strip() for k in open('day24.txt').readlines()]

numpos = [None] * 10
for y,row in enumerate(grid):
    for x,c in enumerate(row):
        if c in '0123456789':
            numpos[int(c)] = (y,x)
numpos = [n for n in numpos if n]
if DEBUG:
    print(numpos)

deltas = ((-1,0),(0,1),(1,0),(0,-1))

# Find distance from y0,x0 to y1,x1 using a BFS.
#
# We push all squares at distance 1.  Then we pop each and advance, pushing
# all squares at distance 2.  We will never start looking at distance N+1 until
# all squares at distance N-1 are popped.   As soon as we find a winner, 
# that's closest.

def distance( mp, fr, to ):
    q = deque([(0, fr)])
    vis = set([fr])
    while q:
        dst, cur = q.pop()
        if cur == to:
            return dst
        y,x = cur
        for dy,dx in deltas:
            ny, nx = y+dy, x+dx
            if mp[ny][nx] != '#' and (ny,nx) not in vis:
                q.appendleft( (dst+1, (ny,nx) ) )
                vis.add((ny,nx))
    return -1

# Compute the distances between all target squares.

dists = [ [distance(grid, a, b) for b in numpos] for a in numpos ]

if DEBUG:
    print( dists )

# Now do all permutations to find the shortest.

part1 = 99999
part2 = 99999
for path in permutations(range(len(numpos))):
    dst = dists[0][path[0]]
    for i in range(len(path)-1):
        dst += dists[path[i]][path[i+1]]
    part1 = min(part1, dst )
    if DEBUG:
        print( path, dst, end=' ' )
    dst += dists[0][path[-1]]
    if DEBUG:
        print( dst )
    part2 = min(part2, dst )

print('Part 1:', part1)
print('Part 2:', part2 )

