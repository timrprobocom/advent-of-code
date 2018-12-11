test = (
'abcde',
'fghij',
'klmno',
'pqrst',
'fguij',
'axcye',
'wvxyz'
)

import itertools

data = [ln.strip() for ln in open('day02.txt').readlines()]

def compare(a,b):
    diff = 0
    make = ''
    for a1,b1 in zip(a,b):
        if a1 != b1:
            diff += 1
        else:
            make += a1
    return diff == 1, make

def process(data):
    for s1, s2 in itertools.combinations(data,2):
        ok, result = compare(s1,s2)
        if ok:
            print s1, s2, '\n', result

process(test)
process(data)
