import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Normal initialization.
class particle(object):
    def __init__(self,ord,p,v,a):
        self.ord = ord
        self.p = p
        self.v = v
        self.a = a

    def advance(self):
        self.v = tuple((kv+ka for kv,ka in zip(self.v,self.a)))
        self.p = tuple((kp+kv for kp,kv in zip(self.p,self.v)))

# Slimy initialization.
class particle(object):
    def __init__(self,ord,s):
        self.ord = ord
        exec( s, self.__dict__ )
        self.track = [self.p]

    def advance(self):
        self.v = tuple((a+b for a,b in zip(self.v,self.a)))
        self.p = tuple((a+b for a,b in zip(self.p,self.v)))
        self.track.append( self.p )

def universe(fn):
    particles = []
    for ln in open(fn).readlines():
        s = ln.replace('<','(').replace('>',')').replace(', ',';')
        particles.append( particle(len(particles),s) )
    return particles

# Advances all, then returns uncollided particles.
collisions = []
def cycle( particles ):
    check = {}
    for part in particles:
        part.advance()
        if part.p not in check:
            check[part.p] = []
        check[part.p].append(part)

    newpart = []
    for p,v in check.items():
        if len(v) == 1:
            newpart.extend(v)
        else:
            collisions.append( p )
            print( tuple(k.ord for k in v) )
    return newpart

if len(sys.argv) < 2:
    print( "Usage: day20.py xxx.txt" )
    sys.exit()

particles = universe(sys.argv[1])
for i in range(20):
    particles = cycle(particles)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d' )
for part in particles:
    xs = tuple(a[0] for a in part.track)
    ys = tuple(a[1] for a in part.track)
    zs = tuple(a[2] for a in part.track)
    ax.plot( xs, ys, zs )

xs = tuple(a[0] for a in collisions)
ys = tuple(a[1] for a in collisions)
zs = tuple(a[2] for a in collisions)
ax.scatter( xs, ys, zs )
plt.xlim(-1000,1000)
plt.ylim(-1000,1000)
ax.set_zlim(-1000,1000)
plt.show()
