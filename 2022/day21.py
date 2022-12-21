import sys
from collections import deque

test = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day21.txt').readlines()

DEBUG = 'debug' in sys.argv

def parse(data):
    known = {}
    unknown = {}
    for line in data:
        parts = line.strip().split()
        if len(parts) == 2:
            known[parts[0][:-1]] = int(parts[1])
        else:
            unknown[parts[0][:-1]] = parts[1:]
    return known, unknown


def lookup(name):
    if name in known:
        return known[name]
    a,op,b = unknown[name]
    if op == '+':
        return lookup(a)+lookup(b)
    elif op == '-':
        return lookup(a)-lookup(b)
    elif op == '*':
        return lookup(a)*lookup(b)
    elif op == '/':
        return lookup(a)//lookup(b)

def part1(data):
    return lookup('root')

def part2(data):
    left, _, right = unknown['root']
    R = lookup(right)
    
    base = 10000
    incr = 10000
    while True:
        known['humn'] = base
        print(base)
        L = lookup(left)
        if L == R:
            return base
        if L > R:
            base *= 10 
        else:
            break

    base //= 10
    incr = base
    while True:
        known['humn'] = base
        L = lookup(left)
        if L == R:
            break
        if L > R:
            base += incr
        else:
            base -= incr
            incr //= 10

    return base

known, unknown = parse(data)
print("Part 1:", part1(data))
if 'test' not in sys.argv:
    known, unknown = parse(data)
    print("Part 2:", part2(data))
