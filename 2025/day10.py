import os
import sys
import itertools
import numpy as np
from scipy.optimize import linprog

test = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read()

data = data.splitlines()

def parse(data):
    lights = []
    presses = []
    joltage = []
    for line in data:
        l1, *parts, j1 = line.split()
        lights.append(list(int(c == '#') for c in l1[1:-1]))
        joltage.append(list(map(int,j1.strip('{}').split(','))))
        pp = []
        for p in parts:
            pp.append( tuple(map(int, p.strip('()').split(','))))
        presses.append(pp)
    return lights, presses, joltage

def toggle(lights,switch):
    for i in switch:
        lights[i] = 1 - lights[i]

def part1(lights, presses):
    sum = 0
    for target,prs in zip(lights,presses):
        found = 0
        for i in range(1,len(prs)+1):
            for cx in itertools.combinations(prs,i):
                mylights = [0]*len(target)
                for c in cx:
                    toggle(mylights, c)
                if mylights == target:
                    found = i
                    break 
            if found:
                sum += found
                break
        assert found
    return sum

def solve2(goal, moves):
    c = np.ones(len(moves))
    A_eq = np.zeros((len(goal), len(moves)))
    b_eq = np.array(goal)
    for i in range(len(goal)):
        A_eq[i] = [1 if i in m else 0 for m in moves]
    return round(linprog(c, A_eq=A_eq, b_eq=b_eq, integrality=True).fun)

def part2(presses, joltage):
    return sum( solve2(j,p) for p,j in zip(presses,joltage) )

lights, presses, joltage = parse(data)                

print("Part 1:", part1(lights, presses))
print("Part 2:", part2(presses, joltage))
