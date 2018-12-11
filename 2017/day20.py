# p=< 0,0,0>, v=<0,0,0>, a=<0,0,0>


class particle:
    def __init__(self, ord,ln=""):
        self.ord = ord
        self.p = (0,0,0)
        self.v = (0,0,0)
        self.a = (0,0,0)
        if ln:
            self.parse( ln )

    def parse(self,ln):
        ln = ln.replace('<','(').replace('>',')').replace(', ',';')
        exec(ln)
        self.p = p
        self.v = v
        self.a = a

#        i1 = ln.find('<')
#        i2 = ln.find('>',i1)
#        self.p = tuple (int(k) for k in ln[i1+1:i2].split(',') )

#        i1 = ln.find('<',i2)
#        i2 = ln.find('>',i1)
#        self.v = tuple (int(k) for k in ln[i1+1:i2].split(',') )

#        i1 = ln.find('<',i2)
#        i2 = ln.find('>',i1)
#        self.a = tuple (int(k) for k in ln[i1+1:i2].split(',') )

    def cycle(self):
        self.v = tuple(i+j for i,j in zip(self.v,self.a))
        self.p = tuple(i+j for i,j in zip(self.p,self.v))

    def dist(self):
        p = self.p
        print p
        return p[0]*p[0]+p[1]*p[1]+p[2]*p[2]

def collide( particles ):
    known = {}
    for p in particles:
        if p.p in known:
            known[p.p].append(p)
        else:
            known[p.p] = [p]
    new = []
    for v in known.values():
        if len(v) == 1:
            new.append( v[0] )
    particles[:] = new


particles = []
#particles.append( particle( 0, "p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>" ) )
#particles.append( particle( 1, "p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>" ) )

for ln in open('day20.txt').readlines():
    particles.append(particle( len(particles), ln ) )

mina = 99999999999
mins = []
for p in particles:
    d = p.a[0]*p.a[0] + p.a[1]*p.a[1] + p.a[2]*p.a[2]
    if d < mina:
        mina = d
        mins = [p]
    elif d == mina:
        mins.append( p )

for i in range(1000):
    for p in particles:
        p.cycle()
    collide( particles )


#mind = 9999999999999
#mindo = 0
#for p in particles:
#    d = p.dist()
#    if d < mind:
#        mind = d
#        mindo = p.ord

print mins[0].__dict__
print "bbbbb", len(particles)
print "***", mind, mindo

