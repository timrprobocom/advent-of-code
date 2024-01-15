import os
import re
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

nums = re.compile(r"-*\d+")

class Point:
    def __init__(self,x,y,z,dx,dy,dz):
        self.pos = np.array((x,y,z))
        self.dt = np.array((dx,dy,dz))

    @classmethod
    def make(self,row):
        return Point(*tuple(int(i) for i in nums.findall(row)))

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

print(vectors)

# Compute the distance between the two lines at time t.

def distance(p1,p2,t):
    return math.dist( p1.at(t), p2.at(t) )

# We want to know the integral times t1,t2 where the distance between
# p1.at(t1) and p2.at(t2) equals (t1-t2)*k.  Right?

def attempt1():
    base = Point(24,13,10,-3,1,2) # At time 5,3,4
    p1,p2,p3 = vectors[0:3]
    for t in range(50):
        print(t, 
            math.dist(base.at(t),p1.at(t)),
            math.dist(base.at(t),p2.at(t)),
            math.dist(base.at(t),p3.at(t))
        )

    # Distance traveled by our throw in one t
    print(math.sqrt(-3*-3+1*1+2*2))     # 3.7

    print(math.dist(p1.at(5),p2.at(3))) # 7.4
    print(math.dist(p1.at(5),p3.at(4))) # 3.7
    print(math.dist(p2.at(3),p3.at(4))) # 3.7



# Given two points on our first line and a point on a second line, 
# find our plane.

def find_plane_3pt(pt1,pt2):
    p0 = pt1.pos
    p1 = p0 + pt1.dt
    p2 = pt2.pos

    v1 = p2-p0
    v2 = p2-p1
    normal = np.cross(v1,v2)
    normal = normal / math.gcd(*normal)
    print("Normal vector",normal)
    return normal, np.dot(normal,p0)

def find_plane(pt1,pt2):
    normal = np.cross(pt1.dt,pt2.dt)
    print("Normal vector",normal)
    d0 = np.dot(normal, pt1.pos)
    d1 = np.dot(normal, pt2.pos)
    d2 = np.dot(normal, pt1.at(1))
    txt = f"{normal[0]}x + {normal[1]}y + {normal[2]}z ="
    print( txt, d0 )
    print( txt, d1 )
    print( txt, d2 )
    return normal

def plot_plane(ax,pt1,pt2):
#    normal = find_plane(pt1,pt2)
    normal = pt1.dt
    point = pt1.pos
    d = -point.dot(normal)
    xx, yy = np.meshgrid(range(50), range(50))
    z = (-normal[0] * xx - normal[1] * yy - d) / normal[2]

    ax.plot_surface(xx, yy, z, alpha=0.2)

def intersect( normal, point, line ):
    pt = point.pos
    pt0 = line.pos
    dd0 = line.dt
    a = (pt-pt0).dot(normal)
    b = dd0.dot(normal)
    d = a/b
    print( "intersects at t=",d)
    return pt0 + d*dd0

# Try the reference frame shift.

def attempt2():
    p1,p2,p3,_ = vectors[:4]
    p2.subtract(p1)
    p3.subtract(p1)
    p1 = Point(0,0,0,0,0,0)
    n2 = p2.dt
    n3 = p3.dt
    n2 = find_plane_3pt(p2,p1)[0]
    n3 = find_plane_3pt(p3,p1)[0]
    n4 = np.cross(n2,n3) / 8
    print("before",n4)
    n4 += vectors[0].dt
    print(n2)
    print(n3)
    print(n4)

# Make some lines.

    ax = plt.subplot(projection='3d')
    t = np.array([0,1,0,2,0,3,0,4,0,5,0,6,0,7,0,8,0,9,0,10])
    for n in (n2,n3,n4):
        x = t * n[0]
        y = t * n[1]
        z = t * n[2]
        plt.plot( x, y, z )
    plt.show()

def doplot():
    p0,p1,p2,p3 = vectors[:4]
    p1.subtract(p0)
    p2.subtract(p0)
    p3.subtract(p0)
    p0 = Point(0,0,0,0,0,0)
#    normal = find_plane_3pt(p1,p0)[0]
#    pts = [intersect(normal,p0,v) for v in vectors[1:]]
    ax = plt.subplot(projection='3d')
    plot_plane(ax, p1, p0 )
    plot_plane(ax, p2, p0 )
    plot_plane(ax, p3, p0 )
#    ax.scatter( *pts[0], color='green')
#    ax.scatter( *pts[1], color='red')
#    ax.scatter( *pts[2], color='blue')
    plt.show()

# If three vectors are coplanar, the triple scalar product is 0.
def attempt3():
    dr = np.array((-3,1,2))
    p1 = vectors[0]
    p2 = vectors[1]
    p3 = vectors[2]

    v1 = p1.pos-p2.pos
    v2 = p1.dt-p2.dt
    v3 = p1.dt-dr
    print(v1,v2,v3)
    r = np.dot(v3,np.cross(v1,v2))
    print(r)

    v1 = p2.pos-p1.pos
    v2 = p1.dt-dr
    v3 = p2.dt-dr
    r = np.dot(v1,np.cross(v2,v3))
    print(r)

def attempt4():
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
    return np.linalg.solve(np.array(sys), equals)

drock = attempt4()
print(drock)

#doplot()
#print(pts)

def printthem():
    print(find_plane_3pt(vectors[0],vectors[1]))
    print(find_plane(vectors[0],vectors[1]))
    print(find_plane_3pt(vectors[0],vectors[2]))
    print(find_plane(vectors[0],vectors[2]))
    print(find_plane_3pt(vectors[0],vectors[3]))

