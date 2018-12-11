#
#  Holy shit.  This is very clever.  I need to remember this algorithm.
#

grid = """\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########""".splitlines()

grid = [k.strip() for k in open('day24.txt').readlines()]

from collections import deque
from itertools import permutations
import sys

def find_in_map( mp, c ):
    return [(y,x) for y in range(len(mp)) for x in range(len(mp[y])) if mp[y][x]==c]

numpos = [ k[0] for k in [ find_in_map(grid, c) for c in '0123456789' ] if k ]
print numpos

deltas = ((-1,0),(0,1),(1,0),(0,-1))

# Find distance from y0,x0 to y1,x1.  This does an exhaustive search.
# How do we know this is minimal?
# We push all squares at distance 1.  Then we pop each and advance, pushing
# all squares at distance 2.  We will never start looking at distance N+1 until
# all squares at distance N-1 are popped.   As soon as we find
# a winner, that's closest.

def distance( mp, fr, to ):
    print fr, to
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
        print q
    return -1

# Compute the distances between all target squares.

dists = []
for a in numpos:
    dists.append( [distance(grid, a, b) for b in numpos] )

print dists

# Now do all permutations to find the shortest.

part1 = 99999
part2 = 99999
for path in permutations(range(len(numpos))):
    dst = dists[0][path[0]]
    for i in range(len(path)-1):
        dst += dists[path[i]][path[i+1]]
    part1 = min(part1, dst )
    print path, dst,
    dst += dists[0][path[-1]]
    print dst
    part2 = min(part2, dst )

print part1, part2

