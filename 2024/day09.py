import os
import sys

test = """\
2333133121414131402"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.strip()
else:
    data = open(day+'.txt').read().strip()

data = [int(c) for c in data]

def part1(data):
    idn = 0
    disk = []

    for i,size in enumerate(data):
        if i % 2:
            disk.extend( [-1]*size)
        else:
            disk.extend( [idn]*size)
            idn += 1

    # Now compact it.
    i = 0
    j = len(disk)-1

    while i < j:
        while disk[i] >= 0:
            i += 1
        while disk[j] < 0:
            j -= 1
        if i < j:
            disk[i], disk[j] = disk[j], -1
            i += 1
            j -= 1
    
    if DEBUG:
        print(disk)

    # Evaluate.

    sumx = 0
    for n,i in enumerate(disk):
        if i >= 0:
            sumx += n*i
    return sumx

# Combine free blocks and remove empty ones.

def coalesce( space, start, size ):
    newspace = []
    while space:
        sstart, ssize = space.pop(0)
        if not ssize:
            continue
        elif start > sstart+ssize:
            newspace.append( [sstart, ssize] )
        elif start+size == sstart:
            newspace.append( [start, size+ssize] )
            break
        elif sstart+ssize == start:
            newspace.append( [sstart, size+ssize] )
            break
        elif sstart > start+size:
            break
    return newspace+space

# Find the first hold large enough to hold this file.

def find_hole_below( space, start, size ):
    for i,s in enumerate(space):
        if s[0] > start:
            return -1
        if s[1] >= size:
            return i
    return -1

def part2(data):
    locate = 0
    files = []
    space = []

    for i,size in enumerate(data):
        if i % 2:
            space.append( [locate, size] )
        else:
            files.append( [locate, size, len(files)] )
        locate += size

    if DEBUG:
        print(files)
        print(space)

    # Now try to move all the files starting from the end.

    for start,size,idn in reversed(files):
        n = find_hole_below( space, start, size )
        if n >= 0:
            # Move this file.  Reduce empty space.
            files[idn][0] = space[n][0]
            space[n][0] += size
            space[n][1] -= size
            space = coalesce(space, start, size)
    
    if DEBUG:
        files.sort()
        print(files)
        print(space)

    # Evaluate.  There are better ways to compute the sum of a sequence, but
    # we know that no file is longer than 9 blocks.

    return sum( sum(range(start,start+size)) * idn for start,size,idn in files )

print("Part 1:", part1(data))
print("Part 2:", part2(data))
