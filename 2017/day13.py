import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

test = """\
0: 3
1: 2
4: 4
6: 4""".splitlines()

live = open('day13.txt').read().splitlines()

# Isn't this a modulo problem?  For a:b, I get caught if t+a % (2(b-1)) == 0.

data = []
for ln in test if TEST else live:
    p1,p2 = ln.split(': ')
    data.append( (int(p1), int(p2)) )

def part1(data):
    count = sum( a * b * (a % (2 * (b-1)) == 0) for (a,b) in data)
    return count

def part2(data):
    for i in range(4000000):
        for a,b in data:
            if (i+a) % (2 * (b - 1)) == 0:
                break
        else:
            return i

print('Part 1:',part1(data))
print('Part 2:',part2(data))
