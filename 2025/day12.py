import os
import sys
import functools
from collections import defaultdict

test = """\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""

# 4s nest to make a 4x4.
# 3 3 5 nest to make a solid 7x3.
# 1 3 nest to make a 5x3.
# 0 2 0 makes a 7x3.

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read()

data = data.splitlines()

def parse(data):
    regions = []
    for line in data:
        if 'x' in line:
            # This is a region.
            regions.append( [int(i) for i in line.replace('x',' ').replace(':',' ').split()])
    return regions

def part1(data):
    regions = parse(data)
    count = 0
    for x,y,*region in regions:
        count += sum(region) * 8 < x * y
    return count
                
print("Part 1:", part1(data))