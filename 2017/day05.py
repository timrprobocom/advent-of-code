import sys

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

test = """\
0
3
0
1
-3"""

live = open('day5.txt').read()

data = list(map(int,(test if TEST else live).split()))

def part1(data, part):
    data = data[:]
    pc = 0
    n = 0
    while pc in range(len(data)):
        if DEBUG:
            print(pc, data)
        npc = pc +  data[pc]
        if part == 2 and data[pc] >= 3:
            data[pc] -= 1
        else:
            data[pc] += 1
        n += 1
        if npc not in range(len(data)):
            break
        pc = npc
    return n

print("Part 1:", part1(data,1))
print("Part 2:", part1(data,2))
