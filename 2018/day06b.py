
#
#
# For each point, find the region within manhattan 10000.
# That's a diamond.
# Store just the start,end for each line? 20000?
#
# Intersect all the diamonds.
# What's the area of the remainder?

# Find the distance from each point in the grid to each point in the 
#

# Start with 10x10.
import sys

test = (
    (1, 1),
    (1, 6),
    (8, 3),
    (3, 4),
    (5, 5),
    (8, 9)
)

live = tuple(tuple(int(p) for p in ln.split(' ')) for ln in open('day06.txt').readlines())

data = test
TARGET = 32
MAXD = 25

data = live
TARGET = 10000
MAXD = 500

def ham(x0,y0,x1,y1):
    return abs(x0-x1) + abs(y0-y1)

knt = 0
for y in range(-MAXD,MAXD):
    sys.stdout.write('%d\r' % y )
    sys.stdout.flush()
    for x in range(-MAXD,MAXD):
        sumh = 0
        for px,py in data:
            sumh += ham(x,y,px,py)
            if sumh >= TARGET:
                break
        if sumh < TARGET:
            print x,y
            knt += 1

print knt
