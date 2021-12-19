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

#print( scanners )
#print(len(scanners))
#print(len(scanners[0]))
#sys.exit(0)

def sub( pta, ptb ):
    return pta[0]-ptb[0], pta[1]-ptb[1], pta[2]-ptb[2]

# So.  Compute all deltas and sort them?

def deltas( points ):
    delta = []
    delta = [sub(pa,pb) for pa,pb in itertools.combinations(points, 2)]
    return set(delta)

#    |cos θ   −sin θ   0| |x|   |x cos θ − y sin θ|   |x'|
#    |sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|
#    |  0       0      1| |z|   |        z        |   |z'|
#around the Y-axis would be
#
#    | cos θ    0   sin θ| |x|   | x cos θ + z sin θ|   |x'|
#    |   0      1       0| |y| = |         y        | = |y'|
#    |−sin θ    0   cos θ| |z|   |−x sin θ + z cos θ|   |z'|
#around the X-axis would be
#
#    |1     0           0| |x|   |        x        |   |x'|
#    |0   cos θ    −sin θ| |y| = |y cos θ − z sin θ| = |y'|
#    |0   sin θ     cos θ| |z|   |y sin θ + z cos θ|   |z'|

# We will need a "rotate".
# There are 24 rotations?
# We can rotate around any of the 3 axes, up to 4 times.
#
# Rotate on Y axis:
# 0   [ +x, +y, +z ]
# 1   [ +z, +y, -x ]
# 2   { -x, +y, -z ]
# 3   [ -z, +y, +x ]
# Rotate on X axis:
# 0   [ +x, +y, +z ]
# 1   [ +x, -z, +y ]
# 2   [ +x, -y, -z ]
# 3   [ +x, +z, -y ]
# Rotate on Z axis:
# 0   [ +x, +y, +z ]
# 1   [ -y, +x, +z ]
# 2   [ -x, -y, +z ]
# 3   [ +y, -x, +z ]

# And then there are combinations of those. 4*4*4 = 64 rotations, many are duplicates.

def rotatex( points, steps):
    x,y,z = points
    for i in range(steps):
        x,y,z = z,y,-x
    return (x,y,z)

def rotatey( points, steps ):
    x,y,z = points
    for i in range(steps):
        x,y,z = x,-z,y
    return (x,y,z)

def rotatez( points, steps ):
    x,y,z = points
    for i in range(steps):
        x,y,z = -y, x, z
    return (x,y,z)

def dorotate( pt, guide ):
    posn = [abs(i)-1 for i in guide]
    sign = [-1 if i < 0 else 1 for i in guide]
    return (sign[0]*pt[posn[0]], sign[1]*pt[posn[1]], sign[2]*pt[posn[2]])

def get_all_rotations():
    pt = (1,2,3)
    accum = set([pt])
    for dx in range(0,4):
        pt = rotatex(pt,dx)
        for dy in range(0,4):
            pt = rotatex(pt,dy)
            for dz in range(0,4):
                pt = rotatez(pt,dz)
                accum.add( pt )
    return accum

allrot = get_all_rotations()

# Make rotations of all scanners .

rotations = []
for scanner in scanners:
    rotations = [[dorotate(point,rot) for point in scanner] for rot in allrot]
print(rotations)

print( "Total", sum(len(s) for s in scanners))

def choices(n):
    ch = [0]*n
    while True:
        yield ch[:]
        carry = 1
        for i in range(len(ch)):
            ch[i] += carry
            carry = 0
            if ch[i] > 15:
                ch[i] = 0
                carry = 1
        if carry:
            break

# For each scanner > 1
#  For each rotation
#   combine rotation(scanner][rotation]


minx = 999999
print(len(rotations[0][0]))
for pick in choices(len(scanners)-1):
    delta1 = deltas(scanners[0])
    for i,p in enumerate(pick):
        delta1 = delta1.union( rotations[i+1][p] )
        print(i,p,len(delta1))
        if len(delta1) >= minx:
            continue
    if len(delta1) < minx:
        minx = len(delta1)
        print(0, pick, len(delta1))
sys.exit(0)










#print( "Part 1:", part1(data) )
#print( "Part 2:", part2(data) )

