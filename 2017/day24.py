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

#data = translate(test)
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

maxp = 0
maxlen = 0
maxlenp = 0
def chain(p, search, accum):
    global maxp, maxlen, maxlenp
    accum = accum[:]
    accum.append( p )
    left[p[0]].remove( p )
    right[p[1]].remove( p )

    lefts = left[search] if search in left else []
    rights = right[search] if search in right else []

    if not lefts and not rights:
        tot = sum((i+j for i,j in accum))
        if tot > maxp:
            maxp = tot
        if len(accum) > maxlen:
            maxlen = len(accum)
            maxlenp = tot
        elif len(accum) == maxlen:
            if tot > maxlenp:
                maxlenp = tot
        print 'end', accum, tot
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
print maxp, maxlen, maxlenp


