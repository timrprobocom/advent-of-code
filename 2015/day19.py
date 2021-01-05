import sys


DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

test = """\
H => HO
H => OH
O => HH

HOH""".splitlines()

if 'test' in sys.argv:
    data = test
else:
    data = open('day19.txt').read().splitlines()

changes = []
for ln in data:
    if '=>' in ln:
        a,b = ln.split(' => ')
        changes.append( (a, b) )
    elif ln:
        basis = ln

results = set()
for a,b in changes:
    i = ln.find(a)
    while i >= 0:
        nx = ln[0:i] + b + ln[i+len(a):]
        results.add(nx)
        i = ln.find(a,i+1)

print( "Part 1:", len(results) )

# Part 2 merits an analytical approach, not brute force.

# There are only four different productions:
#   e => XX
#   X => X Rn X Ar | X Rn X Y X Ar | X Rn X Y X Y X Ar
#
# Think of Rn Y Ar as ( , ).  So:
#   X => X ( X ) | X ( X , X ) | X ( X , X , X ) 
# Each of those steps the size by 3, 5, or 7
#
# Each , reduces the size by 2 -- the , X
# Each ( and ) results the size by 1.  
# After parens are gone, it takes N-1 steps to get to 'e'.

rn = basis.count('Rn')
ar = basis.count('Ar')
yy = basis.count('Y')
ele = sum( 1 for c in basis if c < 'a' )
dprint( ele, rn, ar, yy )
print( "Part 2:", ele - rn - ar - yy - yy - 1 )
