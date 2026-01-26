import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = 5
else:
    data = 3018458


def onepass( table, start ):
    nxt = start ^ (len(table) & 1)
    newtable = []
    if start:
        for i in range(len(table)):
            if i & 1:
                newtable.append(table[i])
    else:
        for i in range(len(table)):
            if not i & 1:
                newtable.append(table[i])
    return newtable, nxt
    
def part1(data):
    table = range(1,data+1)
    nxt = 0
    while len(table) > 1:
        table, nxt = onepass( table, nxt )
        if DEBUG:
            print( table, nxt )
    return table[0]    

def onepass2( table ):
    if len(table) == 3:
        return [table[-1]]
    elif len(table) == 4:
        return [table[0]]

    newseq = []
    half = len(table) // 2
    
# For odd tables, we:
#   skip 1 take 1 skip 2 take 1 ...
# For even tables, we:
#                 skip 2 take 1 ...

# So we always skip 3.
# We start with half+1 if odd, half+2 if even.

    pick = half + 2 - (len(table) & 1)
    if DEBUG:
        print( half, pick )
    rest = len(table) - half
    while pick < len(table):
        if DEBUG:
            print( pick, table[pick] )
        newseq.append( table[pick] )
        pick += 3

    got = rest - len(newseq)

    if got < half:
        return table[got:half]+newseq+table[:got]
    else:
        return newseq + table[:half]

# This is the optimized sequence.

def part2(x):
    table = list(range(1, x+1))
    while len(table) > 1:
        table = onepass2( table )
        if DEBUG and len(table) < 50:
            print( table )
    return table[0]

if DEBUG:
    for i in (5,7,21,22,23,24):
        part2(i)

print('Part 1:', part1(data))
print('Part 2:', part2(data))
