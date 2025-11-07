import sys
moves = open('day1.txt').read().split(',')
x,y = (0,0)
face = 0
hits = {}
hits[(x,y)]=1
for m in moves:
    m = m.strip()
    direc = m[0]
    count = int(m[1:])
    if direc=='L':
        face = (face + 3) % 4
    else:
        face = (face + 1) % 4

    for i in range(count):
        if face==0:        # North
            y -= 1
        elif face==1:       # East
            x += 1
        elif face==2:       # South
            y += 1
        else:
            x -= 1
        if (x,y) in hits: 
            print(x, y, abs(x)+abs(y))
            sys.exit(1)
        hits[(x,y)]=1
    print(direc, count, x, y)
print(x, y)
print(abs(x)+abs(y))
