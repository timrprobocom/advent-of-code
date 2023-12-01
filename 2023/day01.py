import sys
import re

test = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

test2 = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

nums = ['\\d','one','two','three','four','five','six','seven','eight','nine']
pat = re.compile('|'.join(nums))

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day01.txt').readlines()


def part1(data):
    sumx = 0
    for line in data:
        dig = []
        for c in line:
            if c.isdigit():
                dig.append(int(c))
        sumx += dig[0]*10 + dig[-1]
    return sumx


def part2(data):
    sumx = 0
    for line in data:
        for z in nums[1:]:
            line = line.replace(z,z[0]+z+z[-1])
        p = pat.findall(line)
        dig = [int(i) if i.isdigit() else nums.index(i) for i in p]
        sumx += dig[0]*10 + dig[-1]
    return sumx


print("Part 1:", part1(data))
if 'test' in sys.argv:
    data = test2.splitlines()
print("Part 2:", part2(data))
