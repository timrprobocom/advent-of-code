import sys

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

    def advance(self):
        self.v = tuple((a+b for a,b in zip(self.v,self.a)))
        self.p = tuple((a+b for a,b in zip(self.p,self.v)))

def universe(fn):
    particles = []
    for ln in open(fn).readlines():
        s = ln.replace('<','(').replace('>',')').replace(', ',';')
        particles.append( particle(len(particles),s) )
    return particles

# Advances all, then returns uncollided particles.
def cycle( particles ):
    check = {}
    for part in particles:
        part.advance()
        if part.p not in check:
            check[part.p] = []
        check[part.p].append(part)

    newpart = []
    for v in check.values():
        if len(v) == 1:
            newpart.extend(v)
        else:
            print( tuple(k.ord for k in v) )
    return newpart

if len(sys.argv) < 2:
    print( "Usage: day20.py xxx.txt" )
    sys.exit()

particles = universe(sys.argv[1])
for i in range(100):
    particles = cycle(particles)
    print( len(particles) )
