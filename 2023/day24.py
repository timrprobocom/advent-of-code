import os
import re
import sys
import collections
from sympy import solve_poly_system, Symbol
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

Point = collections.namedtuple('Point',('x','y','z','dx','dy','dz','m','b'))

nums = re.compile(r"-*\d+")
def get_all_nums(line):
    return tuple(int(i) for i in nums.findall(row))

def find_mbx(x0,y0,dx,dy):
    m = dy/dx
    b = y0 - m * x0
    return (m,b)

vectors = []
for row in data.splitlines():
    n = get_all_nums(row)
    n = n + find_mbx(n[0],n[1],n[3],n[4])
    vectors.append( Point(*n))

def intersect2d(pt1,pt2):
    # Are the lines parallel?
    if pt1.m == pt2.m:
        return (0,0)
    # So, where does m0 x + b0 = m1 x + b1?
    x = (pt2.b-pt1.b)/(pt1.m-pt2.m)
    y = pt1.m*x+pt1.b
    # Did this happen in the past?
    if ((pt1.dx > 0) == (x < pt1.x)) or ((pt2.dx > 0) == (x < pt2.x)):
        return (0,0)
    return (x,y)

def part1(vectors):
    rmin,rmax = (7,28) if TEST else (2*10**14,4*10**14) 
    count = 0
    for i,pt0 in enumerate(vectors):
        for pt1 in vectors[i+1:]:
            x,y = intersect2d(pt0,pt1)
            count += rmin <= x <= rmax and rmin < y < rmax
    return count

def part2(vectors):
    # They're saying there is some line that intersects ALL of the lines at an integer location.
    
    # It's a system of linear equations, right?  For the first three vectors:
    # x + dx*t == vx + vdx * t
    # y + dy*t == vy + vdy * t
    # z + dz*t == vz + vdz * t

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