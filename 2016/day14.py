import sys
import hashlib

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

# So, for each hex digit 0 to f, look for 3 in a row and 5 in a row.
# Track:
#   000 found at 192 and 2339
#   111 found at 336
# When quint is found
#   If matching triplet 

def dohash(s,n):
    for _ in range(n):
        s = hashlib.md5(s.encode('ascii')).hexdigest()
    return s

class Triplets(object):
    def __init__(self):
        self.data = dict( zip( '0123456789abcdef', ([],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]) ) )
        self.keys = []

    def ageOut( self, index ):
        for row in self.data:
            if index-1000 in row:
                row.remove(index-1000)

    def add( self, digit, index ):
        if DEBUG:
            print( "Adding %d for %s" % (index, digit*3) )
        self.data[digit].append( index )

    def compare( self, digit, index ):
        for i in self.data[digit]:
            if i >= index-1000 and i not in self.keys:
                if DEBUG:
                    print( "*** Match '%s' %d and %d" % (digit, i, index) )
                self.keys.append( i )

if TEST:
    SALT = 'abc'
else:
    SALT = 'cuanljph'

def part(n):
    triplets = Triplets()
    index = 0
    while len(triplets.keys) < 64:
        md5x = dohash(SALT+str(index), n*2016+1)
        for c in '0123456789abcdef':
            quint = c*5
            if md5x.find( quint ) >= 0:
                if DEBUG:
                    print( "Checking quint %s at %d" % (quint,index) )
                triplets.compare( c, index )
        for i in range(len(md5x)-2):
            if md5x[i] == md5x[i+1] == md5x[i+2]:
                triplets.add( md5x[i], index )
                break
        index += 1
    if DEBUG:
        print( triplets.keys )
    return triplets.keys[63]

print("Part 1:", part(0))
print("Part 2:", part(1))