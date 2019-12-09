import sys
import queue
import itertools
import threading

TRACE = 'trace' in sys.argv
TESTS = 'test' in sys.argv

# The IntCode computer.

class Program(threading.Thread):
    count = 0
    def __init__(self, program, inputs=None):
        threading.Thread.__init__(self)
        self.id = Program.count
        Program.count += 1
        self.pgm = program[:]
        self.pc = 0
        self.input = queue.Queue()
        self.output = queue.Queue()
        if inputs:
            for i in inputs:
                self.input.put(i)
        self.rbase = 0

    def push(self, val):
        self.input.put( val )

    def pop(self):
        return self.output.get()

    def dump(self):
        q = []
        while not self.output.empty():
            q.append( self.output.get() )
        return q

    def opcode(self):
        opc = self.pgm[self.pc]
        self.modes = [(opc//100)%10, (opc//1000)%10, opc//10000]
        if TRACE:
            print( f"{self.id}: At {self.pc}: {opc}" )
        self.pc += 1
        return opc % 100

    def verify(self,loc):
        if loc >= len(self.pgm):
            if TRACE:
                print( f"Extending memory to {loc}" )
            self.pgm += [0] * (loc-len(self.pgm)+1)

    def fetch(self):
        nxtmode = self.modes.pop(0)
        operand = self.pgm[self.pc]
        self.pc += 1
        if nxtmode == 0:
            self.verify(operand)
            val = self.pgm[operand]
        elif nxtmode == 1:
            val = operand
        elif nxtmode == 2:
            self.verify(operand+self.rbase)
            val = self.pgm[operand+self.rbase]
        if TRACE:
            print( f"{self.id} fetch[{nxtmode}] {operand} = {val}" )
        return val

    def store(self, n):
        nxtmode = self.modes.pop(0)
        operand = self.pgm[self.pc]
        if TRACE:
            print( f"{self.id} store {n} at {operand}" )
        self.pc += 1
        if nxtmode == 0:
            self.verify(operand)
            self.pgm[operand] = n
        elif nxtmode == 2:
            self.verify(operand+self.rbase)
            self.pgm[operand+self.rbase] = n

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
                self.final = p
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
            elif opcode == 9:  # set rbase
                self.rbase += self.fetch()
            elif opcode == 99:
                break
            else:
                print( f"Explode, pc={self.pc}, pgm={self.pgm}" )
                break
        return self
