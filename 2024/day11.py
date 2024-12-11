import os
import sys
from functools import cache

test = """\
125 17"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read().strip()

data = [int(d) for d in data.split()]

# 0 becomes 1
# Even digits: split in two, half on each stone
# Else N becomes 2024*N

# The key here is recognizing that the stones are independent.  A given
# stone will always follow the same path.  So, we can cache the results 
# without actually tracking the stones.

@cache
def blink(s, n):
    if not n:
        return 1
    if not s:
        return blink(1, n-1)
    ss = str(s)
    slen = len(ss)
    if slen % 2 == 0:
        a = int(ss[:slen//2])
        b = int(ss[slen//2:])
        return blink(a,n-1)+blink(b,n-1)
    return blink(s*2024, n-1)

def part1(data):
    return sum(blink(i,25) for i in data)

def part2(data):
    return sum(blink(i,75) for i in data)

print("Part 1:", part1(data))
print("Part 2:", part2(data))