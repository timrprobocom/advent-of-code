import os
import sys
import numpy as np
from collections import defaultdict, Counter
from itertools import permutations, combinations

test = """\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""


day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read()

# Convert the input into locks and keys.

def tobinary(pattern):
    return np.array( [[int(c=='#') for c in line] for line in pattern] )

locks = []
keys = []
for chunk in data.split('\n\n'):
    lines = chunk.splitlines()
    if lines[0][0] == '.':
        keys.append(tobinary(lines))
    else:
        locks.append(tobinary(lines))

# Any #/# invalidates.

def part1(locks, keys):
    sumx = 0
    for l in locks:
        for k in keys:
            x = l & k
            if not np.flatnonzero(x).size:
                sumx += 1
    return sumx

print("Part 1:", part1(locks,keys))