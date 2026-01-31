import sys
TEST = False
DEBUG = 'debug' in sys.argv

data = [k.strip() for k in open('day25.txt').readlines()]

def parse(data):
    return [ln.split() for ln in data]

class CPU:
    def __init__(self, pgm):
        self.register = {'a': 0, 'b':0, 'c':0, 'd':0 }
        self.program = pgm
        self.ip = 0
        self.outs = []

    def eval(self,val):
        if val[0] > '9':
            return self.register[val]
        else:
            return int(val)

    def execute(self):
        if self.ip >= len(self.program):
            return False
        parts = self.program[self.ip]

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
        elif parts[0] == 'out':
            r = self.eval(parts[1])
            self.outs.append( r )
            if len(self.outs) == 16: 
                return False
            self.ip += 1
        elif parts[0] == 'tgl':
            delta = self.eval(parts[1]) + self.ip
            if DEBUG:
                print( self.register )
                print( "fixing",delta )
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

def part1(program):
    i = 0
    while 1:
        cpu = CPU( program )
        cpu.register['a'] = i
        while cpu.execute():
            pass
        if DEBUG:
            print( i, cpu.outs )
        if cpu.outs == [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1] or cpu.outs == [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]:
            if DEBUG:
                print( cpu.register )
            return i
        i += 1
            
program = parse(data)
print('Part 1:', part1(program))
