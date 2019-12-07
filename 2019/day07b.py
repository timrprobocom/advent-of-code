import sys
import queue
import itertools
import threading

test = (
#Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):
[3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5],
#Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):
[3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
)

real = [ 3,8,1001,8,10,8,105,1,0,0,21,38,55,80,97,118,199,280,361,442,99999,3,9,101,2,9,9,1002,9,5,9,1001,9,4,9,4,9,99,3,9,101,5,9,9,102,2,9,9,1001,9,5,9,4,9,99,3,9,1001,9,4,9,102,5,9,9,101,4,9,9,102,4,9,9,1001,9,4,9,4,9,99,3,9,1001,9,3,9,1002,9,2,9,101,3,9,9,4,9,99,3,9,101,5,9,9,1002,9,2,9,101,3,9,9,1002,9,5,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99]

TRACE = 'trace' in sys.argv
TESTS = 'test' in sys.argv

# The IntCode computer.

class Program(threading.Thread):
    count = 0
    def __init__(self, array):
        threading.Thread.__init__(self)
        self.id = Program.count
        Program.count += 1
        self.pgm = array[:]
        self.pc = 0
        self.input = None
        self.output = queue.Queue()

    def opcode(self):
        opc = self.pgm[self.pc]
        self.modes = [(opc//100)%10, (opc//1000)%10, opc//10000]
        if TRACE:
            print( f"{self.id}: At {self.pc}: {opc}" )
            print( self.pgm[self.pc], self.pgm[self.pc+1], self.pgm[self.pc+2] )
        self.pc += 1
        return opc % 100

    def fetch(self):
        nxtmode = self.modes.pop(0)
        operand = self.pgm[self.pc]
        self.pc += 1
        if TRACE:
            print( self.id, "fetch", operand if nxtmode else self.pgm[operand] )
        return operand if nxtmode else self.pgm[operand]

    def store(self, n):
        if TRACE:
            print( f"{self.id} store {n} at {self.pgm[self.pc]}" )
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
                 ip = self.input.get()
                 if TRACE:
                     print( self.id, "input", ip )
                 self.store( ip )
#                self.store( self.input.get() )
            elif opcode == 4:
                p = self.fetch()
                self.output.put( p )
                if TRACE:
                    print( self.id, "output", p )
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
                print( f"Explode, pc={self.pc}, pgm={self.pgm}" )
                return None

def runsequence( pgm0 ):
    maxval = 0
    for ip in itertools.permutations([5,6,7,8,9]):
        if TRACE:
            print( ip )

        amps = [
            Program(pgm0),
            Program(pgm0),
            Program(pgm0),
            Program(pgm0),
            Program(pgm0)
        ]

# The output from 0 becomes the input to 1.

        q = amps[4].output
        for amp in amps:
            amp.input = q
            q = amp.output

# Set the initial input for each amp.

        for amp,val in zip(amps,ip):
            amp.input.put( val )

# Set the first signal into amp 0.

        amps[0].input.put( 0 )

# Go.

        for amp in amps:
            amp.start()

# Wait for all to exit.

        for amp in amps:
            amp.join()

# The answer is waiting in amp 4's output queue.

        maxval = max( maxval, amps[4].output.get())

    return maxval
    

if TESTS:
    for p in test:
        print( "Answer: ", runsequence(p) )

else:
    print( "Part 2:", runsequence(real))
