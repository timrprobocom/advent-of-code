
import os
import sys
import copy
import time
import itertools



# moon position (x,y,z)
# First apply gravity to update velocity
# Then update position by applying velocity
# First/second derivatives.
#
# Gravity:
#   Each velocity bumps by +1/-1
# 

class Moon(object):
    def __init__(self,x,y,z):
        self.pos = [x,y,z]
        self.vel = [0,0,0]

    def apply(self):
        self.pos = list(a+b for a,b in zip(self.pos,self.vel))

    def pot(self):
        return sum(abs(k) for k in self.pos)

    def kin(self):
        return sum(abs(k) for k in self.vel)

    def __repr__(self):
        return "pos<%d,%d,%d> vel<%d,%d,%d>" % tuple(self.pos+self.vel)

# I made so many typos in this data (missing minus signs) that it would
# have been better to write a parser for their <...> formatting.

test = (
  (-1,0,2),
  (2,-10,-7),
  (4,-8,8),
  (3,5,-1)
)

test2 = (
  (-8, -10, 0),
  (5, 5, 10),
  (2, -7, 3),
  (9, -8, -3)
)

real = (
  (-8,-18,6),
  (-11,-14,4),
  (8,-3,-10),
  (-2,-16,1)
)

def makemoons( pts ):
    return tuple( Moon(*pt) for pt in pts )

# Part 1

def energy(system):
    return sum(m.pot() * m.kin() for m in system)

def sign(a,b):
    if a<b:
        return 1
    elif a>b:
        return -1
    else:
        return 0

def step(system):
    # Apply gravity
    for m1,m2 in itertools.combinations(system,2):
        for axis in range(3):
            m1.vel[axis] += sign(m1.pos[axis],m2.pos[axis])
            m2.vel[axis] -= sign(m1.pos[axis],m2.pos[axis])
    # Apply velocity.
    for m1 in system:
        m1.apply()

def run(system, n):
    for m1 in system:
        print( m1 )
    for i in range(n):
        step( system )
    return energy( system )

def part1():
#    run( makemoons(test), 10 )
#    run( makemoons(test2), 100 )
    print( "Part 1: ", run( makemoons(real), 1000 ))

# Part 2.

def getstate(system,axis):
    return tuple( m.vel[axis] for m in system )

def gcd(x,y):
    while y:
        x,y = y,x%y
    return x

def lcm(x,y):
    return x * y // gcd(x,y)

def lcm3(x,y,z):
    return lcm(lcm(x,y),z)

# This is my third algorithm.  The velocities all reach zero at
# the halfway point, so we can look for that without tracking the
# previous positions.  This is 60% faster.

def findrepeat( system ):
    found = [0,0,0]
    zeros = tuple([0]*len(system))
    step(system)
    nstep = 1
    while not all(found):
        for axis in range(3):
            if not found[axis] and getstate(system,axis) == zeros:
                print("Found",axis,"at",nstep)
                found[axis] = nstep*2
        step(system)
        nstep += 1
    return found

def run2(system):
    cycles = findrepeat( makemoons(system) )
    print( cycles, lcm3(*cycles) )
    return lcm3(*cycles)

def part2():
    print( "Part 2:", run2( real ) )

def dotiming(fn):
    p1 = time.time()
    fn()
    p2 = time.time()
    print( "Elapsed:", p2-p1)

dotiming( part1 )
dotiming( part2 )

