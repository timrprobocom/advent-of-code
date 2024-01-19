import os
import re
import sys
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

if TEST:
    data = test.strip()
else:
    data = open(day+'.txt').read().strip()


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
        return find_mbx(self.pos[0],self.pos[1],self.dt[0],self.dt[1])

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

def find_mbx(x0,y0,dx,dy):
    m = dy/dx
    b = y0 - m * x0
    return (m,b)

def intersect2d(p1m,p1b,p2m,p2b):
    # Are the lines parallel?
    if p1m == p2m:
        return (0,0)
    x = round((p2b-p1b)/(p1m-p2m))
    y = round(p1m*x+p1b)
    return (x,y)

def in_the_future(pt1,x,y):
    # Did this happen in the future?
    return (pt1.dt[0] < 0) == (x < pt1.pos[0])

def part1(vectors):
    rmin,rmax = (7,28) if TEST else (2*10**14,4*10**14) 
    count = 0
    for i,pt0 in enumerate(vectors):
        p1m,p1b = pt0.find_mbx()
        for pt1 in vectors[i+1:]:
            p2m,p2b = pt1.find_mbx()
            x,y = intersect2d(p1m,p1b,p2m,p2b)
            if in_the_future(pt0,x,y) and in_the_future(pt1,x,y):
                count += rmin <= x <= rmax and rmin < y < rmax
    return count

# Find the velocity of the rock.

# Here's an explanation, as best as I can.
#
# Call the rock's location r, and it's velocity dr.  For every hailstone s, 
# there must be a time t so that
#   r + dr*t = s * ds*t
# Which means
#   r = s + (ds-dr) * t
# That means if we shift our framework relative to the rock's velocity,
# every ray passes through that point r.  That makes for some nice triangles.
#
# That means that the vectors (s2-s1), (ds1-dr) and (ds2-dr) are all coplanar,
# in the plane of the triangle that contains s1, s2, and r.  (The two velocity
# vectors don't make up the other legs, but they are in the same direction.)
# This is where I went wrong with my first analysis -- I was using vectors
# that were not coplanar.
#
# By rearranging, it also means that (s2-s1), (ds1-ds2), and (ds2-dr) are 
# coplanar.  If we look up the Wikipedia definition of a "triple scalar
# product", we find definitions that let us construct a system of three
# linear equations that produce dr.
#
# Believe it or not.

def find_rock_vel(vectors):
    p1 = vectors[0]
    p2 = vectors[1]
    p3 = vectors[2]
    sys = np.array([
        np.cross(p1.pos-p2.pos,p1.dt-p2.dt),
        np.cross(p2.pos-p3.pos,p2.dt-p3.dt),
        np.cross(p3.pos-p1.pos,p3.dt-p1.dt)
    ])
    if DEBUG:
        print(sys)
    equals = np.array([
        np.dot(sys[0],p2.dt),
        np.dot(sys[1],p3.dt),
        np.dot(sys[2],p1.dt)
    ])
    return np.linalg.solve(np.array(sys), equals).round().astype(int)

# Given the velocity of the rock, find the initial position.

# As above, we warp space by shifting the reference frame so that the rock's 
# velocity is zero.  That way, all of the hailstones will pass through a 
# single point.  If we can find the point where two of the hailstones
# cross, since the rock's velocity is zero, that must be the point where
# the rock started.

# It's not easy to find the intersection of two 3D lines, but if the vectors
# intersect in 2D (and we know how to do that), it's pretty safe to assume 
# they cross in 3D.

def find_rock_pos(vectors, drock):
    p1 = vectors[0].copy()
    p2 = vectors[1].copy()
    p1.dt = p1.dt - drock
    p2.dt = p2.dt - drock

    p1m,p1b = find_mbx(p1.pos[0],p1.pos[1],p1.dt[0],p1.dt[1])
    p2m,p2b = find_mbx(p2.pos[0],p2.pos[1],p2.dt[0],p2.dt[1])

    # So, hailstones 0 and 1 intersect in x, y here:
    x,y = intersect2d(p1m,p1b,p2m,p2b)

    # At these times:
    ta = int((x - p1.pos[0]) / p1.dt[0])
    tb = int((x - p2.pos[0]) / p2.dt[0])

    # And what is that location in 3D?
    return p1.at(ta)

def part2(vectors):
    drock = find_rock_vel(vectors)
    prock = find_rock_pos(vectors, drock)
    return sum(prock)

def part2b(vectors):
    #from sympy import solve_poly_system, Symbol

    # They're saying there is some line that intersects ALL of the lines at an integer location.
    
    # It's a system of non-linear equations.  For the first three vectors:
    # x + dx * t == vx + vdx * t
    # y + dy * t == vy + vdy * t
    # z + dz * t == vz + vdz * t

    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    dx = Symbol('dx')
    dy = Symbol('dy')
    dz = Symbol('dz')

    equations = []
    for i,v1 in enumerate(vectors[0:3]):
        t = Symbol(f"t{i}")
        equations.append( x + dx * t - v1.x - v1.dx * t )
        equations.append( y + dy * t - v1.y - v1.dy * t )
        equations.append( z + dz * t - v1.z - v1.dz * t )
    result = solve_poly_system(equations)
    if DEBUG:
        print(result)
    return sum(result[0][0:3])

print("Part 1:", part1(vectors))
print("Part 2:", part2(vectors))
