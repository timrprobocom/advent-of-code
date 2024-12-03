import os
import sys
import re

test = """\
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read().strip()

pat1 = r"mul\((\d*),(\d*)\)"
pat2 = pat1+r"|(do\(\))|(don't\(\))"

def part1(data):
    return sum( int(i)*int(j) for i,j in re.findall(pat1,data))

def part2(data):
    yes = 1
    sumx = 0
    for j in re.findall(pat2, data):
        if j[2]:
            yes = 1
        elif j[3]:
            yes = 0
        elif yes:
            sumx += int(j[0])*int(j[1])
    return sumx

print("Part 1:", part1(data))
print("Part 2:", part2(data))
