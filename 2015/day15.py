import os
import re
import sys
import functools
import itertools
import operator
from pprint import pprint

test = """\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3""".splitlines()

DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

if 'test' in sys.argv:
    data = test
else:
    data = open('day15.txt').read().split('\n')[:-1]

def parse(data):
    ingred = []
    for ln in data:
        name,rest = ln.split(': ')
        attrs = {}
        for attr in rest.split(', '):
            a,b = attr.split()
            attrs[a] = int(b)
        ingred.append( attrs )
    return ingred

def make2():
    for i in range(100):
        yield i+1, 99-i

def make4():
    for i in range(100):
        for j in range(99-i):
            for k in range(98-i-j):
                yield i+1, j+1, k+1, 97-i-j-k

make = make2 if 'test' in sys.argv else make4

ingred = parse(data)

attrs = list(ingred[0].keys())
attrs.remove('calories')

def check(prop):
    return sum( ing['calories'] * f for ing,f in zip(ingred,prop) ) == 500

def combine1(prop):
    return functools.reduce(operator.mul, (max( 0, sum( ing[name] * f for ing,f in zip(ingred,prop ) ) ) for name in attrs ) )

def combine2(prop):
    return combine1(prop) if check(prop) else 0

print( "Part 1:", max( combine1(m) for m in make() ) )
print( "Part 2:", max( combine2(m) for m in make() ) )
