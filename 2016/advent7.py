import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

if TEST:
    data = [
    'abba[mnop]qrst',
    'abcd[bddb]xyyx',
    'aaaa[qwer]tyui',
    'ioxxoj[asdfgh]'
    ]
else:
    data = [
    'aba[bab]xyz',
    'xyx[xyx]xyx',
    'aaa[kek]eke',
    'zazbz[bzb]cdb'
    ]

def validate1(code):
    within = False
    sequences = [0,0]
    for i in range(len(code)-3):
        if code[i] == '[':
            within = True
        elif code[i] == ']':
            within = False
        elif code[i] == code[i+3] and code[i+1] == code[i+2] and code[i] != code[i+1]:
            sequences[within] += 1
    return sequences[False] and not sequences[True]

def validate2(code):
    if DEBUG:
        print( code )
    within = False
    sequences = { False: [], True: [] }
    for i in range(len(code)-2):
        if code[i] == '[':
            within = True
        elif code[i] == ']':
            within = False
        elif code[i] == code[i+2] and code[i] != code[i+1]:
            sequences[within].append( code[i:i+3] )
    if DEBUG:
        print( sequences )
    for aba in sequences[False]:
        other = aba[1] + aba[0] + aba[1]
        if other in sequences[True]:
            return True
    return False

data = [k.strip() for k in open('day7.txt').readlines()]

def part2(data):
    counts = [0,0]
    for line in data:
        counts[0] += validate1(line)
        counts[1] += validate2(line)
    return counts

p1,p2 = part2(data)
print( 'Part 1:', p1 )
print( 'Part 2:', p2 )
