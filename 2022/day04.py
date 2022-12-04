import sys

test = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [s.rstrip() for s in open('day04.txt').readlines()]

DEBUG = 'debug' in sys.argv

def parse(row):
    p1,p2 = row.split(',')
    a1,a2 = p1.split('-')
    b1,b2 = p2.split('-')
    return int(a1),int(a2),int(b1),int(b2)

data = list(map(parse,data))

def part1(data):
    count = sum( (a1<=b1 and a2>=b2) or (b1<=a1 and b2>=a2) for a1,a2,b1,b2 in data )
    return count

def part2(data):
    if DEBUG:
        for a1,a2,b1,b2 in data:
            if (b1>=a1 and b1<=a2) or (a1>=b1 and a1<=b2):
                print(a1,a2,b1,b2)

    count = sum( (b1>=a1 and b1<=a2) or (a1>=b1 and a1<=b2) for a1,a2,b1,b2 in data)
    return count

print("Part 1:", part1(data))
print("Part 2:", part2(data))
