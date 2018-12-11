

# Pass 1, determine the size;


test = (
'#1 @ 1,3: 4x4',
'#2 @ 3,1: 4x4',
'#3 @ 5,5: 2x2'
)

live = list( k.strip() for k in open('day03.txt').readlines())

import re
match = r'#(\d*) @ (\d*),(\d*): (\d*)x(\d*)'

def makematrix( x, y ):
    matrix = []
    row = [0] * x
    for n in range(y):
        matrix.append( row[:] )
    return matrix

def maxi(lns):
    maxx = 0
    maxy = 0
    for ln in lns:
        parse = re.match(match,ln)
        data = list(int(x) for x in parse.groups())
        print data
        mx = data[1] + data[3]
        my = data[2] + data[4]
        if mx > maxx: maxx = mx
        if my > maxy: maxy = my
    return maxx, maxy

def fill(mat, lns):
    for ln in lns:
        parse = re.match(match,ln)
        n,x,y,w,h = (int(x) for x in parse.groups())
        for dx in range(w):
            for dy in range(h):
                mat[y+dy][x+dx] += 1
    return mat

def countm(mat):
    tot = 0
    for row in mat:
        for col in row:
            if col > 1:
                tot += 1
    return tot

def check( mat, lns ):
    for ln in lns:
        parse = re.match(match,ln)
        n,x,y,w,h = (int(x) for x in parse.groups())
        winner = True
        for dx in range(w):
            for dy in range(h):
                if mat[y+dy][x+dx] > 1:
                    winner = False
                    break
            if not winner:
                break
        if winner:
            print n

data = live

w,h = maxi( data )
mat = makematrix( w, h )
fill( mat, data )
print countm(mat)

check( mat, data )
