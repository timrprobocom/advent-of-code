
data = """\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a""".splitlines()

data = [k.strip() for k in open('day12.txt').readlines()]

ip = 0

class CPU(object):
    def __init__(self):
        self.register = {'a': 0, 'b':0, 'c':1, 'd':0 }
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

cpu = CPU()
while cpu.execute():
    pass

print cpu.register
