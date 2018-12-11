import sys
import md5

# So, for each hex digit 0 to f, look for 3 in a row and 5 in a row.
# Track:
#   000 found at 192 and 2339
#   111 found at 336
# When quint is found
#   If matching triplet 

def dohash(s):
    for i in range(2017):
        s = md5.md5(s).hexdigest()
    return s

class Triplets(object):
    def __init__(self):
        self.data = dict( zip( '0123456789abcdef', ([],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]) ) )
        self.keys = {}

    def ageOut( self, index ):
        for row in self.data:
            if index-1000 in row:
                row.remove(index-1000)

    def add( self, digit, index ):
        print "Adding %d for %s" % (index, digit*3)
        self.data[digit].append( index )

    def compare( self, digit, index ):
        for i in self.data[digit]:
            if i >= index-1000:
                print "*** Match '%s' %d and %d" % (digit, i, index)
                self.keys[i] = 1

#SALT = 'abc'
SALT = 'cuanljph'

triplets = Triplets()

index = 0
while len(triplets.keys) < 72:
    md5x = dohash(SALT+str(index))
    for c in '0123456789abcdef':
        quint = c*5
        if md5x.find( quint ) >= 0:
            print "Checking quint %s at %d" % (quint,index)
            triplets.compare( c, index )
    for i in range(len(md5x)-2):
        if md5x[i] == md5x[i+1] == md5x[i+2]:
            triplets.add( md5x[i], index )
            break
    index += 1

print triplets.keys
print len(triplets.keys)
k = triplets.keys.keys()
k.sort()
print k[63]
