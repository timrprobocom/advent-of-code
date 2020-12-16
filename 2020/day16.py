import os
import sys
import functools
import itertools
import operator

test = """\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12""".split('\n\n')

test2 = """\
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9""".split('\n\n')

from pprint import pprint

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
elif 'test2' in sys.argv:
    data = test2
else:
    data = open('day16.txt').read().split('\n\n')

def parse(lines):
    # There are three parts to the input.
    rules = {}
    for line in lines[0].splitlines():
        keyword,_,parts = line.partition(': ')
        valid = set()
        for rule in parts.split(' or '):
            a,b = map(int, rule.split('-'))
            valid = valid.union(set(range(a,b+1)))
        rules[keyword] = valid

    # Now my ticket.
    line = lines[1].splitlines()[1]
    mytix = list(map(int, line.split(',')))

    # Now nearby tickets.
    nearby = []
    for line in lines[2].splitlines():
        if line[0] == 'n':
            continue
        nearby.append( list(map(int, line.split(','))) )

    return rules, mytix, nearby

def makevalid(rules):
    # Combine all ranges.
    return set().union( *rules.values() )

def part1(rules, nearby):
    valid = makevalid(rules)
    return sum( sum( t for t in tix if t not in valid ) for tix in nearby )

# OK, we have N fields.
# We need to know which fields each can be.

def part2( rules, mytix, nearby ):
    possible = dict( (k,set(range(len(rules)))) for k in rules.keys() )
    print( possible )

    valid = makevalid(rules)

    for tix in nearby:
        if any( t not in valid for t in tix ):
            continue
        for name,valid in rules.items():
            for i,t in enumerate(tix):
                if i in possible[name] and t not in valid:
                    possible[name].remove(i)
        
    # Pull out the certains.  It takes 7 passes for the full list.

    certain = {}
    while 1:
        removed = False
        for k,poss in possible.items():
            if len(poss) == 1 and k not in certain:
                value = next(iter(poss))
                certain[k] = value
                for k1, p1 in possible.items():
                    if k != k1 and value in p1:
                        removed = True
                        p1.remove(value)
        if not removed:
            break

    print( "Final:", possible )

    factor = 1
    for k, value in certain.items():
        print( k, value )
        if k.startswith('departure'):
            factor *= mytix[value]
    return factor


rules, mytix, nearby = parse(data)
print( "Part 1:", part1(rules, nearby) )
print( "Part 2:", part2(rules, mytix, nearby) )




