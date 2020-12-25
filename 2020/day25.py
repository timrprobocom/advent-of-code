import os
import re
import sys
import functools
import itertools
import operator
from pprint import pprint

MOD = 20201227

test = ( 5764801, 17807724 )

live = ( 10604480, 4126658 )

DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

if 'test' in sys.argv:
    data = test
else:
    data = live

def transform( loops, subj ):
    return functools.reduce( lambda a, _: (a * subj) % MOD, range(loops), 1 )

def loop(data):
    subj = 7
    nx = 1
    answer = []
    for i in itertools.count(1):
        nx = (nx * subj) % MOD
        if nx in data:
            answer.append( (i,nx) )
            print( i, nx )
            if len(answer) == 2:
                return(answer)

ans = loop(data)
print( "Part 1:", transform( ans[0][0], ans[1][1] ) )
print( "Part 1:", transform( ans[1][0], ans[0][1] ) )
