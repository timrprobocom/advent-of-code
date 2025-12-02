import os
import sys

test = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""

day = os.path.splitext(os.path.basename(__file__))[0]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = ''.join(test).replace('\n','')
else:
    data = open(day+'.txt').read()

def part1(data):
    count = 0
    for row in data.split(','):
        l,r = row.split('-')
        ln = int(l)
        rn = int(r)

        # If they are not the same length, adjust the odd one.
        # If left is odd, replace it by 1000.
        # If right is odd, replace it by 9999.
        if len(l) % 2:
            if len(r) % 2:
                continue
            else:
                l = '1' + '0'*len(l)
        elif len(r) % 2:
            r = '9'*len(l)

        lhalf = l[0:len(l)//2]
        lhalfn = int(lhalf)
        rhalfn = int(r[0:len(l)//2]) + 1

        while lhalfn < rhalfn:
            llln = int(str(lhalfn)+str(lhalfn))
            if ln <= llln <= rn:
                count += llln
            lhalfn += 1
        if DEBUG:
            print(l, r, count)
    return count

# This is a shameful brute force approach.

def check(num):
    ns = str(num)
    n = len(ns)
    for i in range(1,n//2+1):
        if n % i:
            continue
        for j in range(i,n,i):
            if ns[j:j+i] != ns[:i]:
                break
        else:
            return True
    return False

def part2(data):
    count = 0
    for row in data.split(','):
        l,r = row.split('-')
        ln = int(l)
        rn = int(r)
        for n in range(ln,rn+1):
            if check(n):
                count += n
        if DEBUG:
            print(l,r,n)
    return count

print("Part 1:", part1(data))
print("Part 2:", part2(data))
