import sys

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

data = """\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a""".splitlines()

data = [k.strip() for k in open('day12.txt').readlines()]

ip = 0

class CPU:
    def __init__(self, init=0):
        self.register = {'a': 0, 'b':0, 'c':init, 'd':0 }
        self.ip = 0

    def eval(self,val):
        if val[0] > '9':
            return self.register[val]
        else:
            return int(val)

    def execute(self):
        if self.ip >= len(data):
            return False
        parts = data[self.ip].split()

        if parts[0] == 'cpy':
            self.register[parts[2]] = self.eval(parts[1])
            self.ip += 1
        elif parts[0] == 'inc':
            self.register[parts[1]] += 1
            self.ip += 1
        elif parts[0] == 'dec':
            self.register[parts[1]] -= 1
            self.ip += 1
        elif parts[0] == 'jnz':
            if self.eval(parts[1]):
                self.ip += int(parts[2])
            else:
                self.ip += 1

        return True

cpu = CPU(0)
while cpu.execute():
    pass
if DEBUG:
    print( cpu.register )
print( 'Part 1:', cpu.register['a'] )

cpu = CPU(1)
while cpu.execute():
    pass
if DEBUG:
    print( cpu.register )
print( 'Part 2:', cpu.register['a'] )