import sys
import functools

DEBUG = 'debug' in sys.argv

class Machine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.regs = { 'w': 0, 'x': 0, 'y': 0, 'z': 0 }

    def fetch(self,c):
        if c in 'wxyz':
            return self.regs[c]
        else:
            return int(c)

    def store(self,c,v):
        self.regs[c] = v

    def run(self, program, inp):
        self.reset()
        inputs = inp[:]
        for line in program:
            if len(line) < 2:
                continue
            parts = line.rstrip().split()
            opc = parts[0]
            res = parts[1]
            if opc == 'inp':
                self.regs[res] = inputs.pop(0)
            elif opc == 'add':
                self.regs[res] += self.fetch(parts[2])
            elif opc == 'mul':
                self.regs[res] *= self.fetch(parts[2])
            elif opc == 'div':
                self.regs[res] //= self.fetch(parts[2])
            elif opc == 'mod':
                self.regs[res] %= self.fetch(parts[2])
            elif opc == 'eql':
                self.regs[res] = int(self.regs[res] == self.fetch(parts[2]))
        return len(inp)-len(inputs)

data = open('day24.txt').readlines()

# We get these constraints from the code itself.
#So dig[0]+14- 7 == dig[13]  +7 0 is 1,2
#So dig[1]+ 2-10 == dig[12]  -8 1 is 9
#So dig[2]+ 1- 5 == dig[11]  -4 2 is 5-9
#So dig[3]+13-12 == dig[6]   +1 3 is 1-8
#So dig[4]+ 5-12 == dig[5]   -7 4 is 8 9
#So dig[7]+ 9- 7 == dig[8]   +2 7 is 1-7
#So dig[9]+13- 8 == dig[10]  +5 9 is 1-4

valid = []
machine = Machine()
d1 = 9
d12 = 1
for d0 in (1,2):
    for d2 in (5,6,7,8,9):
        for d3 in range(1,9):
            for d4 in (8,9):
                for d7 in range(1,8):
                    for d9 in (1,2,3,4):
                        d13 = d0+7
                        d11 = d2-4
                        d6 = d3+1
                        d5 = d4-7
                        d8 = d7+2
                        d10 = d9+5
                        code = [d0,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13]
                        machine.run(data, code)
                        if machine.regs['z'] == 0:
                            valid.append( code )
print(len(valid), "keys")
print( "Part 1:", ''.join(str(s) for s in valid[-1]))
print( "Part 2:", ''.join(str(s) for s in valid[0]))

