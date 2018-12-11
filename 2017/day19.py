test = """\
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ """.splitlines()

live = open('day19.txt').readlines()

data = live

m = max(len(ln) for ln in data)

row,col = 0,data[0].find('|')
direc = (1,0)
print "Grid is ",len(data),"rows x",m,"cols"

print row,col
collect = []
steps = 0
while 1:
    row,col = row+direc[0],col+direc[1]
    steps += 1
    print row,col,
    if row < 0 or row >= len(data) or col < 0 or col >= m:
        break

    ch = data[row][col]
    print ch
    if ch == '|' or ch == '-':
        continue
    if ch == ' ':
        break
    if ch == '+':
# If we can continue, we do.
        nr,nc = row+direc[0],col+direc[1]
        print "Testing",nr,nc
        if nr >= 0 and nr < len(data) and nc >= 0 and nc < m and data[nr][nc] != ' ':
            continue
        if direc[0] == 0:
# We are travelling horizontally.
            if row == 0:
                direc = (1,0)
            elif row == len(data)-1:
                direc = (-1,0)
            elif data[row+1][col] == ' ':
                direc = (-1,0)
            else:
                direc = (1,0)
        elif direc[1] == 0:
# We are travelling vertically.
            if col == 0:
                direc = (0,1)
            elif col == m-1:
                direc = (0,-1)
            elif data[row][col+1] == ' ':
                direc = (0,-1)
            else:
                direc = (0,1)
    else:
        collect.append(ch)
        print ''.join(collect)

print
print ''.join(collect)
print steps


