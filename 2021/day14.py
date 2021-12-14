import sys
from collections import Counter
import itertools

test = """\
NNCB

BB -> N
BC -> B
BH -> H
BN -> B
CB -> H
CC -> N
CH -> B
CN -> C
HB -> C
HC -> B
HH -> N
HN -> C
NB -> B
NC -> B
NH -> C
NN -> C"""

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day14.txt').readlines()

polymer = data[0].rstrip()

xform = {}
for row in data[2:]:
    a,b = row.rstrip().split(' -> ')
    xform[a] = (a[0]+b,b+a[1])

def generation(counts, xform):
    newcounts = Counter()
    for k,v in xform.items():
        newcounts[v[0]] += counts[k]
        newcounts[v[1]] += counts[k]
    return newcounts

def part(polymer, xform, gens):
    # Store pairs?
    counts = Counter()
    for a,b in zip(polymer[:-1],polymer[1:]):
        counts[a+b] += 1
    for _ in range(gens):
        counts = generation(counts, xform)

    counter = Counter()
    counter[polymer[0]] = 1
    counter[polymer[-1]] = 1
    for k,v in counts.items():
        counter[k[0]] += v
        counter[k[1]] += v
        
    a = max(counter.values())//2
    b = min(counter.values())//2
    return a-b

print("Part 1:", part(polymer,xform,10)) # 3009
print("Part 2:", part(polymer,xform,40)) # 3459822539451
