
A = 16807
B = 48271
mod = 0x7fffffff

test = (65, 8921)

def gen( start, mult, factor ):
    a = start
    while 1:
        a = (a * mult) % 2147483647
        if a % factor == 0:
            yield a

#g1 = gen( 65, A, 4 )
#g2 = gen( 8921, B, 8 )
g1 = gen( 277, A, 4 )
g2 = gen( 349, B, 8 )

count = 0
for i in xrange(5000000):
    p1 = g1.next()
    p2 = g2.next()
    if p1 & 0xffff == p2 & 0xffff:
        count += 1
print count
