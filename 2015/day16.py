import os
import re
import sys
import functools
import itertools
import operator
from pprint import pprint

gift = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

# Sue 2: perfumes: 5, trees: 8, goldfish: 8

def scan(more,less):
    for ln in open('day16.txt'):
        fail = False
        p1,_,p2 = ln[4:].partition(': ')
        for attr in p2.split(', '):
            a,n = attr.split(': ')
            n = int(n)
            if a in more:
                fail = n <= gift[a]
            elif a in less:
                fail = n >= gift[a]
            else:
                fail = n != gift[a]
            if fail:
                break
        if not fail:
            return p1

more = ['cats','trees']
less = ['pomeranians','goldfish']

print( "Part 1:", scan([],[]) )
print( "Part 2:", scan(more,less) )

