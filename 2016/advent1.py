import sys
DEBUG = 0
moves = open('day1.txt').read().split(',')
x,y = (0,0)
face = 0
hits = {}
hits[(x,y)]=1
part2 = None
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
        if (x,y) in hits and not part2: 
            part2 = x, y
        hits[(x,y)]=1
    if DEBUG:
        print(direc, count, x, y)
if DEBUG:
    print(x, y)
print("Part 1:", abs(x)+abs(y))
x,y = part2
if DEBUG:
    print(x, y)
print("Part 2:", abs(x)+abs(y))
