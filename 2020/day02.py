#! /usr/bin/env python3

import re

test = (
'1-3 a: abcde',
'1-3 b: cdefg',
'2-9 c: ccccccccc'
)

pat = r"(\d+)-(\d+) (.): (.*)$"
pat = re.compile(pat)

def pass1( line ):
    a, b, tgt, haystack = pat.match(line).groups()
    a, b = int(a), int(b)
    return a <= haystack.count(tgt)  <= b

def pass2( line ):
    a, b, tgt, haystack = pat.match(line).groups()
    a, b = int(a), int(b)
    return (haystack[a-1] == tgt) != (haystack[b-1] == tgt)

live = open('day02.txt').readlines()

def evaluate( lines, passx ):
    return sum( passx(line) for line in lines )

print( "2:", evaluate( test, pass1 ) )
print( "Part 1:", evaluate( live, pass1 ) )
print( "1:", evaluate( test, pass2 ) )
print( "Part 2:", evaluate( live, pass2 ) )
