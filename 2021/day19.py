import sys
import itertools

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = open('test19.txt').readlines()
else:
    data = open('day19.txt').readlines()


scanners = []
for ln in data:
    ln = ln.rstrip()
    if not ln:
        continue
    if ln.startswith( '---' ):
        scanners.append( [] )
    else:
        scanners[-1].append( eval(ln) )


def sub( pta, ptb ):
    return pta[0]-ptb[0], pta[1]-ptb[1], pta[2]-ptb[2]

def add( pta, ptb ):
    return pta[0]+ptb[0], pta[1]+ptb[1], pta[2]+ptb[2]


def rotatex( point ):
    x,y,z = point
    return x, z, -y

def rotatey( point ):
    x,y,z = point
    return z, y, -x

def rotatez( point ):
    x,y,z = point
    return -y, x, z

def flip( point ):
    return rotatex(rotatez(rotatex(point)))

# This returns a vector of the 24 possible rotations of this point.
# I still don't understand why this works.  Why these 24 out of the 64 possibles?

def allrotate( point ):
    for _ in range(2):
        for _ in range(3):
            point = rotatex(point)
            yield point
            for _ in range(3):
                point = rotatez(point)
                yield point
        point = flip(point)

# THis function answers the musical question, for each pair of points
# in the two scan lists, if they lined up, how many other points would
# line up?

def find_matches( scan1, scan2 ):
    set1 = set(scan1)
    for pt1 in scan1:
        for pt2 in scan2:
            # Why is this reversed from what I think?
            delta = sub(pt2,pt1)
            if len(set1.intersection((sub(pt2x,delta) for pt2x in scan2))) >= 12:
                return delta

# Make rotations of all scanners .
# This is a 25x24 array.

def process(scanners):
    rotations = [
        list(zip(*list((list(allrotate(pt)) for pt in scanner)))) for scanner in scanners
    ]

# This is the set of known beacons.

    beacons = set(rotations[0][0])

    placed = { 0: (0, (0,0,0)) }
    while len(placed) < len(rotations):
        for i, scan1 in enumerate(rotations):
            if i in placed:
                continue
            escape = False

            # scan1 is our candidate scanner.

            for j, (rot2,pt2) in placed.items():
                scan2 = rotations[j][rot2]

                # scan2 is a scanner whose position and rotation is now known.

                for possrot in range(24): 

                    # Does this rotation of scan1 line up with scan2?

                    result = find_matches( scan2, scan1[possrot] )
                    if not result:
                        continue
                    if DEBUG:
                        print( "Matched", i, "rot", possrot, "vs", j )

                    # We have a winner.  Add this to the set of knowns.

                    beacons |= {*(
                        sub(sub(pt,result),pt2) for pt in scan1[possrot] 
                    )}

                    placed[i] = ( possrot, add(result,pt2) )
                    escape = True
                    break

                if escape:
                    break

    return beacons, placed

info = process(scanners)

def part1(info):
    return len(info[0])

def part2(info):
    placed = info[1].values()
    # Find the largest distance between any two scanners (not beacons).
    maxx = 0
    for pt0 in placed:
        for pt1 in placed:
            maxx = max( maxx, sum(abs(i) for i in sub(pt0[1],pt1[1])))
    return maxx

print( "Part 1:", part1(info))
print( "Part 2:", part2(info))

