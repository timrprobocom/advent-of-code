import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv


A = 16807
B = 48271
mod = 0x7fffffff

test = (65, 8921)
live = (277, 349)

data = test if TEST else live

def gen( start, mult, factor ):
    a = start
    while 1:
        a = (a * mult) % mod
        if a % factor == 0:
            yield a

def part1(vals):
    g1 = gen( vals[0], A, 1 )
    g2 = gen( vals[1], B, 1 )
    count = 0
    for i in range(40000000):
        p1 = next(g1)
        p2 = next(g2)
        count += p1 & 0xffff == p2 & 0xffff
    return count

def part2(vals):
    g1 = gen( vals[0], A, 4 )
    g2 = gen( vals[1], B, 8 )
    count = 0
    for i in range(5000000):
        p1 = next(g1)
        p2 = next(g2)
        count +=  p1 & 0xffff == p2 & 0xffff
    return count

print("Part 1:", part1(data))
print("Part 2:", part2(data))
