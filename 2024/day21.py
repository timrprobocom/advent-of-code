import os
import sys
import math
from functools import cache

test = """\
029A
980A
179A
456A
379A"""

live = """\
973A
836A
780A
985A
413A"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test
else:
    data = live

data = data.splitlines()


# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

buttons = {
    '7': (0,0),
    '8': (1,0),
    '9': (2,0),
    '4': (0,1),
    '5': (1,1),
    '6': (2,1),
    '1': (0,2),
    '2': (1,2),
    '3': (2,2),
    'X': (0,3),
    '0': (1,3),
    'A': (2,3)
}

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

dirpad = {
    'X': (0,0),
    '^': (1,0),
    'A': (2,0),
    '<': (0,1),
    'v': (1,1),
    '>': (2,1)
}


@cache
def cheapestAuxPad( x0, y0, x1, y1, robots ):
    res = math.inf
    queue = []
    queue.append( (x0,y0,''))
    while queue:
        x, y, s = queue.pop(0)
        if (x,y) == (x1,y1):
            res = min(res, cheapestRobot( s+'A', robots-1 ))
            continue
        if (x,y) == dirpad['X']:
            continue
        if x < x1:
            queue.append( (x+1, y, s+'>' ))
        elif x > x1:
            queue.append( (x-1, y, s+'<' ))
        if y < y1:
            queue.append( (x, y+1, s+'v' ))
        elif y > y1:
            queue.append( (x, y-1, s+'^' ))
    return res        


def cheapestRobot( keys, robots ):
    if not robots:
        return len(keys)
    sumx = 0
    x0,y0 = dirpad['A']
    for c in keys:
        x1,y1 = dirpad[c]
        sumx += cheapestAuxPad( x0, y0, x1, y1, robots)
        x0,y0 = x1,y1
    return sumx


def cheapest( x0, y0, x1, y1, botcount=2 ):
    res = math.inf
    queue = []
    queue.append( (x0, y0, '') )
    while queue:
        x, y, s = queue.pop(0)
        if (x,y) == (x1,y1):
            res = min( res, cheapestRobot( s+'A', botcount ) )
            continue
        if (x,y) == buttons['X']:
            continue
        if x < x1:
            queue.append( (x+1, y, s+'>' ))
        elif x > x1:
            queue.append( (x-1, y, s+'<' ))
        if y < y1:
            queue.append( (x, y+1, s+'v' ))
        elif y > y1:
            queue.append( (x, y-1, s+'^' ))
    return res
    

def part1(data, bots=2):
    sumx = 0
    for line in data:
        res = 0
        x0,y0 = buttons['A']
        for c in line:
            if DEBUG:
                print("---",c,"---")
            x1,y1 = buttons[c]
            res += cheapest( x0, y0, x1, y1, bots)
            x0,y0 = x1,y1
        if DEBUG:
            print(res)
        val = int(''.join(s for s in line if s.isdigit()))
        sumx += val * res
    return sumx


print("Part 1:", part1(data,2))
print("Part 2:", part1(data,25))
if DEBUG:
    print(cheapestAuxPad.cache_info())
