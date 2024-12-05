import os
import sys
from collections import defaultdict
from pprint import pprint

test = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

# Not sure why the topological sort didn't work for this one.

before = defaultdict(set)
cases = []
for line in data:
    if not line:
        continue
    if line[2] == '|':
        a,b = (int(k) for k in line.split('|'))
        before[b].add(a)
    else:
        cases.append( list(int(k) for k in line.split(',')))

def is_ordered(case):
    remain = set(case)
    for page in case:
        remain.remove(page)
        if remain & before[page]:
            return False
    return True

def do_sort(case):
    for i,_ in enumerate(case):
        remain = set(case[i:])
        for j,p2 in enumerate(case):
            if i <= j:
                if not before[p2] & remain:
                    case[i],case[j] = case[j],case[i]
                    break

def part1(cases):
    sumx = 0
    for case in cases:
        if is_ordered(case):
            sumx += case[len(case)//2]
    return sumx

def part2(cases):
    sumx = 0
    for case in cases:
        if not is_ordered(case):
            do_sort(case)
            sumx += case[len(case)//2]
    return sumx

print("Part 1:", part1(cases))
print("Part 2:", part2(cases))
