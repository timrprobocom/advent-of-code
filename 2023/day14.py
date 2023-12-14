import os
import sys
import itertools

test = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test
else:
    data = open(day+'.txt').read()


DEBUG = 'debug' in sys.argv

# Convert to a dict.

round = []
cube = set()
for y,row in enumerate(data.splitlines()):
    for x,c in enumerate(row):
        if c == '#':
            cube.add( (x,y) )
        elif c == 'O':
            round.append( (x,y) )

H = y+1
W = x+1

def tilt_n(round):
    round = sorted(round, key=lambda z: z[1])
    newround = []
    for x,y in round:
        while y and (x,y-1) not in newround and (x,y-1) not in cube:
            y -= 1
        newround.append( (x,y) )
    return newround

def tilt_w(round):
    # Sort by X.
    round = sorted(round)
    newround = []
    for x,y in round:
        while x and (x-1,y) not in newround and (x-1,y) not in cube:
            x -= 1
        newround.append( (x,y) )
    return newround

def tilt_s(round):
    # Sort by Y reversed.
    round = sorted(round, key=lambda z: -z[1])
    newround = []
    for x,y in round:
        while y < H-1 and (x,y+1) not in newround and (x,y+1) not in cube:
            y += 1
        newround.append( (x,y) )
    return newround

def tilt_e(round):
    # Sort by X reversed.
    round = sorted(round, reverse=True)
    newround = []
    for x,y in round:
        while x < W-1 and (x+1,y) not in newround and (x+1,y) not in cube:
            x += 1
        newround.append( (x,y) )
    return newround

def weight(round):
    return sum(H-z[1] for z in round)

def part1(round):
    return weight(tilt_n(round))

def part2(round):
    seen = [0]
    scores = [0]
    want = -1
    for i in itertools.count():
        round = tilt_n(round)
        round = tilt_w(round)
        round = tilt_s(round)
        round = tilt_e(round)
        cur = hash(tuple(round))
        scores.append(weight(round))
        if DEBUG:
            print(i+1,scores[-1])
        if cur in seen:
            pat0 = seen.index(cur)
            cycle = len(seen) - pat0
            want =  (1000000000 - pat0) % cycle + pat0
            break
        seen.append(cur)
    return scores[want]


print("Part 1:", part1(round)) # 64
print("Part 2:", part2(round)) # 83516
