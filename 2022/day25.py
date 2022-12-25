import sys
from collections import defaultdict, deque
import math

test = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [k.strip() for k in open('day25.txt').readlines()]

DEBUG = 'debug' in sys.argv


def parse(data):
    return data

data = parse(data)

codes = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

uncode = '012=-'

def convert(n):
    s = ''
    while n:
        r = n % 5
        n = n // 5 + (r >= 3)
        s = uncode[r] + s
    return s

def part1(data):
    sumx = 0
    for line in data:
        num = 0
        for c in line:
            num = num * 5 + codes[c]
        sumx += num

    print(sumx)
    return convert(sumx)

def part2(data):
    return 0

print("Part 1:", part1(data))
#print("Part 2:", part2(data))
