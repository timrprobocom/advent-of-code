import sys
data = [
'abba[mnop]qrst',
'abcd[bddb]xyyx',
'aaaa[qwer]tyui',
'ioxxoj[asdfgh]'
]

data = [
'aba[bab]xyz',
'xyx[xyx]xyx',
'aaa[kek]eke',
'zazbz[bzb]cdb'
]

def validate(code):
    print code
    within = False
    sequences = { False: [], True: [] }
    for i in range(len(code)-2):
        if code[i] == '[':
            within = True
        elif code[i] == ']':
            within = False
        elif code[i] == code[i+2] and code[i] != code[i+1]:
            sequences[within].append( code[i:i+3] )
    print sequences
    for aba in sequences[False]:
        other = aba[1] + aba[0] + aba[1]
        if other in sequences[True]:
            return True
    return False


data = [k.strip() for k in open('../Downloads/day7.txt').readlines()]

counts = { False: 0, True: 0 }
for line in data:
    val = validate(line)
    print line, val
    counts[val] += 1

print counts
           
