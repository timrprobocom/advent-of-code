tests = [
    "",
    "AoC 2017",
    "1,2,3",
    "1,2,4",
    "94,84,0,79,2,27,81,1,123,93,218,23,103,255,254,243"
]

extra = ''.join(chr(k) for k in (17,31,73,47,23))

def knothash(inp):
    val = inp + extra
    rope = range(256)
    posn = 0
    skip = 0

    for k in range(64):
        for c in val:
            i = ord(c)
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

    # Compute hash.

    xor = 0
    knot = ""
    for i,c in enumerate(rope):
        xor = xor ^ c
        if i % 16 == 15:
            knot += "%02x" % xor
            xor = 0
    return knot

for t in tests:
    print round(t), t
