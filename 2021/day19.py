import sys
import itertools
from collections import defaultdict

DEBUG = 'debug' in sys.argv


# This returns all 24 possible rotations of this point.

def rot(v):
    # This is a rotation in x.
    rotx = lambda a, b, c: (a, c, -b)
    # This is a rotation in z.
    rotz = lambda a, b, c: (-b, a, c)

    # 2 x 4 x 3. 

    a = []
    for _ in range(2):
        for _ in range(3):
            v = rotx(*v)
            a.append(v)
            for _ in range(3):
                v = rotz(*v)
                a.append(v)
        v = rotx(*rotz(*rotx(*v)))
    return a


def find_matches(aa, bb):
    ptsa = set(aa)
    # For all pairs of points in the two sets...
    for (a, b, c), (d, e, f) in itertools.product(aa, bb):
        # If we assume these points line up, how many other points line up? 
        # If there are at least 12. then these two overlap and we know the 
        # delta between them.
        #
        # Why == 12?  It didn't say ONLY 12.  It said AT LEAST 12.

        if len(ptsa.intersection((x - d + a, y - e + b, z - f + c) for x, y, z in bb)) >= 12:
            return d - a, e - b, f - c


def crunch(f):
    #  This is what I called "rotations".  All possible rotations of all scanners.
    scanners = [
        [*zip(*[rot([int(j) for j in i.split(",")]) for i in x.splitlines()[1:]])]
        for x in f.read().strip().split("\n\n")
    ]

    # This is the rotation needed for scanner n.
    rotates = {0: 0}
    # This is the offset needed for scanner n.
    offsets = {0: (0, 0, 0)}

    nt = defaultdict(set)

    # Beacons holds the set of known beacons.

    beacons = set(scanners[0][0])

    # We are trying to find the rotation factors for all of the scanners.

    while len(rotates) < len(scanners):
        print( rotates, offsets, nt )

        # For every scanner that we haven't placed yet.

        for i, sci in enumerate(scanners):
            if i in rotates:
                continue

            # For every scanner where we know the rotation that hasn't already
            # matched with us...

            for j, jrotidx in rotates.items():
                if j in nt[i]:
                    continue

                # Fetch the known rotation and offset for this scanner.

                scj = scanners[j][jrotidx]
                axx, ayy, azz = offsets[j]

                # For each rotation.

                for rot_idx in range(24):
                    
                    # Does this one line up with the current scanner?

                    res = find_matches(scj, sci[rot_idx])
                    if res is None:
                        continue

                    # Add this set to the set of known beacons.

                    ox, oy, oz = res
                    beacons |= {(x - ox - axx, y - oy - ayy, z - oz - azz) for x, y, z in sci[rot_idx]}

                    # Remember this info.

                    rotates[i] = rot_idx
                    offsets[i] = ox + axx, oy + ayy, oz + azz
                    break
                else:
                    continue
                break
            else:
                nt[i].add(j)
                continue
            break

    return rotates, offsets, beacons


def part1(data):
    return len(data[2])

def part2(data):
    offsets = data[1]
    return max(
        sum(abs(i - j) for i, j in zip(offsets[a], offsets[b]))
        for a, b in itertools.product(range(len(offsets)), repeat=2)
    )


if 'test' in sys.argv:
    name = 'test19.txt'
else:
    name = 'day19.txt'

data = crunch(open(name))
print("Part 1:", part1(data))
print("Part 2:", part2(data))
