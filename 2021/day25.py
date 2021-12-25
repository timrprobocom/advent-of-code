import sys

test = """\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day25.txt').readlines()

HEIGHT = len(data)
WIDTH = len(data[0].rstrip())

# Convert the map to a set of coordinates.

c_right = set()
c_down = set()

for y,row in enumerate(data):
    for x,cell in enumerate(row):
        if cell == '>':
            c_right.add( (x,y) )
        elif cell == "v":
            c_down.add( (x,y) )

def printgrid(c_right, c_down):
    grid = [['.']*WIDTH for _ in range(HEIGHT)]
    for x,y in c_right:
        grid[y][x] = '>'
    for x,y in c_down:
        grid[y][x] = 'v'
    for row in grid:
        print(''.join(row))


def generation(c_right, c_down):
    changes = 0
    new_right = set()
    new_down = set()
    for x,y in c_right:
        dx = 0 if x==WIDTH-1 else x+1
        if (dx,y) in c_right or (dx,y) in c_down:
            new_right.add( (x,y) )
        else:
            changes += 1
            new_right.add( (dx,y) )
    for x,y in c_down:
        dy = 0 if y==HEIGHT-1 else y+1
        if (x,dy) in new_right or (x,dy) in c_down:
            new_down.add( (x,y) )
        else:
            changes += 1
            new_down.add( (x,dy) )

    return changes, new_right, new_down


if DEBUG:
    printgrid(c_right,c_down)
for gen in range(999):
    n,c_right,c_down = generation(c_right,c_down)
    if DEBUG:
        printgrid(c_right,c_down)
        print(n)
    if not n:
        break

print("Part 1:", gen+1)



#print( "Part 1:", part1(convert(data1)) )
#print( "Part 2:", part2(convert(data2)) )

