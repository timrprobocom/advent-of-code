import sys
import itertools
import functools
import operator

DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

test = [ 1, 2, 3, 4, 5, 7, 8, 9, 10, 11 ]
live = [
    1, 3, 5, 11, 13, 17, 19, 23, 29, 31, 37,
    41, 43, 47, 53, 59, 67, 71, 73, 79, 83, 89,
    97, 101, 103, 107, 109, 113
]

if 'test' in sys.argv:
    data = test
else:
    data = live

data.reverse()

# How many ways are there to make N/3?


def fill(data, pkgs=[]):
    sumsofar = sum(pkgs)
    last = pkgs[-1] if pkgs else 999
    for n in data:
        if n >= last:
            continue
        if answers and len(pkgs) > answers[0][0]:
            return
        if sumsofar + n == each:
            pkgs.append( n )
            qe = functools.reduce( operator.mul, pkgs )
            answers.append( (len(pkgs), qe, pkgs ) )
            return 
        if sumsofar + n < each:
            fill(data,pkgs+[n])

answers = []
each = sum(data) // 3
fill( data, [] )
for i in answers:
    dprint(i)
print( min(answers) )
print( "Part 1:", min(answers)[1] )

answers = []
each = sum(data) // 4
fill( data, [] )
for i in answers:
    dprint(i)
print( min(answers) )
print( "Part 1:", min(answers)[1] )

