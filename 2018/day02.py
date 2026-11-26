import sys
import itertools

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

test = (
'abcdef',
'bababc',
'abbcde',
'abcccd',
'aabcdd',
'abcdee',
'ababab'
)

test2 = (
'abcde',
'fghij',
'klmno',
'pqrst',
'fguij',
'axcye',
'wvxyz'
)

live = [ln.strip() for ln in open('day02.txt').readlines()]

if TEST:
    data = test
else:
    data = live

def check(s):
    cnts = {}
    for c in s:
        if not c in cnts:
            cnts[c] = 1
        else:
            cnts[c] += 1

    two = 0
    three = 0
    for c,cnt in cnts.items():
        if cnt == 2:
            two += 1
        if cnt == 3:
            three += 1

    return (two, three)

def part1(data):
    twos = 0
    threes = 0
    for s in data:
        t2, t3 = check(s)
        if t2: twos += 1
        if t3: threes += 1

    if DEBUG:
        print( twos, threes, twos * threes )
    return twos * threes

def compare(a,b):
    diff = 0
    make = ''
    for a1,b1 in zip(a,b):
        if a1 != b1:
            diff += 1
        else:
            make += a1
    return diff == 1, make

def part2(data):
    for s1, s2 in itertools.combinations(data,2):
        ok, result = compare(s1,s2)
        if ok:
            if DEBUG:
                print( s1, s2, '\n', result )
            break
    return result

print("Part 1:", part1(data))
if TEST:
    data = test2
print("Part 2:", part2(data))

