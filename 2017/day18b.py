test = """\
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d""".splitlines()

data = open('day18.txt').readlines()


class CPU(object):
    def __init__(self, p):
        self.id = p
        self.regs = { 'pc': 0, 'p': p }
        self.queue = []
        self.blocked = False
        self.traffic = 0

    def reg(self, rno):
        return self.regs[rno]

    def set(self, rno, val):
        self.regs[rno] = self.lookup(val)

    def lookup(self, v):
        if v in self.regs:
            return self.regs[v]
        else:
            return int(v)

    def send(self,v):
        self.traffic += 1
        self.queue.append(v)




#program = [ln.split() for ln in test]
program = [ln.split() for ln in data]


def execute( cpu, other ):
    if cpu.blocked: return 0
    pc = cpu.reg('pc')
    opc = program[pc][0]
    reg = program[pc][1]
    val = program[pc][2] if len(program[pc]) > 2 else None
    print cpu.id, pc, opc, reg, val
    if opc == "set":
        cpu.set(reg, cpu.lookup(val))
    elif opc == "add":
        cpu.set(reg, cpu.reg(reg)+cpu.lookup(val))
    elif opc == "mul":
        cpu.set(reg, cpu.reg(reg)*cpu.lookup(val))
    elif opc == "mod":
        cpu.set(reg, cpu.reg(reg)%cpu.lookup(val))
    elif opc == "snd":
        other.send( cpu.lookup(reg) )
        other.blocked = False
        print "CPU", cpu.id, "sent", cpu.lookup(reg)
    elif opc == "rcv":
        if cpu.queue:
            cpu.set(reg, cpu.queue.pop(0))
        elif other.blocked:
            print "BOTH BLOCKED"
            return 0
        else:
            cpu.blocked = True
            return 1
    elif opc == "jgz":
        if cpu.lookup(reg) > 0:
            cpu.set('pc', pc + cpu.lookup(val))
            return 1
    cpu.set('pc', pc+1 )
    return 1
    
registers1 = CPU(0)
registers2 = CPU(1)

while (execute(registers1,registers2), execute(registers2, registers1)) != (0,0):
    pass


print registers1.traffic
print registers2.traffic

