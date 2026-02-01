import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    rope = list(range(5))
    data = [3,4,1,5]
else:
    rope = list(range(256))
    data = [94,84,0,79,2,27,81,1,123,93,218,23,103,255,254,243]

live = str(data)[1:-1].replace(' ','')

def part1(data,rope):
    posn = 0
    skip = 0
    if DEBUG:
        print(rope)
    for i in data:
        # Rotate so position is at 0.
        p1 = rope[posn:]+rope[:posn]
        sub = p1[:i]
        sub.reverse()
        # Put it back together.
        p1 = sub + p1[i:]
        # Unrotate.
        rest = len(rope)-posn
        rope = p1[rest:]+p1[:rest]
        posn = (posn + i + skip) % len(rope)
        skip += 1
    if DEBUG:
        print(rope)
    return rope[0]*rope[1]

tests = [
    "",
    "AoC 2017",
    "1,2,3",
    "1,2,4"
]

extra = ''.join(chr(k) for k in (17,31,73,47,23))

def knothash(inp):
    val = inp + extra
    rope = list(range(256))
    posn = 0
    skip = 0

    for k in range(64):
        for c in val:
            i = ord(c)
            # Rotate so position is at 0.
            p1 = rope[posn:]+rope[:posn]
            sub = p1[:i]
            sub.reverse()
            # Put it back together.
            p1 = sub + p1[i:]
            # Unrotate.
            rest = len(rope)-posn
            rope = p1[rest:]+p1[:rest]
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

print('Part 1:', part1(data,rope))
if TEST:
    for t in tests:
        print(t,knothash(t))
else:
    print('Part 2:', knothash(live) )



