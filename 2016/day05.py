import sys
import hashlib
import itertools

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

key = 'uqwqemis'
#key = 'abc'

def part2(key):
    cnt = 0
    part1 = []
    part2 = ['-']*8
    while 1:
        raw = key + str(cnt)
        md5x = hashlib.md5(raw.encode('ascii')).hexdigest()
        if md5x[0:5] == '00000':
            if len(part1) < 8:
                part1.append( md5x[5] )
            if md5x[5] < '8':
                pos = ord(md5x[5]) - ord('0')
                if part2[pos] == '-':
                    part2[pos] = md5x[6]
                    if DEBUG:
                        print( raw, md5x, ''.join(part1), ''.join(part2) )
                    if not '-' in part2: break
        cnt += 1
    return part1,part2

p1, p2 = part2(key)
print('Part 1:', ''.join(p1))
print('Part 2:', ''.join(p2))