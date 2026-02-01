import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

test = """\
5 1 9 5
7 5 3
2 4 6 8"""

test2 = """\
5 9 2 8
9 4 7 3
3 8 6 5"""

live = open('day2.txt').read()

def parse(lines):
    data = []
    for line in lines.splitlines():
        data.append( list(map(int, line.split())))
    return data

data = test if TEST else live
data = parse(data)

def part1(data):
    return sum(max(row)-min(row) for row in data)

def part2(data):
    sum = 0
    for row in data:
        for i,a in enumerate(row):
            for b in row[i+1:]:
                a1 = max(a,b)
                b1 = min(a,b)
                if a1 % b1 == 0:
                    sum += a1//b1
                    break
    return sum

print('Part 1:', part1(data))
if TEST:
    data = parse(test2)
print('Part 2:', part2(data))
