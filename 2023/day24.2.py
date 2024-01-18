import os
import re
import sys
import math
import numpy as np

test = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

data = test.strip()
data = open('day24.txt').read().strip()


class Point:
    nums = re.compile(r"-*\d+")

    def __init__(self,x,y,z,dx,dy,dz):
        self.pos = np.array((x,y,z))
        self.dt = np.array((dx,dy,dz))

    @classmethod
    def make(cls,row):
        return Point(*tuple(int(i) for i in cls.nums.findall(row)))

    def copy(self):
        p = Point(0,0,0,0,0,0)
        p.pos = self.pos[:]
        p.dt = self.dt[:]
        return p

    def find_mbx(self):
        self.m = self.dy/self.dx
        self.b = self.y - m * self.x

    def subtract(self,pt):
        self.pos -= pt.pos
        self.dt -= pt.dt

    def at(self,t):
        return self.pos + t * self.dt
    
    def __repr__(self):
        x,y,z = self.pos
        dx,dy,dz = self.dt
        return f'<Point {x},{y},{z}, delta={dx},{dy},{dz}>'

vectors = [Point.make(row) for row in data.splitlines()]

# Compute the distance between the two lines at time t.

def distance(p1,p2,t):
    return math.dist( p1.at(t), p2.at(t) )


# Given two points on our first line and a point on a second line, 
# find our plane.

def find_rock_dv():
    p1 = vectors[0]
    p2 = vectors[1]
    p3 = vectors[2]
    sys = []
    sys.append( np.cross(p1.pos-p2.pos,p1.dt-p2.dt) )
    sys.append( np.cross(p2.pos-p3.pos,p2.dt-p3.dt) )
    sys.append( np.cross(p3.pos-p1.pos,p3.dt-p1.dt) )
    sys = np.array(sys)
    print(sys)
    equals = np.array([
        np.dot(sys[0],p2.dt),
        np.dot(sys[1],p3.dt),
        np.dot(sys[2],p1.dt)
    ])
    return np.linalg.solve(np.array(sys), equals).round().astype(int)

def find_mbx(x0,y0,dx,dy):
    m = dy/dx
    b = y0 - m * x0
    return (m,b)

def mxb(pt):
    m = pt.dt[1]/pt.dt[0]
    b = pt.pos[1] - m * pt.pos[0]
    return m,b

def intersect2d(p1m,p1b,p2m,p2b):
    # Are the lines parallel?
    if p1m == p2m:
        return (0,0)
    x = round((p2b-p1b)/(p1m-p2m))
    y = round(p1m*x+p1b)
    return (x,y)


# We know the velocity of the rock.  Now we need the position.

def find_rock_pos(drock):
    p1 = vectors[0].copy()
    p2 = vectors[1].copy()
    p1.dt = p1.dt - drock
    p2.dt = p2.dt - drock
    print(p1,p2)

    p1m,p1b = find_mbx(p1.pos[0],p1.pos[1],p1.dt[0],p1.dt[1])
    p2m,p2b = find_mbx(p2.pos[0],p2.pos[1],p2.dt[0],p2.dt[1])
# So, hailstones 0 and 1 intersect in x, y here:
    x,y = intersect2d(p1m,p1b,p2m,p2b)

# At these times:
    ta = int((x - p1.pos[0]) / p1.dt[0])
    tb = int((x - p2.pos[0]) / p2.dt[0])

# Working backwards from the real hailstone 0:
    pt0 = vectors[0]
    return pt0.pos + ta * (pt0.dt - drock)


drock = find_rock_dv()
print(drock)
prock = find_rock_pos(drock)
print(sum(prock))


#doplot()
#print(pts)


