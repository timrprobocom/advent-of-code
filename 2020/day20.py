import os
import re
import sys
import math
import functools
import operator
from pprint import pprint

test = """\
""".split('\n')

# I've made this way too complicated.

# 1: 26 437 12240 13632 sum 26335
# 2: 46 1445 669060 23340 sum 693891

DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

if 'test' in sys.argv:
    data = open('test20.txt').read().split('\n\n')
else:
    data = open('day20.txt').read().split('\n\n')

# Which edge is it?  
# 0 = N
# 1 = S
# 2 = E
# 3 = W
# 4 = N rev
# 5 = S rev
# 6 = E rev
# 7 = W rev

# Contains the list of tiles that contain the edge string.
edges = {}
# Contains the set of tiles that adjoin this tile.
matches = {}
# Contains the strings for each rotation.
rotations = {}

def record( tno, reflect, edge ):
    if tno not in rotations:
        rotations[tno] = [0]*8
    rotations[tno][reflect] = edge
    if edge not in edges:
        edges[edge] = [tno]
    else:
        edges[edge].append( tno )

def reverse(s):
    l = list(s)
    l.reverse()
    return ''.join(l)
 
count = 0
tiles = {}
for tile in data:
    grid = tile.splitlines()
    tileno = int(grid.pop(0).split()[1][:-1])
    matches[tileno] = set()
    tiles[tileno] = grid

    for t in grid[1:-1]:
        count += t[1:-1].count('#')

# Record all possible reflections.

    g1 = ''.join( g[0] for g in grid )
    g2 = ''.join( g[-1] for g in grid )

    record( tileno, 0, grid[0] )
    record( tileno, 4, reverse(grid[0]) )
    record( tileno, 1, grid[-1] )
    record( tileno, 5, reverse(grid[-1]) )
    record( tileno, 3 , g1 )
    record( tileno, 7, reverse(g1) )
    record( tileno, 2, g2 )
    record( tileno, 6, reverse(g2) )

# Which tiles have edges in common?

for e,tlist in edges.items():
    if len(tlist) > 1:
        matches[tlist[0]].add( tlist[1] )
        matches[tlist[1]].add( tlist[0] )

for e,v in matches.items():
    matches[e] = list(v)

gridsize = int(math.sqrt(len(data)))

# Test is 3x3, count is 303
# Live is 12x12, count is 2806 - 15 * 12

def prod(it):
    return functools.reduce( operator.mul, it, 1 )

def part1():
    return prod( t for t, tlist in matches.items() if len(tlist) == 2 )

# How do we stitch this together?
# The 2s have to be corners.  The 3s are edges.  The 4s are centers.
#

def findgrid():
    grid = list( [0]*gridsize for i in range(gridsize) )
    placed = set()

    # So, pick a 2.

    for e,tlist in matches.items():
        if len(tlist) == 2:
            grid[0][0] = e
            placed.add(e)
            break

    # We can fill out the row by just picking the first.

    for ctr in range( 1, gridsize-1 ):
        for e,tlist in matches.items():
            if e in placed: continue
            if grid[0][ctr-1] in tlist and len(tlist) == 3:
                grid[0][ctr] = e
                placed.add(e)
                break

    # Pick a right, a match were len = 2.

    for n in matches[grid[0][-2]]:
        if len(matches[n]) == 2:
            grid[0][-1] = n
            placed.add(e)
            break
    
    # Now do middle rows.

    for row in range( 1, gridsize-1 ):
        for e,tlist in matches.items():
            if e in placed: continue
            if grid[row-1][0] in tlist and len(tlist) == 3:
                grid[row][0] = e
                placed.add( e )
                break

        for col in range(1, gridsize-1 ):
            for e,tlist in matches.items():
                if e in placed: continue
                if grid[row][col-1] in tlist and grid[row-1][col] in tlist:
                    grid[row][col] = e
                    placed.add( e )
                    break

        for e,tlist in matches.items():
            if e in placed: continue
            if grid[row-1][-1] in tlist and len(tlist) == 3:
                grid[row][-1] = e
                placed.add( e )
                break

    # Now do last row.

    for e,tlist in matches.items():
        if e in placed: continue
        if len(tlist) == 2 and grid[-2][0] in tlist:
            grid[-1][0] = e
            placed.add( e )
            break

    for col in range(1, gridsize-1):
        for e,tlist in matches.items():
            if e in placed: continue
            if grid[-2][col] in tlist: #and grid[-1][col-1] in tlist:
                grid[-1][col] = e
                placed.add( e )
                break

    for e,tlist in matches.items():
        if e in placed: continue
        if grid[-1][-2] in tlist and grid[-2][-1] in tlist:
            grid[-1][-1] = e
            break

    return grid

def r_hflip( tile ):
    # Horizontal flip.
    return [reverse(ln) for ln in tile]

def r_vflip( tile ):
    # Vertical flip.
    new = tile[:]
    new.reverse()
    return new

def r_rot90cw( tile ):
    # Clockwise rotation.
    llen = len(tile)
    return [ ''.join( tile[llen-col-1][row] for col in range(llen)) for row in range(llen) ]

N,S,E,W = (0,1,2,3)

# rotations (right, down)
#  E S == nothing
#  E N == v flip
#  W S == h flip
#  W N == h flip, v flip
#  N E == rot 90 cw
#  N W == h flip, rot 90 cw
#  S E == h flip, v flip, rot 90 cw
#  S W == v flip, rot 90 cw

# So, if the right side was the E edge and the bottom side was the S edge, no rotation.

rotate_mapping = {
    (E,S): (),
    (E,N): (r_vflip,),
    (W,S): (r_hflip,),
    (W,N): (r_hflip, r_vflip),
    (N,E): (r_rot90cw,),
    (N,W): (r_hflip, r_rot90cw),
    (S,E): (r_vflip, r_rot90cw),
    (S,W): (r_hflip, r_vflip, r_rot90cw)
}

def rotate_cell( target, found1, found2 ):
    for xform in rotate_mapping[found1,found2]:
        tiles[target] = xform(tiles[target])


def rotate_grid( grid ):
    # For each element, find which one they have in common, right and down.
    for row in range(gridsize-1):
        for col in range(gridsize-1):
            target = grid[row][col]
            # Find the grid matches.
            dprint( row, col, target, grid[row][col+1], grid[row+1][col] )
            found1,found2 = -1,-1
            for m,ms in enumerate(rotations[target][:4]):
                if ms in rotations[grid[row][col+1]]:
                    found1 = m
                    break
            for m,ms in enumerate(rotations[target][:4]):
                if ms in rotations[grid[row+1][col]]:
                    found2 = m
                    break
            rotate_cell( target, found1, found2 )

    # Do the right column.  Check left and down.
    col = -1
    for row in range(gridsize-1):
        target = grid[row][col]
        dprint( row, gridsize-1, target, grid[row][-2], grid[row+1][-1] )
        found1,found2 = -1,-1
        for m,ms in enumerate(rotations[target][:4]):
            if ms in rotations[grid[row][col-1]]:
                found1 = m ^ 1
                break
        for m,ms in enumerate(rotations[target][:4]):
            if ms in rotations[grid[row+1][col]]:
                found2 = m
                break
        rotate_cell( target, found1, found2 )

    # Do the bottom row.  Check right and up.
    row = -1
    for col in range(gridsize-1):
        target = grid[row][col]
        dprint( row, col, target, grid[row][col+1], grid[row-1][col] )
        found1,found2 = -1,-1
        for m,ms in enumerate(rotations[target][:4]):
            if ms in rotations[grid[row][col+1]]:
                found1 = m 
                break
        for m,ms in enumerate(rotations[target][:4]):
            if ms in rotations[grid[row-1][col]]:
                found2 = m ^ 1
                break
        rotate_cell( target, found1, found2 )

    # Do the final cell, do up and left.
    col = row = -1
    target = grid[row][col]
    found1,found2 = -1,-1
    dprint( gridsize-1, gridsize-1, target, grid[-1][-2], grid[-2][-1] )
    for m,ms in enumerate(rotations[target][:4]):
        if ms in rotations[grid[-1][-2]]:
            found1 = m ^ 1
            break
    for m,ms in enumerate(rotations[target][:4]):
        if ms in rotations[grid[-2][-1]]:
            found2 = m ^ 1
            break
    rotate_cell( target, found1, found2 )

def stitchgrid( tiles, grid ):
    biggrid = []
    subrows = len(tiles[grid[0][0]])
    for row in grid:
        for y in range(1,subrows-1):
            line = []
            for col in row:
                line.append( ''.join( tiles[col][y][1:-1] ) )
            biggrid.append( ''.join( line ) )
    return biggrid


"""
01234567890123456789
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""

monster = (
    (0,18),
    (1,0),(1,5),(1,6),(1,11),(1,12),(1,17),(1,18),(1,19),
    (2,1),(2,4),(2,7),(2,10),(2,13),(2,16)
)

msize = (3,20)

def search1( biggrid ):
    pattern = r"(?=#..{76}#....##....##....###.{76}.#..#..#..#..#..#)"
    bg = ''.join(r_rot90cw(r_vflip(biggrid)))
    return len(re.findall(pattern, bg))

def search1( biggrid ):
    pattern = r"(?=#\S.{77}#\S\S\S\S##\S\S\S\S##\S\S\S\S###.{77}\S#\S\S#\S\S#\S\S#\S\S#\S\S#)"
    bg = ' '.join(r_rot90cw(r_vflip(biggrid)))
    return len(re.findall(pattern, bg))

def search2( biggrid ):
    count = 0
    bglen = len(biggrid)
    for row in range(0,bglen-3):
        for col in range(0,bglen-20):
            if all( biggrid[col+dx][row+dy] == '#' for dy,dx in monster ):
                count += 1
    return count


def search( biggrid ):
    count = 0
    bglen = len(biggrid)
    for row in range(0,bglen-3):
        for col in range(0,bglen-20):
            # Check primary.
            if all( biggrid[row+dy][col+dx] == '#' for dy,dx in monster ):
                count += 1
                print( "FOUND 1", row, col )
            # Check flip.
            if all( biggrid[-row-dy-1][col+dx] == '#' for dy,dx in monster ):
                count += 1
                print( "FOUND 2", row, col )
            # Check vflikp.
            if all( biggrid[-row-dy-1][-col-dx-1] == '#' for dy,dx in monster ):
                count += 1
                print( "FOUND 3", row, col )
            # Check flip.
            if all( biggrid[row+dy][-col-dx-1] == '#' for dy,dx in monster ):
                count += 1
                print( "FOUND 4", row, col )
            # Check rotate primary.
            if all( biggrid[col+dx][row+dy] == '#' for dy,dx in monster ):
                count += 1
                print( "FOUND 5", row, col )
            # Check rotate flip.
            if all( biggrid[-col-dx-1][row+dy] == '#' for dy,dx in monster ):
                count += 1
                print( "FOUND 6", row, col )
            # Check rotate vflip
            if all( biggrid[-col-dx-1][-row-dy-1] == '#' for dy,dx in monster ):
                count += 1
                print( "FOUND 7", row, col )
            # Check rotate flip.
            if all( biggrid[col+dx][-row-dy-1] == '#' for dy,dx in monster ):
                count += 1
                print( "FOUND 8", row, col )
    return count

               

print( "Part 1:", part1() )

grid = findgrid()

rotate_grid(grid)

biggrid = stitchgrid( tiles, grid )

if DEBUG:
    pprint( biggrid )

import time
t1 = time.time()
print( search1(biggrid))
print( search2(biggrid))
for i in range(100):
    search1(biggrid)
t2 = time.time()
for i in range(100):
    search2(biggrid)
t3 = time.time()
print( t2-t1, t3-t2 )

ogres = search(biggrid)

print( "Part 2:", count - 15*ogres )

