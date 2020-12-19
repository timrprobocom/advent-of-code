import os
import sys
import functools
import itertools
import operator
from pprint import pprint

test = """\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb""".split('\n\n')


DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

if 'test' in sys.argv:
    data = test
else:
    data = open('day19.txt').read().split('\n\n')

data = [d.splitlines() for d in data]

# It's not necessary to conert strings to ints.  Would it matter?

def parse(x):
    d = {}
    for line in x:
        i, rule = line.split(': ')
        d[i] = tuple(tuple(part.split()) for part in rule.split(' | '))
    return d

# If we match the start of the string, we yield the part after
# what we matched.  If we match the whole string, we yield an empty 
# string.  If we match nothing we yield nothing.

# The tuples here are either empty or contain one string.

def g(rules, x, i, d=''):
    dprint( d, "Checking", x, "rule", i )
    # For each set of possibles for this rule:
    for option in rules[i]:
        # If we've found a terminal and our target string 
        # starts with the terminal, we yield the rest of the 
        # string still to be matched.  It keeps getting
        # smaller and smaller.
        if option[0].startswith('"'):
            if x.startswith(option[0][1]):
                yield x[1:]
            continue

        # Start trying to match the rest of the string piece by piece.
        rems = (x,)
        # For each subsequence in this alternative:
        for token in option:
            # rems[0] keeps getting smaller as we match.
            # If we fail to match, rems becomes () and remains that way.
            rems = tuple(r for rem in rems for r in g(rules, rem, token, d+'+ '))
            dprint( d, token, rems )
        # If we have matched everything so far, rems contains a string.  
        # If we matched the whole string, rems contains an empty string.
        # Otherwise, it is empty.   If rems is empty, we failed and yield 
        # nothing.  Part 2 can actually return multiple successes.
        dprint( d, "rems", rems )
        for rem in rems:
            dprint( d, x, i, "yield", rem )
            yield rem

def part1(data):
    rules, strings = data
    rules = parse(rules)
    # Count only calls that yielded empty strings.  Empty tuple means
    # no match, non-empty string means there was leftover.
    return sum('' in g(rules, string, "0") for string in strings)

def part2(data):
    rules, strings = data
    rules += ('8: 42 | 42 8', '11: 42 31 | 42 11 31')
    rules = parse(rules)
    return sum('' in g(rules, string, "0") for string in strings)

print( part1(data) )
print( part2(data) )


