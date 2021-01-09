
data = open('day03.txt').read()

pt = 0

delta = {
    '^': 0-1j,
    "v": 0+1j,
    "<": -1,
    ">": 1,
    '\n': 0
}

visit = set()
visit.add(pt)
for ch in data:
    pt += delta[ch]
    visit.add( pt )

print( "Part 1:", len(visit) )

pt,xx = 0, 0
visit = set()
visit.add(pt)

for ch in data:
    pt += delta[ch]
    visit.add( pt )
    xx,pt = pt,xx

print( "Part 2:", len(visit) )
