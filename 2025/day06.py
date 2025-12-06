import os
import sys
from functools import reduce
import operator

test = """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

ops = data.pop(-1).split()

# Prep for part 1 by transposing the matrix.

def transpose(data):
    cols = [[] for _ in range(len(ops))]
    for line in data:
        row = [int(k) for k in line.split()]
        for c,r in zip(cols,row):
            c.append(r)
    return cols

# Prep for part 2 by handling column by column.

def transform(data):
    ml = max(len(row) for row in data)
    cols = []
    col = []
    for i in range(ml):
        n = 0
        for line in data:
            if line[i] != ' ':
                n = n * 10 + int(line[i])
        if n:
            col.append(n)
        elif col:
            cols.append(col)
            col = []
    if col:
        cols.append(col)
    return cols

def part2(nums,ops):
    result = 0
    for col,op  in zip( nums,ops):
        if op == '*':
            result += reduce(operator.mul, col)
        else:
            result += sum(col)
    return result

print("Part 1:", part2(transpose(data),ops))
print("Part 2:", part2(transform(data),ops))
