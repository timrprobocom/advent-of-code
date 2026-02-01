# How do you represent a hex grid?
#
#
#       -1,-1   1,-1    3,-1
#    -2,0    0,0    2,0,   4,0
#       -1,1    1,1     3,1

test = (
    ("ne,ne,ne", 3),
    ("ne,ne,sw,sw", 0),
    ("ne,ne,s,s", 2),
    ("se,sw,se,sw,sw", 3)
)

live = open('day11.txt').read().rstrip()

# Moves.

moves = {
    "ne": (+1,-1),
    "nw": (-1,-1),
    "sw": (-1,+1),
    "se": (+1,+1),
    "n": (0,-2),
    "s": (0,+2)
}

def getdist(pos):
    pos = [abs(k) for k in pos]
    if pos[0] > pos[1]:
        return pos[0]
    return (pos[0]+pos[1]+1)//2

def walk(movelist):
    xmax = 0
    posn = (0,0)
    for mv in movelist.split(','):
        posn = (posn[0]+moves[mv][0], posn[1]+moves[mv][1])
        dist = getdist(posn)
        if dist > xmax:
            xmax = dist
        print(mv, posn)
    # Distance is
    # min(abs(x),abs(y)+1/2?
    return getdist(posn), xmax


for movelist, ans in test:
    print(walk(movelist), ans)

print(walk(live))
