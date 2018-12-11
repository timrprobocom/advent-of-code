

inrules = {
"../.#": "##./#../...",
".#./..#/###": "#..#/..../..../#..#"
}

# ..
# .#

# AB
# CD
# Flips
# CD  BA
# AB  DC
# Rotated
# BD  DC  CA
# AC  BA  DB
#
# AC  BA  DB
# BD  DC  CA
#

def flip2h(r):
    return r[3]+r[4]+'/'+r[0]+r[1]
def flip2v(r):
    return r[1]+r[0]+'/'+r[4]+r[3]
def rotate2l(r):
    return r[1]+r[4]+'/'+r[0]+r[3]

# CFI
# BEH
# ADG

def flip3h(r):
    return r[2]+r[1]+r[0]+'/' + \
           r[6]+r[5]+r[4]+'/' + \
          r[10]+r[9]+r[8]
def flip3v(r):
    return r[8:11]+'/'+r[4:7]+'/'+r[0:3]
def rotate3l(r):
    return r[2]+r[6]+r[10] + '/' + \
           r[1]+r[5]+r[9] + '/' + \
           r[0]+r[4]+r[8]

def convert(inrules):
    rules2 = {}
    rules3 = {}
    for r,v in inrules.items():
        v = v.split('/')
        if r[2] == '/':
            rules2[r] = v
#            print r, flip2h(r), flip2v(r), rotate2l(r)
            r2 = r
            for i in range(3):
                r2 = rotate2l(r2)
                if r2 not in rules2:
                    rules2[r2] = v

            r2 = flip2h(r)
            rules2[r2] = v
            for i in range(3):
                r2 = rotate2l(r2)
                if r2 not in rules2:
                    rules2[r2] = v

            r2 = flip2v(r)
            rules2[r2] = v
            for i in range(3):
                r2 = rotate2l(r2)
                if r2 not in rules2:
                    rules2[r2] = v
        else:
            rules3[r] = v
#            print r, flip3h(r), flip3v(r), rotate3l(r)
            r3  = r
            for i in range(3):
                r3 = rotate3l(r3)
                if r3 not in rules3:
                    rules3[r3] = v

            r3 = flip3h(r)
            rules3[r3] = v
            for i in range(3):
                r3 = rotate3l(r3)
                if r3 not in rules3:
                    rules3[r3] = v

            r3 = flip3v(r)
            rules3[r3] = v
            for i in range(3):
                r3 = rotate3l(r3)
                if r3 not in rules3:
                    rules3[r3] = v
    return rules2, rules3

def process2x2( grid ):
    print "2x2", len(grid)
    newgrid = []
    for i in range(0,len(grid),2):
        line1 = ''
        line2 = ''
        line3 = ''
        for j in range(0,len(grid[0]),2):
            p1 = grid[i][j:j+2]+'/'+grid[i+1][j:j+2]
            p2 = rules2[p1]
            line1 += p2[0]
            line2 += p2[1]
            line3 += p2[2]
        newgrid.extend( (line1, line2, line3) )
    return newgrid

def process3x3( grid ):
    print "3x3", len(grid)
    newgrid = []
    for i in range(0,len(grid),3):
        line1 = ''
        line2 = ''
        line3 = ''
        line4 = ''
        for j in range(0,len(grid[0]),3):
            p1 = grid[i][j:j+3]+'/'+grid[i+1][j:j+3]+'/'+grid[i+2][j:j+3]
            p2 = rules3[p1]
            line1 += p2[0]
            line2 += p2[1]
            line3 += p2[2]
            line4 += p2[3]
        newgrid.extend( (line1, line2, line3, line4) )
    return newgrid

def getdata():
    live = {}
    for ln in open('day21.txt').readlines():
        p1,p2 = ln.rstrip().split(' => ')
        live[p1] = p2
    return live

def process(grid):
    if len(grid) % 2 == 0:
        return process2x2(grid)
    else:
        return process3x3(grid)

def count(grid, ch):
    count = 0
    for ln in grid:
        count += ln.count(ch)
    return count


inrules = getdata()
rules2, rules3 = convert(inrules)
print len(rules2), "rules for 2x2"
#print rules2
print len(rules3), "rules for 3x3"
#print rules3


test = ".#.","..#","###"

grid = test
print '\n'.join(grid)
print count(grid,'#')
for i in range(18):
    grid = process(grid)
    print '\n'.join(grid)
    print len(grid), 'x', len(grid[0]), count(grid,'#'), count(grid,'.')

