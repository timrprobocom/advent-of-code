import sys

test = """\
bvwbjplbgvbhsrlpgdmjqwftvncz
nppdvjthqldpwncqszvftbrmjlhg
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
"""

test2 = """\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
bvwbjplbgvbhsrlpgdmjqwftvncz
nppdvjthqldpwncqszvftbrmjlhg
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
"""


if 'test' in sys.argv:
    data = test.splitlines()
    data2 = test2.splitlines()
else:
    data = [s.rstrip() for s in open('day06.txt').readlines()]
    data2 = data

DEBUG = 'debug' in sys.argv


def part1(line,n=4):
    for i in range(n,len(line)):
        if len(set(line[i-n:i])) == n:
            return i


for test in data:
    print("Part 1:", part1(test,4))
for test in data2:
    print("Part 2:", part1(test,14))
