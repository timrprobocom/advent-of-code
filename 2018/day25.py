from __future__ import print_function
import sys

def empty(*args,**kwargs):
    pass

if '-v' in sys.argv:
    dbgprint = print
    from pprint import pprint
else:
    dbgprint = empty
    pprint = empty

test0 = (
    ( 0,0,0,0),
    ( 3,0,0,0),
    ( 0,3,0,0),
    ( 0,0,3,0),
    ( 0,0,0,3),
    ( 0,0,0,6),
    ( 9,0,0,0),
    (12,0,0,0)
)

test1 = (
    (-1,2,2,0),
    (0,0,2,-2),
    (0,0,0,-2),
    (-1,2,0,0),
    (-2,-2,-2,2),
    (3,0,2,-1),
    (-1,3,2,2),
    (-1,0,-1,0),
    (0,2,1,-2),
    (3,0,0,0),
)

test2 = (
    (1,-1,0,1),
    (2,0,-1,0),
    (3,2,-1,0),
    (0,0,3,1),
    (0,0,-1,-1),
    (2,3,-2,0),
    (-2,2,0,0),
    (2,-2,0,-1),
    (1,-1,0,-1),
    (3,2,0,2),
)

test3 = (
    (1,-1,-1,-2),
    (-2,-2,0,1),
    (0,2,1,3),
    (-2,3,-2,1),
    (0,2,3,-2),
    (-1,-1,1,-2),
    (0,-2,-1,0),
    (-2,2,3,-1),
    (1,2,2,0),
    (-1,-2,0,-2),
)

live = tuple(tuple(int(k) for k in ln.split(',')) for ln in open('day25.txt'))

CONST = 3

def mandist( a, b ):
    return sum(abs(aa-bb) for aa,bb in zip(a,b))


def fillconstellation( remain ):
    const = [remain.pop(0)]
    done = False
    while not done:
        done = True
        for pta in remain[:]:
            accept = False
            # Compare this point against the other points in the constellation.
            for ptb in const:
                dbgprint( pta, ptb )
                if mandist(pta,ptb) <= CONST:
                    accept = True
                    break
            if accept:
                done = False
                remain.remove( pta )
                const.append( pta )
    return const



def tryme(data):
    remain = list(data)
    dbgprint( remain )

    constellations = []
    while remain:
        constellations.append( fillconstellation( remain ) )
    pprint(constellations)
    return len(constellations)

print( tryme(test0) )
print( tryme(test1) )
print( tryme(test2) )
print( tryme(test3) )
print( tryme(live) )
