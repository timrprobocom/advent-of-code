import sys
if 'test' in sys.argv:
    fn = 'test01.txt'
else:
    fn = 'day01.txt'

vals = [int(i) for i in open(fn)]


def pass1(data):
    ups = 0
    last = 999
    for i in data:
        if i > last:
            ups += 1
        last = i
    return ups


def pass2(data):
    last3 = [999,999,999]
    last = 2999
    ups = 0
    for i in data:
        last3 = last3[1:]+[i]
        if sum(last3) > last:
            ups += 1
        last = sum(last3)
    return ups

print("Part 1:", pass1(vals) )
print("Part 2:", pass2(vals) )

