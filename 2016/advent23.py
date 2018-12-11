data = """\
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a""".splitlines()

data = [k.strip() for k in open('day23a.txt').readlines()]

ip = 0

def parse(data):
    code = []
    for ln in data:
        code.append( ln.split() )
    return code

class CPU(object):
    def __init__(self, pgm):
        self.register = {'a': 12, 'b':0, 'c':0, 'd':0 }
        self.program = pgm
        self.ip = 0

    def eval(self,val):
        if val[0] > '9':
            return self.register[val]
        else:
            return int(val)

    def execute(self):
        if self.ip >= len(self.program):
            return False
        parts = self.program[self.ip]
#        print self.ip, parts

        if parts[0] == 'cpy':
            if parts[2] in self.register:
                self.register[parts[2]] = self.eval(parts[1])
            self.ip += 1
        elif parts[0] == 'inc':
            if parts[1] in self.register:
                self.register[parts[1]] += 1
            self.ip += 1
        elif parts[0] == 'dec':
            if parts[1] in self.register:
                self.register[parts[1]] -= 1
            self.ip += 1
        elif parts[0] == 'muladd':
            self.register[parts[3]] += self.register[parts[1]] * self.register[parts[2]]
            self.register[parts[1]] = 0
            self.register[parts[2]] = 0
            self.ip += 1
        elif parts[0] == 'nop':
            self.ip += 1
        elif parts[0] == 'jnz':
            if self.eval(parts[1]):
                self.ip += self.eval(parts[2])
            else:
                self.ip += 1
        elif parts[0] == 'tgl':
            delta = self.eval(parts[1]) + self.ip
            print self.register
            print "fixing",delta
            self.ip += 1
            if delta < 0 or delta >= len(self.program):
                return True
            if len(self.program[delta]) == 2:
                if self.program[delta][0] == 'inc':
                    self.program[delta][0] = 'dec'
                else:
                    self.program[delta][0] = 'inc'
            else:
                if self.program[delta][0] == 'jnz':
                    self.program[delta][0] = 'cpy'
                else:
                    self.program[delta][0] = 'jnz'

        return True

program = parse(data)
print program
cpu = CPU( program )

for i in range(100):
    while cpu.execute():
        print cpu.register
        pass
        

print cpu.register
