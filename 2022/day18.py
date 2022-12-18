import re
import sys
from functools import cmp_to_key

test = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day18.txt').readlines()

DEBUG = 'debug' in sys.argv

dout = set()
for line in data:
    x,y,z = line.strip().split(',')
    dout.add((int(x),int(y),int(z)))
data = dout

directions = (-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)

def around(cube):
    for delta in directions:
        yield tuple(a+b for a,b in zip(cube,delta))

def part1(data):
    result = 0
    seen = set()
    for cube in data:
        result += 6
        for near in around(cube):
            if near in seen:
                result -= 2
        seen.add(cube)
    return result

minx = min(x for x,y,z in data)
maxx = max(x for x,y,z in data)
miny = min(y for x,y,z in data)
maxy = max(y for x,y,z in data)
minz = min(z for x,y,z in data)
maxz = max(z for x,y,z in data)
xrange = range(minx,maxx+1)
yrange = range(miny,maxy+1)
zrange = range(minz,maxz+1)

# This eventually builds up a list of all cubes within the x,y,z range
# that are not surrounded by other cubes.  That should be the external 
# surface area.

def is_exterior(data,exterior,cube):
    if cube in data:
        return 0
    checked = set()
    todo = [cube]
    while todo:
        cube = todo.pop(0)
        if cube in checked:
            continue
        checked.add(cube)
        if cube in exterior:
            exterior.update( checked - data )
            return 1
        if cube[0] not in xrange or cube[1] not in yrange or cube[2] not in zrange:
            exterior.update( checked - data )
            return 1
        if cube not in data:
            for near in around(cube):
                todo.append(near)
    return 0

def part2(data):
    exterior = set()
    return sum( is_exterior(data,exterior,near) for cube in data for near in around(cube))

print("Part 1:", part1(data))
print("Part 2:", part2(data))
