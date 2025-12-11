import os
import sys
import functools
from collections import defaultdict

test = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

test2 = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read()

data = data.splitlines()

@functools.cache
def paths( s, d ):
    return ( d in connx[ s ] ) + sum( paths( n, d ) for n in connx[ s ] )

# connx has to be global for the cache to work.

def parse(data):
    global connx
    paths.cache_clear()
    connx = {"out":[]}
    for line in data:
        parts = line.split(" ")
        connx[parts[0][:-1]] = parts[1:]

def part1(data):
    parse(data)
    return paths( "you", "out" )

def part2(data):
    parse(data)
    return (
        paths( "svr", "dac" ) * paths( "dac", "fft" ) * paths( "fft", "out" ) +
        paths( "svr", "fft" ) * paths( "fft", "dac" ) * paths( "dac", "out" )
    )
                
print("Part 1:", part1(data))
if TEST:
    data = test2.splitlines()
print("Part 2:", part2(data))
