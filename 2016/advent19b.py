
test = 5
chk = 7
prod = 3018458


def onepass( table ):
    if len(table) == 3:
        return [table[-1]]
    elif len(table) == 4:
        return [table[0]]

    newseq = []
    half = len(table) / 2
    
# For odd tables, we:
#   skip 1 take 1 skip 2 take 1 ...
# For even tables, we:
#                 skip 2 take 1 ...

# So we always skip 3.
# We start with half+1 if odd, half+2 if even.

    pick = half + 2 - (len(table) & 1)
    print half, pick
    rest = len(table) - half
    while pick < len(table):
        print pick, table[pick]
        newseq.append( table[pick] )
        pick += 3

    got = rest - len(newseq)

    if got < half:
        return table[got:half]+newseq+table[:got]
    else:
        return newseq + table[:half]

def simple( table, i ):
    print i, table
    if i < (len(table)+1)/2:
        print table.pop( i + len(table)/2 )
        return i+1
    else:
        print table.pop( i + len(table)/2 - len(table) )
        return i

# This is the brute force sequence.

def try2(x):
    print "******", x, "******"
    table = range(1, x+1)
    i = 0
    while len(table) > 1:
        i = simple( table, i )
        if i >= len(table):
            i = 0
    print table
    

# This is the optimized sequence.

def try1(x):
    print "******", x, "******"
    table = range(1, x+1)
    while len(table) > 1:
        table = onepass( table )
        if len(table) < 50: print table

for i in (5,7,21,22,23,24):
    try1(i)
    try2(i)

try1(prod)
