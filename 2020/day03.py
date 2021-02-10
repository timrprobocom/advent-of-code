#! /usr/bin/env python3

import sys

test = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""".split()

if 'test' in sys.argv:
    data = test
else:
#    data = [ln.strip() for ln in open('day03.txt').readlines()]
    data = open('day03.txt').read().split('\n')[:-1]

# This could have been done smarter.

def try1():
    counts = [0,0,0,0,0]
    x = [0,0,0,0,0]
    dx = [1,3,5,7,1]
    dy = [1,1,1,1,2]

    for y,ln in enumerate(data):
        for i in range(len(x)):
            if y % dy[i]:
                continue
            if ln[x[i]] == '#':
                counts[i] += 1
            x[i] = (x[i] + dx[i]) % len(ln)

    return counts
    print( "Part 1:", counts[1] )
    print( "Part 2:", counts[0] * counts[1] * counts[2] * counts[3] * counts[4] )

def coords(dx,dy,limx,limy):
    x,y = 0,0
    while y < limy:
        yield x,y
        x = (x + dx) % limx
        y += dy

def counttrees( dx, dy ):
    return sum( 1 
        for x,y in coords(dx, dy, len(data[0]), len(data)) 
        if data[y][x]=='#' 
    )

def try2():
    return [counttrees(*s) for s in ((1,1),(3,1),(5,1),(7,1),(1,2))]

counts = try2()
print( "Part 1:", counts[1] )
print( "Part 2:", counts[0] * counts[1] * counts[2] * counts[3] * counts[4] )

