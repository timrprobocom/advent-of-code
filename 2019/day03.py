import sys

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv


test =  [ 'R75,D30,R83,U83,L12,D49,R71,U7,L72','U62,R66,U55,R34,D71,R55,D58,R83'] #= distance 159  and  610
test2 = [ 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51','U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'] # = distance 135  and  410

live = open('day03.txt').read().splitlines()

if TEST:
    data = test
else:
    data = live

deltas = {
    'R': 1,
    'L': -1,
    'U': -1j,
    'D': 1j
}

# This was the wrong tactic.

def find_extent( s1 ):
    pt = 0
    minptx, minpty = (999,999)
    maxptx, maxpty = (0,0)
    steps = 0
    for move in s1.split(','):
        val = int(move[1:])
        steps += val
        pt += deltas[move[0]] * val
        if pt.real < minptx: minptx = pt.real
        if pt.real > maxptx: maxptx = pt.real
        if pt.imag < minpty: minpty = pt.imag
        if pt.imag > maxpty: maxpty = pt.imag
    return steps,(minptx,minpty),(maxptx,maxpty)

# Construct the set of all points visited on this path.

def makepath( s1 ):
    steps = {}
    pt = 0
    dist = 0
    for move in s1.split(','):
        d = deltas[move[0]]
        val = int(move[1:])
        for v in range(val):
            dist += 1
            pt += d
            if pt not in steps:
                steps[pt] = dist
    return steps

# Return Manhattan distance between two points.

def mandist( p1, p2 ):
    return abs(p1.real-p2.real) + abs(p1.imag-p2.imag)


# Construct the paths.
p1 = makepath(data[0])
p2 = makepath(data[1])
if DEBUG:
    print(p1)
    print(p2)

# Extract the keys, which are the points themselves.
ps1 = set(p1.keys())
ps2 = set(p2.keys())

# Find the intersection.
inx = ps1.intersection(ps2)
if DEBUG:
    print(inx)

# For part 1, find the minimum distance from 0,0.
dist = min(int(mandist(0,pt)) for pt in inx)
print( "Part 1:", dist )

# For part 2, find the minimum total steps taken.
sigdist = min(p1[pt]+p2[pt] for pt in inx)
print( "Part 2:", sigdist )

