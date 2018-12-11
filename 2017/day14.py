test='flqrgnkx'
live='nbysizxe'

# 128 bits is 16 bytes
# I have 10, 11, or 12 characters

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

def makecounts():
    counts = []
    for i in range(256):
        c = 0
        for b in (1,2,4,8,16,32,64,128):
            if i & b:
                c += 1
        counts.append(c)
    return counts

counts = makecounts()

def countbits(hx):
    c = 0
    for byte in hx.decode('hex'):
        c += counts[ord(byte)]
    return c

def makearray(data):
    array = []
    for row in range(128):
        array.append( knothash('%s-%d' % (data,row) ) )
    return array

def parta(array):
    return sum( countbits(row) for row in array )

def convert(array):
    grid = []
    for row in array:
        binrow = []
        for c in row.decode('hex'):
            for b in (128,64,32,16,8,4,2,1):
                binrow.append( -1 if ord(c) & b else 0 )
        grid.append(binrow)
    return grid

def contiguous( grid, y, x, tag ):
    grid[y][x] = tag
    if x > 0 and grid[y][x-1] < 0:
        contiguous( grid, y, x-1, tag )
    if x < 127 and grid[y][x+1] < 0:
        contiguous( grid, y, x+1, tag )
    if y > 0 and grid[y-1][x] < 0:
        contiguous( grid, y-1, x, tag )
    if y < 127 and grid[y+1][x] < 0:
        contiguous( grid, y+1, x, tag )

def partb(grid):
    tag = 1
    for y in range(128):
        for x in range(128):
            if grid[y][x] == -1:
                contiguous( grid, y, x, tag )
                tag += 1
    return tag-1

array = makearray(test)
print 'Part A', parta(array)
grid = convert(array)
print 'Part B', partb(grid)
for y in range(16):
    print ' '.join('%3d' % k for k in grid[y][0:16])


array = makearray(live)
print 'Part A', parta(array)
grid = convert(array)
print 'Part B', partb(grid)
for y in range(16):
    print ' '.join('%3d' % k for k in grid[y][0:16])
