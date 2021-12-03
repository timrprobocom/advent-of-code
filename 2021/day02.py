import sys

test = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2"""


if 'test' in sys.argv:
    idata = test.splitlines()
else:
    idata = open('day02.txt').readlines()

data = []
for row in idata:
    parts = row.rstrip().split()
    data.append( (parts[0], int(parts[1])) )


def pass1(data):
    pos = [0,0]
    for verb,cnt in data:
        if verb == 'forward':
            pos = [pos[0]+cnt, pos[1]]
        elif verb == 'up':
            pos = [pos[0], pos[1]-cnt]
        elif verb == 'down':
            pos = [pos[0], pos[1]+cnt]

    return pos, pos[0]*pos[1]


def pass2(data):
    # surface, depth, aim
    pos = [0,0,0]
    for verb,cnt in data:
        print(pos)
        if verb == 'forward':
            pos = [pos[0]+cnt, pos[1]+pos[2]*cnt, pos[2]]
        elif verb == 'up':
            pos = [pos[0], pos[1], pos[2]-cnt]
        elif verb == 'down':
            pos = [pos[0], pos[1], pos[2]+cnt]

    return pos, pos[0]*pos[1]


print("Part 1:", pass1(data) )
print("Part 2:", pass2(data) )

