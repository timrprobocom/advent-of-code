import os
import sys

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

data = data.replace('#','1').replace('.','0')

def tobinary(pattern):
    return int((''.join(pattern)),2)

locks = []
keys = []
for chunk in data.split('\n\n'):
    lines = chunk.splitlines()
    if lines[0][0] == '0':
        keys.append(tobinary(lines))
    else:
        locks.append(tobinary(lines))

# Any #/# invalidates.

def part1(locks, keys):
    return sum(not (l&k) for k in keys for l in locks)

print("Part 1:", part1(locks,keys))