import ast
import sys
from functools import cmp_to_key

test = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [s.rstrip() for s in open('day13.txt').readlines()]

DEBUG = 'debug' in sys.argv

def makedata(data):
    d2 = []
    left = None
    for line in data:
        if not line:
            d2.append((left,right))
            left = right = None
        else:
            if left is None:
                left = ast.literal_eval(line)
            else:
                right = ast.literal_eval(line)
    d2.append((left,right))
    return d2

data = makedata(data)

def cmp(l,r):
    if l < r:
        return 1
    if l > r:
        return -1
    return 0

def compare(left,right):
    if isinstance(left,int):
        if isinstance(right,int):
            return cmp(left,right)
        return compare([left],right)
    if isinstance(right,int):
        return compare(left,[right])

    for i in range(min(len(left),len(right))):
        res = compare(left[i],right[i])
        if res != 0:
            return res

    return cmp(len(left),len(right))

def part1(data):
    return sum(i+1 for i,(left,right) in enumerate(data) if compare(left,right)==1)

def part2(data):
    combine = [[2],[6]]
    for row in data:
        combine.extend(row)
    combine.sort(key=cmp_to_key(compare),reverse=True)
    mult = 1
    for i,row in enumerate(combine):
        if row in ([2],[6]):
            mult *= i+1
    return mult
    
print("Part 1:", part1(data))
print("Part 2:", part2(data))
