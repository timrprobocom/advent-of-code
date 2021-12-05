import sys


test = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [line.rstrip() for line in open('day03.txt')]

# Is it better to keep the input as a string, or as an integer?
# It's the difference between row[i] and row & bit.

def common(data):
    num = len(data)
    bits = len(data[0])
    allone = (1 << bits) - 1
    counts = [0]*bits
    for row in data:
        for i,c in enumerate(row):
            counts[i] += int(c)
    res = 0
    for i in counts:
        res = res * 2 + (1 if i*2 >= num else 0)
    if DEBUG:
        print(num, bits, counts, res)
    return res, allone-res

def part1(data):
    most, least = common(data)
    return most * least

def part2(data):
    bits = len(data[0])

    hdata = data
    ldata = data

    for bitno in range(bits):
        bit = 1 << (bits-bitno-1)
        if len(hdata) > 1:
            most, least = common(hdata)
            crit = '1' if bit & most else '0'
            hdata = [row for row in hdata if row[bitno] == crit]

        if len(ldata) > 1:
            most, least = common(ldata)
            crit = '1' if bit & least else '0'
            ldata = [row for row in ldata if row[bitno] == crit]

        if len(hdata) == 1 and len(ldata) == 1:
            break

    print(hdata, ldata)
    return int(hdata[0],2) * int(ldata[0],2)


print("Part 1:", part1(data) )
print("Part 2:", part2(data) )

