import sys
import re

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

data = """\
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]""".splitlines()

data = ["qzmt-zixmtkozy-ivhz-343[xxxxx]"]
if not TEST:
    data = open('day4.txt').readlines()


def decode( name, code ):
    result = ""
    for c in name:
        if c == '-':
            result += ' '
        else:
            result += chr((ord(c) - ord('a') + code) % 26 + ord('a'))
    return result

def decodeAll(data):
    for ln in data:
        ln = ln.strip()
        x = re.search( r'-\d+', ln )
        code = ln[0:x.start()]
        room = int(ln[x.start()+1:x.end()])
        cksum = ln[x.end():]

        print( room, ln, decode(code,room) )

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
    keys = sorted(count.keys())
    for k in keys:
        v = count[k]
        if v not in bycount:
            bycount[v] = k
        else:
            bycount[v] += k

    keys = sorted(bycount.keys(),reverse=True)
    sumx = ''

    for k in keys:
        sumx += bycount[k]
        if len(sumx) >= 5:
            return sumx[:5]

def part1(dataset):
    part2 = None
    valid = 0
    for ln in dataset:
        ln = ln.strip()
        x = re.search( r'-\d+', ln )
        code = ln[0:x.start()]
        room = int(ln[x.start()+1:x.end()])
        cksum = ln[x.end():]

        mysum = makeSum( code )

        if decode(code,room) == 'northpole object storage':
            part2 = room

        if DEBUG:
            print( code, room, cksum, mysum )
        if cksum[1:-1] == mysum:
            valid += room
     
    return valid,part2

p1,p2 = part1(data)
print( "Part 1:", p1 )
print( "Part 2:", p2 )
