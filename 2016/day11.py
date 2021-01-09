from pprint import pprint
import itertools
import sys
import queue


# Initial state:
#
#  4:
#  3:   PmG  PmM  RuG  RuM
#  2:             PuM  SrM
#  1: E TmG  TmM  PuG  SrG  ElG  ElM  DiG  DiM

# Generators are negative, chips are positive.

dprint = print if 'debug' in sys.argv else lambda *s: 0

if 'test' in sys.argv:
    bldg = ( ( 1, 2 ), ( -1, ), ( -2, ), () )
else:
    bldg = ( ( -1, 1, -2, -3 ), ( 2, 3 ), ( -4, 4, -5, 5 ), ( ) )

bldg = tuple(tuple(sorted(k)) for k in bldg)

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

# Yield all possible moves from this floor.

def get_moves(bldg, floor):
    contents = bldg[floor]
    # Don't go back to lower floors once cleared.
    minfloor = min( i for i,f in enumerate(bldg) if f )
    for newfloor in (floor-1, floor+1):
        if newfloor < minfloor or newfloor > 3:
            continue
        # We can move any single or any pair.
        for n in itertools.chain( contents, itertools.combinations(contents,2)):
            new1 = diff(contents, n)
            new2 = union(bldg[newfloor], n)
            if not valid(new1) or not valid(new2):
                continue
            if newfloor < floor:
                newbldg = bldg[:floor-1] + (new2,new1) + bldg[floor+1:]
            else:
                newbldg = bldg[:floor] + (new1,new2) + bldg[floor+2:]
            yield newfloor, newbldg

def process(bldg):
    seen = set( (0,bldg) )
    undone = queue.Queue()
    undone.put( (bldg,0,1) )
    count = 0
    while not undone.empty():
        count += 1
        if count % 10000 == 0:
            print(count,depth)
        bldg, elevator, depth = undone.get()
        dprint( depth, elevator, bldg )
        dprint( list( get_moves(bldg, elevator) ) )
        dprint( "****" )
        for newfloor,newbldg in get_moves(bldg, elevator):
            if not any(newbldg[0:3]):
                print( "WINNER", depth, newbldg )
                return depth
            if (elevator,newbldg) in seen:
                continue
            seen.add( (elevator,newbldg) )
            undone.put( (newbldg, newfloor, depth+1 ) )

# This does reach the correct state, but it takes 39 steps.
# Should be 31.  Why?
# Clearing a floor with N symbols is 2*(N-1)-1
# 4 2 4 0 = 5, 9, 17 = 31

print( "Part 1:", process(bldg) )

bldg = ( ( -1, 1, -2, -3, 6, -6, 7, -7 ), ( 2, 3 ), ( -4, 4, -5, 5 ), ( ) )
bldg = tuple(tuple(sorted(k)) for k in bldg)
print( "Part 2:", process(bldg) )

# 8 2 4 0 = 13, 17, 25 = 55
