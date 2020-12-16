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
38,6,12""".splitlines()

test2 = """\
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9""".splitlines()

from pprint import pprint

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
elif 'test2' in sys.argv:
    data = test2
else:
    data = open('day16.txt').read().split('\n')[:-1]

def parse(lines):
    lines = itertools.chain(lines)
    rules = {}
    for line in lines:
        if not line:
            break
        keyword,_,parts = line.partition(': ')
        valid = set()
        for rule in parts.split(' or '):
            a,b = [int(i) for i in rule.split('-')]
            valid = valid.union(set(range(a,b+1)))
        rules[keyword] = valid

    # Now my ticket.
    line = next(lines)
    line = next(lines)
    mytix = [int(i) for i in line.split(',')]
    line = next(lines)

    #  Now nearby tickets.
    nearby = []
    line = next(lines)
    for line in lines:
        nearby.append( [int(i) for i in line.split(',')] )

    return rules, mytix, nearby

def makevalid(rules):
    valid = set()
    # Get all ranges
    for rule in rules.values():
        valid = valid.union(rule)
    return valid

def part1(rules, nearby):
    valid = makevalid(rules)
    return sum( sum( t for t in tix if t not in valid ) for tix in nearby )

# OK, we have N fields.
# We need to know which fields each can be.

def part2( rules, mytix, nearby ):
    possible = {}
    for k in rules.keys():
        possible[k] = set(range(len(rules)))
    print( possible )

    valid = makevalid(rules)

    for tix in nearby:
        if any( t not in valid for t in tix ):
            continue
        for name,valid in rules.items():
            for i,t in enumerate(tix):
                if i in possible[name] and t not in valid:
                    possible[name].remove(i)
        
    # Pull out the certains.

    certain = {}
    while 1:
        moved = []
        for k,poss in possible.items():
            if len(poss) == 1:
                certain[k] = list(poss)[0]
                moved.append(k)
        for k in moved:
            del possible[k]
        removed = False
        for k,cert in certain.items():
            for k1, p1 in possible.items():
                if cert in p1:
                    removed = True
                    p1.remove(cert)
        if not removed:
            break

    print( "Final:", possible )

    factor = 1
    for k, cert in certain.items():
        print( k, cert )
        if k.startswith('departure'):
            factor *= mytix[cert]
    return factor

rules, mytix, nearby = parse(data)
print( "Part 1:", part1(rules, nearby) )
print( "Part 2:", part2(rules, mytix, nearby) )




