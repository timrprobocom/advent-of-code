
test = """\
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2""".splitlines()

data = open('day18.txt').readlines()


class CPU(object):
    def __init__(self, p):
        self.regs = { 'pc': 0, 'p': p }
        self.queue = {}

    def reg(self, rno):
        return self.regs[rno]

    def set(self, rno, val):
        self.regs[rno] = self.lookup(val)

    def lookup(self, v):
        if v in self.regs:
            return self.regs[v]
        else:
            return int(v)




#program = [ln.split() for ln in test]
program = [ln.split() for ln in data]
sound = 0

def execute( cpu ):
    global sound
    pc = cpu.reg('pc')
    opc = program[pc][0]
    reg = program[pc][1]
    val = program[pc][2] if len(program[pc]) > 2 else None
    print pc, opc, reg, val
    if opc == "set":
        cpu.set(reg, cpu.lookup(val))
    elif opc == "add":
        cpu.set(reg, cpu.reg(reg)+cpu.lookup(val))
    elif opc == "mul":
        cpu.set(reg, cpu.reg(reg)*cpu.lookup(val))
    elif opc == "mod":
        cpu.set(reg, cpu.reg(reg)%cpu.lookup(val))
    elif opc == "snd":
        sound = cpu.lookup(reg)
    elif opc == "rcv":
        if cpu.lookup(reg):
            print "Recovered ", sound
            return 0
    elif opc == "jgz":
        if cpu.lookup(reg) > 0:
            cpu.set('pc', pc + cpu.lookup(val))
            return 1
    cpu.set('pc', pc+1 )
    return 1
    
registers1 = CPU( 0 )
registers2 = CPU( 1 )

while execute(registers1):
    pass


