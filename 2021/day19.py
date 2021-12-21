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

# This returns a vector of the 24 possible rotations of this point.
# Move the "facing" direction through all 6 points, then rotate around
# that axis four times.

def allrotate( point ):
    for direction in (
        rotatex, rotatex, rotatex, rotatez, # now pointing up / down
        rotatey, rotatey, rotatey, rotatex, # now pointing back / front
        rotatez, rotatez, rotatez, rotatey  # now pointing left / right
    ) * 2:
        yield point
        point = direction(point)


# This function answers the musical question, for each pair of points
# in the two scan lists, if they lined up, how many other points would
# line up?

def find_matches( scan1, scan2 ):
    set1 = set(scan1)
    for pt1 in scan1:
        for pt2 in scan2:
            delta = sub(pt2,pt1)
            if len(set1.intersection((sub(pt2x,delta) for pt2x in scan2))) >= 12:
                return delta

def process(scanners):
    # Make all rotations of all scanner readings.
    # This is a 25x24 array.

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
                    # We shift scan1 to match the coords of scan2, then
                    # shift that to our master coords.

                    beacons |= {*(
                        sub(sub(pt,result),pt2) for pt in scan1[possrot] 
                    )}

                    placed[i] = ( possrot, add(result,pt2) )
                    escape = True
                    break

                if escape:
                    break

    return beacons, placed

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

def visoalize(beacons, placed):
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits import mplot3d

    beacons = np.array(list(beacons))

    scanners = -np.array( [k[1] for k in placed.values()] )

    ax = plt.axes(projection='3d')
    ax.scatter3D( beacons[:,0], beacons[:,1], beacons[:,2], c='blue', marker='o' )
    ax.scatter3D( scanners[:,0], scanners[:,1], scanners[:,2], c='red', marker='^' )
    plt.show()

info = process(scanners)

if 'vis' in sys.argv:
    visoalize(*info)
    sys.exit(0)

print( "Part 1:", part1(info))
print( "Part 2:", part2(info))
