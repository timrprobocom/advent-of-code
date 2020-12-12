import os
import sys
import functools
import operator
from tools import Point

test = """\
F10
N3
F7
R90
F11""".splitlines()

from pprint import pprint

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
else:
    data = open('day12.txt').read().split('\n')[:-1]


deltas = { 
    'N': Point( 0,-1),
    'E': Point( 1, 0),
    'S': Point( 0, 1),
    'W': Point(-1, 0)
}

# N and E are negative.

def part1():
    ship = Point(0,0)
    facing = deltas['E']
    for ln in data:
        direc = ln[0]
        dist = int(ln[1:])
        if direc in 'NESW':
            ship += deltas[direc] * dist
        elif direc in 'L':
            count = dist // 90
            for i in range(count):
                facing = facing.left()
        elif direc in 'R':
            count = dist // 90
            for i in range(count):
                facing = facing.right()
        elif direc == 'F':
            ship += facing * dist
        if DEBUG:
            print(ln,ship)
    return ship.mandist()


def part2():
    ship = Point(0,0)
    waypt = Point(10,-1)
    for ln in data:
        direc = ln[0]
        dist = int(ln[1:])
        if direc in 'NESW':
            waypt += deltas[direc] * dist
        elif direc in 'L':
            count = dist // 90
            for i in range(count):
                waypt = waypt.left()
        elif direc in 'R':
            count = dist // 90
            for i in range(count):
                waypt = waypt.right()
        elif direc == 'F':
            ship += waypt * dist
        if DEBUG:
            print(ln,ship,waypt)
    return ship.mandist()


print('Part 1:', part1())
print('Part 2:', part2())


