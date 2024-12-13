import os
import sys
import re
import math
import numpy as np

test = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

match1 = re.compile(r"Button ([AB]): X\+(\d*), Y\+(\d*)")
match2 = re.compile(r"(P)rize: X=(\d*), Y=(\d*)")

sets = []
g = []
for line in data:
    for tryme in match1, match2:
        m = tryme.match(line)
        if m:
            g.extend( [int(m[2]),int(m[3])] )
            if m[1] == 'P':
                sets.append(g)
                g = []

data = sets

def part1(data):
    sumx = 0
    for game in data:
        ax,ay,bx,by,px,py = game
        if DEBUG:
            print(ax,ay,bx,by,px,py)
        for a in range(1,px//ax):
            if (px - a*ax) % bx == 0:
                b = (px - a*ax) // bx
                if ay*a + by*b == py:
                    sumx += a*3 + b
                    break
    return sumx

# This can be used to solve part 1 as well, by passing 0.

def part2(data,offset=10000000000000):
    sumx = 0
    for game in data:
        ax,ay,bx,by,px,py = game
        px += offset
        py += offset
        a,b = np.linalg.solve( ([ax,bx],[ay,by]), ([px,py]) )
        # If the solution is not integral, there is no solution.
        a=round(a)
        b=round(b)
        if a*ax+b*bx == px and a*ay+b*by == py:
            sumx += a*3 + b
    return sumx

print("Part 1:", part1(data))
print("Part 1:", part2(data,0))
print("Part 2:", part2(data))