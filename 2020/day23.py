import os
import re
import sys
import functools
import itertools
import operator
from pprint import pprint

test = "389125467"

live = "215694783"

DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

if 'test' in sys.argv:
    data = test
else:
    data = live

    
class Node:
    def __init__(self,n):
        self.value = n

def process( vals, reps ):
    nvals = len(vals)

    dprint( "Build a list of nodes." )
    nodes = [Node(n) for n in vals]
    for i,node in enumerate(nodes):
        node.fwd = nodes[(i+1) % nvals]

    # This is the key -- lookup by cup value.

    dprint( "Build lookup by number." )
    lookup = {node.value: node for node in nodes}

    dprint( "Start rounds." )
    cur = nodes[0]
    for _ in range(reps):

        # Grab the three cups after the first.

        three = cur.fwd, cur.fwd.fwd, cur.fwd.fwd.fwd

        # Remove those three cups.

        cur.fwd = three[-1].fwd

        n = cur.value - 1
        if n == 0:
            n = nvals

        while any(node.value == n for node in three):
            n -= 1
            if n == 0:
                n = nvals

        # Find up the destination cup.

        dest = lookup[n]

        # Move the three cups after the dest,
        # Point the last of the three where dest used to point,
        # Scoot current forward.

        three[2].fwd = dest.fwd
        dest.fwd = three[0]
        cur = cur.fwd

    return lookup[1]


def part1( data ):
    vals = [int(x) for x in data]
    nbr1 = process( vals, 100 )
    mk = []
    link = nbr1.fwd
    while link.value != 1:
        mk.append( chr(link.value+48) )
        link = link.fwd
    return ''.join(mk)

def part2( data ):
    vals = [int(x) for x in data] + list(range(10,1000000+1))
    nbr1 = process( vals, 10000000 )
    return nbr1.fwd.value * nbr1.fwd.fwd.value

print( "Part 1:", part1( data ) )
print( "Part 2:", part2( data ) )

