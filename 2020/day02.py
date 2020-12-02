#! /usr/bin/env python3

test = (
'1-3 a: abcde',
'1-3 b: cdefg',
'2-9 c: ccccccccc'
)

def pass1( line ):
    count,target,haystack = line.split()
    a,b = [int(k) for k in count.split('-')]
    target = target[0]
    haystack = list(haystack)
    return a <= haystack.count(target)  <= b

def pass2( line ):
    count,target,haystack = line.split()
    a,b = [int(k) for k in count.split('-')]
    target = target[0]
    return (haystack[a-1] == target) != (haystack[b-1] == target)

live = open('day02.txt').readlines()

def evaluate( lines, passx ):
    return sum( 1 for line in lines if passx(line) )

print( "2:", evaluate( test, pass1 ) )
print( "Part 1:", evaluate( live, pass1 ) )
print( "1:", evaluate( test, pass2 ) )
print( "Part 2:", evaluate( live, pass2 ) )
