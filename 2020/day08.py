import os
import sys


test = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""".splitlines()

test2 = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""".splitlines()

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
elif 'test2' in sys.argv:
    data = test2
else:
    data = open('day08.txt').read().split('\n')[:-1]

d2 = []
for ln in data:
    parts = ln.split()
    d2.append((parts[0],int(parts[1])))

data = d2
del d2

def onepass(data):
    pc = 0
    accum = 0
    seen = set()
    while 1:
        if pc in seen:
            if DEBUG:
                print("  repeat", pc)
            return (False, accum)
        seen.add(pc)
        if pc == len(data):
            if DEBUG:
                print("  OK", pc, accum )
            return (True, accum)
        if pc > len(data):
            if DEBUG:
                print("  off", pc )
            return (False, accum)
        opc,delta = data[pc]
        if opc == "nop":
            pass
        elif opc == 'acc':
            accum += delta
        elif opc == 'jmp':
            pc += delta - 1
        pc += 1
    print("WHY?")
    return False

def cycle(base):
    for i in range(len(base)):
        data = base[:]
        if data[i][0] == 'acc':
            continue
        if DEBUG:
            print( "Trying", i )
        if data[i][0] == 'nop':
            data[i] = ('jmp',data[i][1])
        elif data[i][0] == 'jmp':
            data[i] = ('nop',data[i][1])
        (res,val) = onepass(data)
        if res:
            print( "SUCCESS", val )
            return val

res, val = onepass(data)
print( "Part 1:", val )
print( "Part 2:", cycle(data) )
