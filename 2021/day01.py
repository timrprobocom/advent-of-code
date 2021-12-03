import sys
import numpy as np

test = [
199,
200,
208,
210,
200,
207,
240,
269,
260,
263
]

if 'test' in sys.argv:
    vals = test
else:
    vals = [int(i) for i in open('day01.txt')]

vals = np.array(vals)

def part1(data):
    return sum((data[1:] - data[:-1]) > 0)

def part2(data):
    return sum((data[3:] - data[:-3]) > 0)

print("Part 1:", part1(vals) )
print("Part 2:", part2(vals) )

