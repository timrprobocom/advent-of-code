import os
import sys
import math
from collections import defaultdict, Counter
from itertools import permutations

test = """\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read()

pairs = [line.split('-') for line in data.splitlines()]

def part1(data):
    connx = defaultdict(set)
    for a,b in data:
        connx[a].add(b)
        connx[b].add(a)
    uniq = set()
    for k,v in connx.items():
        for v1 in v:
            for v2 in v:
                if k[0] == 't' or v1[0] == 't' or v2[0] == 't':
                    if v1 != v2 and k in connx[v2] and v1 in connx[v2]:
                        uniq.add( tuple(sorted((k,v1,v2))))
    return len(uniq)

def part2(data):
    connx = defaultdict(set)
    for a,b in data:
        connx[a].add(a)
        connx[b].add(b)
        connx[a].add(b)
        connx[b].add(a)

    matches = ((a & b) for a,b in permutations(connx.values(),2))
    poss = Counter()
    for m in matches:
        if len(m) < 3:
            continue
        base = ','.join(sorted(set.intersection( *(connx[n] for n in m) )))
        if base:
            poss[base] += 1

    # Return the most common subset found.

    if DEBUG:
        print(poss.most_common())
    return poss.most_common()[0][0]

print("Part 1:", part1(pairs))
print("Part 2:", part2(pairs))
