
data = open('day03.txt').read()

pt = 0+0j

delta = {
    '^': 0-1j,
    "v": 0+1j,
    "<": -1+0j,
    ">": 1+0j,
    '\n': 0+0j
}

# Range is -26 to 55, -17 to 127.  That's 81 x 144.

grid = [ [' ']*145 for i in range(82) ]

nexts = dict(zip(' 0123456789','01234567899'))

import time
def record(pt):
    y = int(pt.real) + 26
    x = int(pt.imag) + 17
    grid[y][x] = nexts[grid[y][x]]
    for row in grid:
        print( ''.join(row).rstrip() )
    time.sleep(.10)


visit = set()
visit.add(pt)
for ch in data:
    pt += delta[ch]
    visit.add( pt )
    record( pt )

print( "Part 1:", len(visit) )
print( min(x.real for x in visit) )
print( min(x.imag for x in visit) )
print( max(x.real for x in visit) )
print( max(x.imag for x in visit) )

pt,xx = 0, 0
visit = set()
visit.add(pt)

for ch in data:
    pt += delta[ch]
    visit.add( pt )
    xx,pt = pt,xx

print( "Part 2:", len(visit) )
