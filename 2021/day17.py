import sys
import itertools
import re

test = "target area: x=20..30, y=-10..-5"
test = (20,30,-10,-5)

live = "target area: x=156..202, y=-110..-69"
live = (156,202,-110,-69)

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
else:
    data = live

datax = range(data[0],data[1]+1)
datay = range(data[2],data[3]+1)


# What's the minimum X velocity?

minx = 0
mustx = data[0]
while mustx > 0:
    minx += 1
    mustx -= minx

def sgn(x):
    return -1 if x < 0 else 1 if x > 0 else 0

# At each step
#x velocity step by 1 towards 0
#y velocity decreases by 1

def launch( vel ):
    pos = [0,0]
    maxy = 0
    while True:
        pos[0] += vel[0]
        pos[1] += vel[1]
        if DEBUG:
            print(pos)
        if pos[0] in datax and pos[1] in datay:
            return maxy
        if pos[0] > data[1] or pos[1] < data[2]:
            return None
        maxy = max(maxy, pos[1])
        vel = (vel[0]-sgn(vel[0]),vel[1]-1)

def part1():
    maxdata = (0,0,0)
    count = 0
    for y in range(-150,150):
        for x in range(minx, data[1]+1):
            vel = (x,y)
            if DEBUG:
                print("*****", vel )
            v = launch( vel )
            if v is not None:
                count += 1
                if v > maxdata[1]:
                    if DEBUG:
                        print(vel,v)
                    maxdata = (vel,v)
    print(maxdata, count)
    return maxdata[1], count

# Part 1 with math.  When aiming up, you will always come back to x=0
# with vy = -vy0, and the max will hit the bottom of the zone at the
# next step.  So, if bottom of the box is -10, you need initial
# velocity 9, and the highest is sum(1..9), which is y1(y1+1)/2.

print( "Math 1:", data[2]*(data[2]+1)//2)

info = part1()
print( "Part 1:", info[0] )
print( "Part 2:", info[1] )

