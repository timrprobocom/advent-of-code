import os
import sys
from collections import defaultdict

test = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read()
data = data.splitlines()

def part1(data):
    count = 0
    beams = {}
    for n, row in enumerate(data[::2]):
        if not n:
            beams[row.find('S')] = 1
            continue
        nbeams = defaultdict(int)
        for i,c in beams.items():
            if row[i] == '.':
                nbeams[i] += c
            else:
                count += 1
                if i > 0:
                    nbeams[i-1] += c
                if i < len(row)-1:
                    nbeams[i+1] += c
        beams = nbeams
        if DEBUG:
            print(n,beams)
    return count, sum(beams.values())

p1,p2 = part1(data)
print("Part 1:", p1)
print("Part 2:", p2)
