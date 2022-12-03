import sys

test = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""


if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day01.txt').readlines()

def part1(data):
    accum = 0
    maxx = 0
    for line in data:
        line = line.strip()
        if not line:
            maxx = max(maxx,accum)
            accum = 0
        else:
            accum += int(line)
    return maxx

def part2(data):
    accum = [0]
    for line in data:
        line = line.strip()
        if not line:
            accum.append(0)
        else:
            accum[-1] += int(line)
    return sum(sorted(accum)[-3:])

print("Part 1:", part1(data))
print("Part 2:", part2(data))
