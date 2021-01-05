import os
import re
import sys
import functools
import itertools
import operator
from pprint import pprint

test = [ 20, 15, 10, 5, 5 ]

live = [ 50, 44, 11, 49, 42, 46, 18, 32, 26, 40, 21, 7, 18, 43, 10, 47, 36, 24, 22, 40 ]

if 'test' in sys.argv:
    target = 25
    data = test
else:
    target = 150
    data = live

winners = []
def fill( nog, jugs, sofar ):
    print( nog, jugs )
    if not jugs:
        return
    for i in range(len(jugs)):
        if jugs[i] == nog:
            winners.append( sofar + [i] )
        elif jugs[i] < nog:
            fill( nog-jugs[i], jugs[i+1:], sofar + [i] )

fill( target, data, [] )
print("Part 1:", len(winners))
minx = min( map( len, winners ) )
print("Part 2:", sum( 1 for w in winners if len(w) == minx) )
