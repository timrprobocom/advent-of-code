import os
import sys
import functools
import itertools
import operator

test = """\
.#.
..#
###""".split('\n')

from pprint import pprint

DEBUG = 'debug' in sys.argv

GRID = 'grid' in sys.argv

if 'test' in sys.argv:
    data = test
else:
    data = open('day17.txt').read().split('\n')

# What's the data structure?
# List of triples?

adjacent = list(itertools.product((-1,0,1), repeat=4))
adjacent.remove( (0,0,0,0) )

def translate(data):
    return set(
        (x,y,0,0) 
        for y,ln in enumerate(data)
        for x,c in enumerate(ln) if c == '#'
    )

def countneighbors( cell, state ):
    x,y,z,w = cell
    return sum( (x+dx,y+dy,z+dz,w+dw) in state for dx,dy,dz,dw in adjacent )

def printgrid( state ):
    minx,miny,minz,minw,maxx,maxy,maxz,maxw = minmax(state)
    for z in range(minz,maxz+1):
        print( "Layer", z )
        for y in range(miny,maxy+1):
            line = ['.'] * (maxx-minx+1)
            for x in range(minx,maxx+1):
                if (x,y,z,0) in state:
                    line[x-minx] = '#'
            print( ''.join(line) )

def minmax(state):
    mns = tuple( min(k[i] for k in state) for i in range(4) )
    mxs = tuple( max(k[i] for k in state) for i in range(4) )
    return mns+mxs

def nextstate(state,part=1):
    minx,miny,minz,minw,maxx,maxy,maxz,maxw = minmax(state)
    wrange = (0,) if part==1 else range(minw-1,maxw+2)

    new = set()
    for w in wrange:
        for z in range(minz-1,maxz+2):
            for y in range(miny-1,maxy+2):
                for x in range(minx-1,maxx+2):
                    cell = (x,y,z,w)
                    neighbors = countneighbors(cell,state)
                    if neighbors == 3 or (cell in state and neighbors == 2):
                        new.add( cell )
    return new

state = translate( data )
for i in range(6):
    state = nextstate( state, 1 )
    print( len(state) )
    if GRID:
        printgrid( state )

print( "Part 1:", len(state) )

state = translate( data )
for i in range(6):
    state = nextstate( state, 2 )
    print( len(state) )

print( "Part 2:", len(state) )
