#rope = range(5)
#data = [3,4,1,5]

rope = range(256)
data = [94,84,0,79,2,27,81,1,123,93,218,23,103,255,254,243]

posn = 0
skip = 0

print rope
for i in data:
    # Rotate so position is at 0.
    p1 = rope[posn:]+rope[:posn]
    sub = p1[:i]
#    print "x",sub
    sub.reverse()
#    print "y",sub
    # Put it back together.
    p1 = sub + p1[i:]
    # Unrotate.
    rest = len(rope)-posn
    rope = p1[rest:]+p1[:rest]
#    print i, posn, skip, rope
    posn = (posn + i + skip) % len(rope)
    skip += 1

print rope
print rope[0]*rope[1]



