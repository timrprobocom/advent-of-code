import os
import sys

test = """\
987654321111111
811111111111119
234234234234278
818181911112111"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

def part2(data,n=12):
    count = 0
    for row in data:
        # In each loop, we take the largest number that still leave enough room.
        poss = []
        ix = 0
        while len(poss) < n:
            px = n-len(poss)
            m = max(row[ix : 1-px or None])
            poss.append(m)
            ix = row.index(m, ix) + 1

        count += int(''.join(poss))
        if DEBUG:
            print(row,''.join(poss))
                
    return count

print("Part 1:", part2(data,2))
print("Part 2:", part2(data,12))
