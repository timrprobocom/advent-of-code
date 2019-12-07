
import sys
import itertools

test = (
[3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],  # 43210
[3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0], # 54321
[3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0 ] # 365210
)


real = [ 3,8,1001,8,10,8,105,1,0,0,21,38,55,80,97,118,199,280,361,442,99999,3,9,101,2,9,9,1002,9,5,9,1001,9,4,9,4,9,99,3,9,101,5,9,9,102,2,9,9,1001,9,5,9,4,9,99,3,9,1001,9,4,9,102,5,9,9,101,4,9,9,102,4,9,9,1001,9,4,9,4,9,99,3,9,1001,9,3,9,1002,9,2,9,101,3,9,9,4,9,99,3,9,101,5,9,9,1002,9,2,9,101,3,9,9,1002,9,5,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99]

TRACE = 'trace' in sys.argv
TESTS = 'test' in sys.argv

# The IntCode computer.

class Program(object):
    def __init__(self, array):
        self.pgm = array[:]
        self.pc = 0
        self.inputs = []
        self.output = None

    def opcode(self):
        opc = self.pgm[self.pc]
        self.modes = [(opc//100)%10, (opc//1000)%10, opc//10000]
        if TRACE:
            print( f"At {self.pc}: {opc}" )
        self.pc += 1
        return opc % 100

    def fetch(self):
        nxtmode = self.modes.pop(0)
        operand = self.pgm[self.pc]
        self.pc += 1
        if TRACE:
            print( "fetch", operand if nxtmode else self.pgm[operand] )
        return operand if nxtmode else self.pgm[operand]

    def store(self, n):
        if TRACE:
            print( f"store {n} at {self.pgm[self.pc]}" )
        self.pgm[self.pgm[self.pc]] = n
        self.pc += 1

    def jump(self):
        self.pc = self.fetch()

    def skip(self):
        self.pc += 1

    def run(self):
        while 1:
            opcode = self.opcode()
            if opcode == 1:
                self.store( self.fetch() + self.fetch() )
            elif opcode == 2:
                self.store( self.fetch() * self.fetch() )
            elif opcode == 3:
                self.store( self.inputs.pop(0) )
            elif opcode == 4:
                self.output = self.fetch()
                print( "output", self.output )
            elif opcode == 5:  # JT
                if self.fetch():
                    self.jump()
                else:
                    self.skip()
            elif opcode == 6:  # JF
                if not self.fetch():
                    self.jump()
                else:
                    self.skip()
            elif opcode == 7:  # JLT
                self.store( 1 if self.fetch() < self.fetch() else 0 )
            elif opcode == 8:  # JE
                self.store( 1 if self.fetch() == self.fetch() else 0 )
            elif opcode == 99:
#                if TESTS or TRACE:
#                    print( self.pgm )
                return self.output
            else:
                print( f"Explode, pc={self.pc}, self={self.self}" )
                return None

def runsequence( pgm0 ):
    maxval = 0
    for inputset in itertools.permutations((0,1,2,3,4)):
        print( inputset )
        lastval = 0
        for ip in inputset:
            pgm = Program( pgm0 )
            pgm.inputs = [ip,lastval]
            lastval = pgm.run()
            print( lastval )
        maxval = max(maxval,lastval)
    return maxval
    

if TESTS:
    for p in test:
        print( "Answer: ", runsequence(p) )

# For part 1, enter 1.  For part 2, enter 5.

else:
    print( "Part 1:", runsequence(real))
