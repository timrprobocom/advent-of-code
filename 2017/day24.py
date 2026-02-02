import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

test = """\
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10""".splitlines()

def translate(lines):
    tups = []
    for ln in lines:
        tups.append( tuple(int(a) for a in ln.rstrip().split('/')) )
    return tups

if TEST:
    data = translate(test)
else:
    data = translate(open('day24.txt').readlines())

def fill(tups):
    left = {}
    right = {}
    for t in tups:
        if t[0] not in left:
            left[t[0]] = []
        left[t[0]].append(t)
        if t[1] not in right:
            right[t[1]] = []
        right[t[1]].append(t)
    return left,right

left,right = fill(data)

class Keep:
    p = 0
    len = 0
    lenp = 0

maxx = Keep()

def chain(p, search, accum):
    accum = accum[:]
    accum.append( p )
    left[p[0]].remove( p )
    right[p[1]].remove( p )

    lefts = left[search] if search in left else []
    rights = right[search] if search in right else []

    if not lefts and not rights:
        tot = sum((i+j for i,j in accum))
        if tot > maxx.p:
            maxx.p = tot
        if len(accum) > maxx.len:
            maxx.len = len(accum)
            maxx.lenp = tot
        elif len(accum) == maxx.len:
            if tot > maxx.lenp:
                maxx.lenp = tot
        if DEBUG:
            print('end', accum, tot)
    else:
        for l in lefts:
            chain( l, l[1], accum )
        for r in rights:
            chain( r, r[0], accum )

    left[p[0]].append( p )
    right[p[1]].append( p )


accum = []
if 0 in left:
    for start in left[0]:
        chain( start, start[1], accum )
if 0 in right:
    for start in right[0]:
        chain( start, start[0], accum )
if DEBUG:
    print(maxx.__dict__)
print('Part 1:', maxx.p)
print('Part 2:', maxx.lenp)
