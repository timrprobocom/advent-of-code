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
    vals = test.splitlines()
else:
    vals = open('day01.txt').readlines()

def part1(vals):
    accum = 0
    maxx = 0
    for line in vals:
        line = line.strip()
        if not line:
            maxx = max(maxx,accum)
            accum = 0
        else:
            accum += int(line)
    return maxx

def part2(vals):
    accum = [0]
    for line in vals:
        line = line.strip()
        if not line:
            accum.append(0)
        else:
            accum[-1] += int(line)
    return sum(sorted(accum)[-3:])

print(part1(vals))
print(part2(vals))
