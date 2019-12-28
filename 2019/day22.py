import sys
import math
import functools

TRACE = 'trace' in sys.argv

# Find the multiplicative inverse in a modulus field.

# This is Euler's theorem.  This is slick, but it really only works if
# mod is prime.  The first line computes the "totient" of the modulus,
# which is mod-1 if mod is prime, but requires prime factoring otherwise.
# The test case uses mod 10 which, of course, is not prime.  We hardcode 
# the totient for 10 to allow the test to work.

def invert_euler(n, mod):
    tot = 4 if mod == 10 else mod - 1
    return pow(n, tot-1, mod)

# This is the Extended Euclidean Algorithm.  It does not care about the
# totient.  It does, however, fail if a is negative, so we compensate.
# It is basically doing a GCD.

def invert_euclid(a, n):
    t = 0; newt = 1
    r = n; newr = a if a > 0 else a+n

    while newr:
        q = r // newr
        (t,newt) = (newt, t - q * newt)
        (r,newr) = (newr, r - q * newr)
    if r > 1:
        print( a, "is not invertable mod", b )
        sys.exit(0)
    if t < 0:
        t += n
    return t

invert = invert_euclid
 

test1 = """\
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1"""
# Result: 9 2 5 8 1 4 7 0 3 6


# A deck can be encoded as ax+b mod n.

class Deck(object):
    def __init__(self,k):
        self.count = k
        self.state = (0,1)

    def cut(self,n):
        off = (self.state[0] + self.state[1] * n) % self.count
        self.state = (off, self.state[1])

    def reverse(self):
        inc = -self.state[1] 
        self.state = ((self.state[0]+inc+self.count) % self.count, inc)

    def increment(self,n):
        inc = (self.state[1] * invert(n, self.count)) % self.count
        self.state = (self.state[0], inc)

    def run( self, src ):
        for ln in src:
            if TRACE:
                print( ln.strip() )
            words = ln.strip().split()
            if words[0] == 'cut':
                self.cut( int(words[1]) )
            if words[1] == 'with':
                self.increment( int(words[3]) )
            if words[1] == 'into':
                self.reverse()
            if TRACE:
                print( self.state )

# Do a part 1 test.  Should be 9 2 5 8 1 4 7 0 3 6, or 9+3x.

COUNT = 10
deck = Deck(COUNT)
deck.run( test1.splitlines() )
print( deck.state )
b,m = deck.state
for x in range(COUNT):
    print( (m*x+b) % COUNT, end='' )
print( '' )

# Do part 1.  Should be 4775.

COUNT = 10007
real = open("day22.txt").readlines()

deck = Deck(COUNT)
deck.run( real )
print( deck.state )
b,m = deck.state

for x in range(COUNT):
    if (m*x+b) % COUNT == 2019:
        print( "Part 1:", x );
        break

# Do part 2.  Shouild be 37889219674304.

COUNT = 119315717514047

deck = Deck(COUNT)
deck.run( real )
print( deck.state )
b,m = deck.state

# So, each cycle through will do
# bn = mn * b
# mn = m
# So it's a geometric series.  b x (1-m^cycles) / (1-m).
# The formula comes from Wikipedia.  There's magic to do
# exponentiation and inversion in a modulus field.

cycles = 101741582076661
finalm = pow( m, cycles, COUNT )
finalb = (b * (1 - finalm) * invert(1 - m, COUNT)  ) % COUNT
print(finalm,finalb)

tgt = 2020
print( "Part 2:", (finalm * tgt + finalb) % COUNT )

