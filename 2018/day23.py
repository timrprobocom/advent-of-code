import sys
import re

bots = []
expr = r"pos=<(-?\d*),(-?\d*),(-?\d*)>, r=(\d*)$"
maxr = 0
maxbot = None
for ln in sys.stdin:
    ln = ln.strip()
    m = re.match( expr, ln )
    bots.append( list(int(k) for k in m.groups()) )
    if bots[-1][3] > maxr:
        maxr = bots[-1][3]
        maxbot = bots[-1]

print( maxr )
print( "X range:", min(x[0] for x in bots), ",", max(x[0] for x in bots) )
print( "Y range:", min(x[1] for x in bots), ",", max(x[1] for x in bots) )
print( "Z range:", min(x[2] for x in bots), ",", max(x[2] for x in bots) )

def mandist( a, b ):
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])

count = 0
for x,y,z,r in bots:
    if mandist( (x,y,z), maxbot ) <= maxr:
        count += 1
print( "Part 1:", count )

# How to do this optimization problem?
# Distances are too vast.
# We can't paint a bitmap.
# Start out in 100x100 array?

def inrange( bot, pt ):
    return mandist( bot, pt ) <= bot[-1]

def divide( bots, factor ):
    round = factor//2
    return list(((x+round)//factor,(y+round)//factor,(z+round)//factor,(r+round)//factor) for x,y,z,r in bots)

def check_at_scale( scale, centroid ):
    print( "Checking at", scale )
    subbots = divide( bots, scale )
    cx,cy,cz = centroid

    maxloc = (0,0,0)
    maxcnt = 0
    for z in range(-12,12):
        for y in range(-12,12):
            for x in range(-12,12):
                cnt = sum(1 for bot in subbots if inrange(bot,(cx+x,cy+y,cz+z)))
                if cnt > maxcnt:
                    maxcnt = cnt
                    maxloc = (cx+x,cy+y,cz+z)
                    print( maxcnt,'@', maxloc )
    return maxloc

scale = 10000000
pt = (0,0,0)
while scale > 0:
    pt = check_at_scale( scale, pt )
    print( "Best result at", scale, pt )
    if scale == 1:
        break
    scale //= 10
    pt = tuple(x*10 for x in pt)
print( "Part 2:", sum(abs(k) for k in pt) )
