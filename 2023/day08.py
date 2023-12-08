import os
import sys
import math

test = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

test1 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test.splitlines()
elif 'test1' in sys.argv:
    data = test1.splitlines()
else:
    data = open(day+'.txt').readlines()

DEBUG = 'debug' in sys.argv

mapx = {}
for line in data:
    line = line.strip()
    if not line:
        continue
    if '=' not in line:
        directions = line
    else:
        parts = line.split()
        parts = [x.strip('(').strip(')').strip(',') for x in parts]
        mapx[parts[0]] = {'L': parts[2], 'R':parts[3]}


def part1():
    curr = 'AAA'
    if curr not in mapx:
        return None
    steps = 0
    while curr != 'ZZZ':
        i = steps % len(directions)
        curr = mapx[curr][directions[i]]
        steps += 1
    return steps

def part2():
    ghosts = [k for k in mapx if k[-1] == 'A']
    steplist = []
    for g in ghosts:
        steps = 0
        while g[-1] != 'Z':
            i = steps % len(directions)
            g = mapx[g][directions[i]]
            steps += 1
        steplist.append(steps)
    
    return math.lcm(*steplist)

print("Part 1:", part1())
print("Part 2:", part2())
