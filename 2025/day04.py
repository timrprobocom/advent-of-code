import os
import sys

test = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

DIR = ( (-1,-1),(-1,0),(-1,1),
        ( 0,-1),       ( 0,1),
        ( 1,-1), (1,0),( 1,1))

rolls = set()
for y,row in enumerate(data):
    for x,col in enumerate(row):
        if col == '@':
            rolls.add( (x, y) )

def part1(rolls):
    total = 0
    for x,y in rolls:
        count = sum(((x+dx,y+dy) in rolls) for dx,dy in DIR)
        total += count < 4
    return total

def part2(rolls):     
    removed = 0
    while 1:
        nrolls = set()
        for x,y in rolls:
            count = sum((x+dx,y+dy) in rolls for dx,dy in DIR)
            if count >= 4:
                nrolls.add( (x,y) )
        if len(rolls) == len(nrolls):
            break
        removed += len(rolls) - len(nrolls)
        rolls = nrolls
    return removed

print("Part 1:", part1(rolls))
print("Part 2:", part2(rolls))
