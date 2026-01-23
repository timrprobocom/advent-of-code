import sys
import itertools

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    cogs = ( (5, 4), (2, 1) )
else:
    cogs = ( (17, 1), (7, 0), (19, 2), (5, 0), (3, 0), (13, 5) )

def part1(cogs):
    for i in itertools.count():
        for j,cog in enumerate(cogs,1):
            if (cog[1] + i + j) % cog[0]:
                break
        else:
            return i

def part2(cogs,p1):
    c1,c2 = 11,0
    c2 += len(cogs) + 1
    cycle = 1
    for i,_ in cogs:
        cycle *= i
    if DEBUG:
        print("cycle", cycle)
    for i in itertools.count(p1, cycle):
        if (c2 + i) % c1 == 0:
            return i

p1 = part1(cogs)
print('Part 1:', p1)
print('Part 2:', part2(cogs, p1))
