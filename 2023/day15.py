import os
import sys
import itertools
import functools

test = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test.strip()
else:
    data = open(day+'.txt').read().strip()

DEBUG = 'debug' in sys.argv

# H = (H+N)*17 % 256

@functools.cache
def dohash(s):
    h = 0
    for c in s:
        h = (h+ord(c))*17%256
    return h

def part1(data):
    return sum(dohash(p) for p in data.split(','))

def part2(data):
    boxes = [{} for _ in range(256)]
    for part in data.split(','):
        if part[-1] == '-':
            a = part[:-1]
            box = dohash(a)
            if a in boxes[box]:
                del boxes[box][a]
        else:
            a,b = part.split('=')
            box = dohash(a)
            boxes[box][a] = int(b)
    return sum( i*j*val
        for i,box in enumerate(boxes,1)
        for j,val in enumerate(box.values(),1))

print("Part 1:", part1(data))
print("Part 2:", part2(data))