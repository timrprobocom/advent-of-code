import sys

DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

live = open('day23.txt').read().splitlines()

data = [ln.split() for ln in live]

def run(a):
    pc = 0
    reg = {'a':a, 'b':0}

    while pc < len(data):
        instr = data[pc]
        if instr[0] == 'hlf':
            reg[instr[1]] = reg[instr[1]] // 2
        elif instr[0] == 'tpl':
            reg[instr[1]] = reg[instr[1]] * 3
        elif instr[0] == 'inc':
            reg[instr[1]] = reg[instr[1]] + 1
        elif instr[0] == 'jmp':
            pc += int(instr[1]) - 1
        elif instr[0] == 'jie':
            if reg[instr[1][0]] % 2 == 0:
                pc += int(instr[2]) - 1
        elif instr[0] == 'jio':
            if reg[instr[1][0]] == 1:
                pc += int(instr[2]) - 1
        pc += 1
        dprint( pc, reg )
    return reg['b']

print( "Part 1:", run(0) )
print( "Part 2:", run(1) )
