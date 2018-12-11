dataset = """\
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]""".splitlines()

dataset = "qzmt-zixmtkozy-ivhz-343[xxxxx]"
dataset = open('../Downloads/day4.txt')

import re

def decode( name, code ):
    result = ""
    for c in name:
        if c == '-':
            result += ' '
        else:
            result += chr((ord(c) - ord('a') + code) % 26 + ord('a'))
    return result

for ln in dataset:
    ln = ln.strip()
    x = re.search( r'-\d+', ln )
    code = ln[0:x.start()]
    room = int(ln[x.start()+1:x.end()])
    cksum = ln[x.end():]

    print room, ln, decode(code,room)

def makeSum( code ):
    count = {}
    for c in code:
        if c == '-':
            continue
        if c not in count: 
            count[c] = 1
        else:
            count[c] += 1

    # Now invert this.

    bycount = {}
    keys = count.keys()
    keys.sort()
    for k in keys:
        v = count[k]
        if v not in bycount:
            bycount[v] = k
        else:
            bycount[v] += k

    keys = bycount.keys()
    keys.sort()
    keys.reverse()
    sumx = ''

    for k in keys:
        sumx += bycount[k]
        if len(sumx) >= 5:
            return sumx[:5]

def part1():
    valid = 0
    for ln in dataset:
        ln = ln.strip()
        x = re.search( r'-\d+', ln )
        code = ln[0:x.start()]
        room = ln[x.start()+1:x.end()]
        cksum = ln[x.end():]

        mysum = makeSum( code )

        print code, room, cksum, mysum
        if cksum[1:-1] == mysum:
            valid += int(room)
     
    print valid
