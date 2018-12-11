
#
#
# OK, on a 350x350 grid
# Find the distance from each point in the grid to each point in the 
#

# Start with 10x10.

test = (
    (1, 1),
    (1, 6),
    (8, 3),
    (3, 4),
    (5, 5),
    (8, 9)
)

live = tuple(tuple(int(p) for p in ln.split(',')) for ln in open('day06.txt').readlines())

def create( sq ):
    mat = []
    for i in range(sq):
        mat.append( [-1]*sq )
    return mat

SQ = 10
data = test

SQ = 358
data = live

mat = create(SQ)

for i,p in enumerate(data):
    x,y = p
    mat[y][x] = i

for y in range(SQ):
    for x in range(SQ):
        mind = 9999
        minxy = []
        for i,pts in enumerate(data):
            man = abs(x-pts[0]) + abs(y-pts[1])
            if man == mind:
                minxy.append( i )
            elif man < mind:
                mind = man
                minxy = [i]
        if len(minxy) == 1:
            mat[y][x] = minxy[0]

print mat

for y in range(min(SQ,80)):
    s = ''
    for x in range(min(SQ,80)):
        c = mat[y+50][x+50]
        if c < 0:
            s += '.'
        else:
            s += chr(64+c)
    print s

tots = [0]*len(data)
for y in range(SQ):
    for x in range(SQ):
        if mat[y][x] >= 0:
            tots[mat[y][x]] += 1

for x in range(SQ):
    if mat[x][0] >= 0:  tots[mat[x][0]] = 0
    if mat[x][-1] >= 0: tots[mat[x][-1]] = 0
    if mat[0][x] >= 0:  tots[mat[0][x]] = 0
    if mat[-1][x] >= 0: tots[mat[-1][x]] = 0

print tots
print max(tots)
