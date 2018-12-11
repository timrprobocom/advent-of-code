test = (
'abcdef',
'bababc',
'abbcde',
'abcccd',
'aabcdd',
'abcdee',
'ababab'
)

data = open('day02.txt').readlines()

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

twos = 0
threes = 0
for s in data:
    t2, t3 = check(s)
    if t2: twos += 1
    if t3: threes += 1

print twos, threes, twos * threes
