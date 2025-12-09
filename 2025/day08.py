import os
import sys
from collections import defaultdict, Counter
import itertools

test = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = open(day+'.txt').read()

data = list(tuple(int(k) for k in ln.split(',')) for ln in data.splitlines())

def hash(p):
    return (p[0]<<18)|p[1]

# This is actually distance squared, but that's OK here.

def dist3d(pt1,pt2):
    return (pt2[0]-pt1[0])**2 + (pt2[1]-pt1[1])**2 + (pt2[2]-pt1[2])**2

# This takes a second.  We're doing a million distance calcs.  numpy?

distances = [(dist3d(a,b),hash(a),hash(b)) for a,b in itertools.combinations(data, 2)]
distances.sort()

# These could easily be combined.

def part1(data, dists):
    # We assign each junction to a circuit.
    circuit = {hash(j):i for i,j in enumerate(data)}

    limit = 10 if TEST else 1000
    for _,a,b in dists[:limit]:
        bindex = circuit[b]
        for c in circuit:
            if circuit[c] == bindex:
                circuit[c] = circuit[a]

    counts = Counter(circuit.values()).most_common(3)
    return counts[0][1] * counts[1][1] * counts[2][1]

def part2(data, dists):
    # We assign each junction to a circuit.
    circuit = {hash(j):i for i,j in enumerate(data)}

    # Keep combining circuits until there is only 1.

    for _,a,b in dists:
        bindex = circuit[b]
        for c in circuit:
            if circuit[c] == bindex:
                circuit[c] = circuit[a]

        if len(set(circuit.values())) == 1:
            return (a>>18)*(b>>18)

print("Part 1:", part1(data, distances))
print("Part 2:", part2(data, distances))
