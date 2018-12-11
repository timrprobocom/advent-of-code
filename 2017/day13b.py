test = """\
0: 3
1: 2
4: 4
6: 4""".splitlines()

live = open('day13.txt').readlines()

# Is there a numerical answer?  Yes, and it's way faster.

# 0 fails when ps mod 4 == 0
# 1 fails when ps+1 mod 2 == 0
# 4 fails when ps+4 mod 6 == 0
# 6 fails when ps+6 mod 6 == 0


def fill(data):
    layer = []
    for ln in data:
        posn,size = tuple(int(k) for k in ln.split(": "))
        while len(layer) < posn:
            layer.append( 0 )
        layer.append( size + size - 2 )
    return layer

import itertools

arena = fill(live)


# At ps=26 we can be looking at 26 25 24 23 22

fail = []
for ps in itertools.count():
    if ps % 100000 == 0:
        print ps
    ok = True
    for col,a in enumerate(arena):
        if not a:
            continue
#        print ps, col, a
        if ((ps+col) % a) == 0:
            ok = False
            break
    if ok:
        print ps, "Success"
        break

