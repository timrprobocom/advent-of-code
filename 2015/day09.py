import os
import re
import sys
import functools
import itertools
import operator
from pprint import pprint

test = """\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141""".splitlines()


DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

if 'test' in sys.argv:
    data = test
else:
    data = open('day09.txt').read().split('\n')[:-1]

def parse(data):
    cities = set()
    route = {}
    for ln in data:
        p1,_,p2,_,dist = ln.split()
        cities.add( p1 )
        cities.add( p2 )
        route[(p1,p2)] = int(dist)
        route[(p2,p1)] = int(dist)
    return cities, route

cities, route = parse(data)
sums = []
for path in itertools.permutations(cities):
    sums.append(sum( route[k] for k in zip(path[:-1],path[1:]) ))

print( "Part 1:", min(sums) )
print( "Part 2:", max(sums) )
