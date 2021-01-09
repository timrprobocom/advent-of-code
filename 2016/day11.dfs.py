from pprint import pprint
import itertools
import sys


# Initial state:
#
#  4:
#  3:   PmG  PmM  RuG  RuM
#  2:             PuM  SrM
#  1: E TmG  TmM  PuG  SrG  ElG  ElM  DiG  DiM


# What's the state structure?
# Set of floors:

if 'test' in sys.argv:
    bldg = ( ( 1, 2 ), ( -1, ), ( -2, ), () )
else:
    bldg = ( ( -1, 1, -2, -3 ), ( 2, 3 ), ( -4, 4, -5, 5 ), ( ) )

bldg = tuple(tuple(sorted(k)) for k in bldg)

# Yield all possible moves from this floor.

def union(a,b):
    if type(b) is not tuple:
        b = (b,)
    return tuple(sorted(a+b))

def diff(a,b):
    if type(b) is not tuple:
        b = (b,)
    return tuple(k for k in a if k not in b)

def valid(contents):
    # A floor is invalid if there is a generator (-) and 
    # a micro (+) without a generator (-),
    return not (
       any(m for m in contents if m < 0) and 
       any(m for m in contents if m > 0 and -m not in contents)
   )

def get_moves(bldg, floor):
    contents = bldg[floor]
    # Don't go back to lower floors once cleared.
    minfloor = min( i for i,f in enumerate(bldg) if f )
    for direc in (1, -1):
        newfloor = floor + direc
        if newfloor < minfloor or newfloor > 3:
            continue
        # We can ship any single or any pair.
        for n in itertools.chain( contents, itertools.combinations(contents,2)):
            new1 = diff(contents, n)
            new2 = union(bldg[newfloor], n)
            if not valid(new1) or not valid(new2):
                continue
            if direc < 0:
                newbldg = bldg[:floor-1] + (new2,new1) + bldg[floor+1:]
            else:
                newbldg = bldg[:floor] + (new1,new2) + bldg[floor+2:]
            yield newfloor, newbldg


seen = { (0,bldg) : 0 }

def try_moves(bldg, elevator, depth=0):
    print( depth, elevator, bldg )
    pprint( list( get_moves(bldg, elevator) ) )
    print( "****" )
    for newfloor,newbldg in get_moves(bldg, elevator):
        if (elevator,newbldg) in seen and depth >= seen[(elevator,newbldg)]:
            continue
        if not any(newbldg[0:3]):
            print( "WINNER", depth, newbldg )
            sys.exit(0)
        seen[ (elevator,newbldg) ] = depth
        try_moves( newbldg, newfloor, depth+1 )

try_moves( bldg, 0 )
