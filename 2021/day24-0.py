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

# This is what each phase of the program does.  It's building a 
# number in base 26.  We need to make sure the last phase cancels
# out the last remaining digit.

def run(ch, z, w):
    x = AX[ch] + (z % 26)
    z = z // DZ[ch]
    if x != w:
        z *= 26
        z += w + AY[ch]
    return z

# Extract the key constants from the code.

AX = []
DZ = []
AY = []
for lineno, line in enumerate(data):
    if "add x " in line and "add x z" not in line:
        AX.append(int(line.split()[2]))
    if "div z " in line:
        DZ.append(int(line.split()[2]))
    if "add y " in line and lineno%19 == 15:
        AY.append(int(line.split()[2]))

if DEBUG:
    print("Extracted from input")
    print("AX", AX)
    print("DZ", DZ)
    print("AY", AY)

assert len(AX) == 14
assert len(DZ) == 14
assert len(AY) == 14

# At each stage, if z is beyond a certain value, it's  hopeless and we can 
# early exit.  Determine these thresholds.

z_too_big = [26**DZ[i:].count(26) for i in range(len(DZ))]

CANDIDATES = list(range(1, 10))

# This is a depth-first search.  We start trying numbers at each stage
# until we exceed the threshhold for that stage.  When we get to the final
# stage, we add that digit to the possibles and back up.

@functools.lru_cache(maxsize=None)
def search(ch, zsofar):
    if ch == 14:
        if zsofar == 0:
            return [""]
        return []
    if zsofar > z_too_big[ch]:
        return []

    # Here's what x needs to be.

    xwillbe = AX[ch] + zsofar % 26
    wopts = CANDIDATES
    if xwillbe in range(1, 10):
        wopts = [xwillbe]

    ret = []
    for w in wopts:
        znext = run(ch, zsofar, w)
        for x in search(ch + 1, znext):
            ret.append(str(w) + x)
    return ret

solns = search(0, 0)
solns = list(map(int,solns))
print("Total solutions:", len(solns))
print("Part 1:", max(solns))
print("Part 2:", min(solns))
