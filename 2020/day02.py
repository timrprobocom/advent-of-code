#! /usr/bin/env python3

import re
import sys

test = (
'1-3 a: abcde',
'1-3 b: cdefg',
'2-9 c: ccccccccc'
)

TEST = 'test' in sys.argv

pat = r"(\d+)-(\d+) (.): (.*)$"
pat = re.compile(pat)

def part1( line ):
    a, b, tgt, haystack = pat.match(line).groups()
    a, b = int(a), int(b)
    return a <= haystack.count(tgt)  <= b

def part2( line ):
    a, b, tgt, haystack = pat.match(line).groups()
    a, b = int(a), int(b)
    return (haystack[a-1] == tgt) != (haystack[b-1] == tgt)

live = open('day02.txt').readlines()
if TEST:
    data = test
else:
    data = live

def evaluate( lines, partx ):
    return sum( partx(line) for line in lines )

print( "Part 1:", evaluate( data, part1 ) )
print( "Part 2:", evaluate( data, part2 ) )
