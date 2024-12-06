import os
import sys
from collections import defaultdict
from functools import cmp_to_key
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

def compare(a,b):
    return 0 if a == b else 1 if b in before[a] else -1

def do_sort(case):
    return sorted(case, key=cmp_to_key(compare))

sum1 = 0
sum2 = 0

for case in cases:
    order = do_sort(case)
    if order == case:
        sum1 += case[len(case)//2]
    else:
        sum2 += order[len(order)//2]

print("Part 1:", sum1)
print("Part 2:", sum2)
