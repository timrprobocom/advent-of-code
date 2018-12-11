test = """\
0: 3
1: 2
4: 4
6: 4""".splitlines()

live = open('day13.txt').readlines()

class Scanner(object):
    def __init__( self, size=0 ):
        self.size = size
        self.posn = 0 if size else -1
        self.dir = 1 if size else 0

    def advance(self):
        if not self.size:
            return
        self.posn += self.dir
        if self.posn == 0:
            self.dir = 1
        elif self.posn == self.size-1:
            self.dir = -1

def fill(data):
    layer = []
    for ln in data:
        posn,size = tuple(int(k) for k in ln.split(": "))
        while len(layer) < posn:
            layer.append( Scanner() )
        layer.append( Scanner(size) )
    return layer

def advance(arena):
    for a in arena:
        a.advance()

def xprint(arena):
    for posn,a in enumerate(arena):
        print posn, a.size, a.posn, a.dir

arena = fill(live)


import itertools

# At ps=26 we can be looking at 26 25 24 23 22

fail = []
for ps in itertools.count():
    if ps % 10000 == 0: print ps
    fail.append( 0 )
    for col,a in enumerate(arena):
        if ps >= col:
            who = ps - col
            if arena[col].posn == 0:
#                print who, "fail in", col
                fail[who] = 1
    if ps >= len(arena) and not fail[ps-len(arena)+1]:
        print ps-len(arena)+1, "Success"
        break
    advance(arena)

# 
# This was part 1
#
#    if arena[me].posn == 0:
#        print "Hit in", me
#        penalty += me * arena[me].size
#    advance(arena)
#
#print penalty

