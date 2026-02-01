#
# Spinlock
#
import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

buffer = [0]

test = 3
live = 328
data = test if TEST else live

def part1(data):
    p = 0
    for i in range(1,2018):
        if i % 10000 == 0:
            print(i, end='\r')
        p = (p+data) % i
        buffer.insert(p+1, i)
        p+=1

    i = buffer.index(2017)
    return buffer[i+1]

# The key lesson for part 2 is that we don't have to track the whole list.
# We never insert at position 0, so "the value after 0" will always be in
# position 1.  So, just track what gets put in position 1.

def part2(steps):
    size = 1
    pos = 0
    out = 0
    for i in range(50000000):
        new = (pos + steps) % size
        new += 1
        if new == 1:
            out = i+1
        pos = new
        size += 1
    return out

print('Part 1:', part1(data))
print('Part 2:', part2(data))
