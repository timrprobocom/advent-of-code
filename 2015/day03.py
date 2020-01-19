from collections import defaultdict

data = open('day03.txt').read()

pt = (0,0)
visit = defaultdict(int)

delta = {
    '^': (0,-1),
    "v": (0,1),
    "<": (-1,0),
    ">": (1,0),
    '\n': (0,0)
}

visit = set()
visit.add(pt)
for ch in data:
    dx = delta[ch]
    pt = (pt[0]+dx[0],pt[1]+dx[1])
    visit.add( pt )

print( "Part 1:", len(visit) )

pts = [(0,0),(0,0)]
visit = set()
visit.add(pts[0])

for ch in data:
    dx = delta[ch]
    pt = pts.pop(0)
    pt = (pt[0]+dx[0],pt[1]+dx[1])
    visit.add( pt )
    pts.append( pt )

print( "Part 2:", len(visit) )
