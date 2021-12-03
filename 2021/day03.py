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


def common(data):
    num = len(data)
    maxn = len(data[0])
    counts = [0]*maxn
    for row in data:
        for i,c in enumerate(row):
            if c == '1':
                counts[i] += 1
    res = 0
    for i in counts:
        res = res * 2
        if i*2 >= num:
            res += 1
    if DEBUG:
        print(num, maxn, counts, res)
    return res, ((1<<maxn)-res-1)

def pass1(data):
    most, least = common(data)
    return most * least

def pass2(data):
    maxn = len(data[0])

    hdata = data
    ldata = data

    for bitno in range(maxn):
        bit = 1<<(maxn-bitno-1)
        if len(hdata) > 1:
            most, least = common(hdata)
            hcrit = '1' if bit & most else '0'
            ndata = []
            for row in hdata:
                if row[bitno] == hcrit:
                    ndata.append( row )
            hdata = ndata

        if len(ldata) > 1:
            most, least = common(ldata)
            lcrit = '1' if bit & least else '0'
            ndata = []
            for row in ldata:
                if row[bitno] == lcrit:
                    ndata.append( row )
            ldata =  ndata
        if len(hdata) == 1 and len(ldata) == 1:
            break

    print(hdata, ldata)
    return int(hdata[0],2) * int(ldata[0],2)


print("Part 1:", pass1(data) )
print("Part 2:", pass2(data) )

