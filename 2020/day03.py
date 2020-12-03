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
    data = [ln.strip() for ln in open('day03.txt').readlines()]

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

def counttrees( dx, dy ):
    x,y = 0,0
    count = 0
    while y < len(data):
        if data[y][x] == '#':
            count += 1
        x = (x + dx) % len(data[0])
        y += dy
    return count

def try2():
    return [counttrees(*s) for s in ((1,1),(3,1),(5,1),(7,1),(1,2))]

counts = try2()
print( "Part 1:", counts[1] )
print( "Part 2:", counts[0] * counts[1] * counts[2] * counts[3] * counts[4] )

