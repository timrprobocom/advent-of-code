import sys
import queue
import itertools
import threading
import copy

TRACE = 'itrace' in sys.argv

# The IntCode computer.

class Program(threading.Thread):
    count = itertools.count()

    def __init__(self, program, inputs=[]):
        threading.Thread.__init__(self)
        self.id = next(Program.count)
        self.pgm = program[:]
        self.pc = 0
        self.input = queue.Queue()
        self.output = queue.Queue()
        for i in inputs:
            self.input.put(i)
        self.rbase = 0

    def clone(self):
        return copy.deepcopy(self)

    def push(self, val):
        self.input.put( val )

    def read_input(self):
        return self.input.get()

    def pop(self):
        return self.output.get()

    def dump(self):
        q = []
        while not self.output.empty():
            q.append( self.output.get() )
        return q

    def opcode(self): 
        opc = self.pgm[self.pc]
        self.modes = opc//100
        if TRACE:
            print( f"{self.id}: At {self.pc}: {opc}" )
        self.pc += 1
        return opc % 100

    def nextmode(self):
        p = self.modes % 10
        self.modes //= 10
        return p

    def verify(self,loc):
        if loc >= len(self.pgm):
            if TRACE:
                print( f"Extending memory to {loc}" )
            self.pgm += [0] * (loc-len(self.pgm)+1)

    def fetch(self):
        mode = self.nextmode()
        operand = self.pgm[self.pc]
        self.pc += 1
        if mode == 0:
            self.verify(operand)
            val = self.pgm[operand]
        elif mode == 1:
            val = operand
        elif mode == 2:
            self.verify(operand+self.rbase)
            val = self.pgm[operand+self.rbase]
        if TRACE:
            print( f"{self.id} fetch[{mode}] {operand} = {val}" )
        return val

    def store(self, n):
        mode = self.nextmode()
        operand = self.pgm[self.pc]
        if TRACE:
            print( f"{self.id} store[{mode}] {n} at {operand}" )
        self.pc += 1
        if mode == 0:
            self.verify(operand)
            self.pgm[operand] = n
        elif mode == 2:
            self.verify(operand+self.rbase)
            self.pgm[operand+self.rbase] = n


    def run(self):
        while 1:
            opcode = self.opcode()
            if opcode == 1:
                self.store( self.fetch() + self.fetch() )
            elif opcode == 2:
                self.store( self.fetch() * self.fetch() )
            elif opcode == 3:
                 ip = self.read_input()
                 if TRACE:
                     print( self.id, "input", ip )
                 self.store( ip )
            elif opcode == 4:
                p = self.fetch()
                self.final = p
                self.output.put( p )
                if TRACE:
                    print( self.id, "output", p )
            elif opcode == 5:  # JT
                if self.fetch():
                    self.pc = self.fetch()
                else:
                    self.pc += 1
            elif opcode == 6:  # JF
                if not self.fetch():
                    self.pc = self.fetch()
                else:
                    self.pc += 1
            elif opcode == 7:  # JLT
                self.store( int(self.fetch() < self.fetch()))
            elif opcode == 8:  # JE
                self.store( int(self.fetch() == self.fetch()))
            elif opcode == 9:  # set rbase
                self.rbase += self.fetch()
            elif opcode == 99:
                break
            else:
                print( f"Explode, pc={self.pc}, pgm={self.pgm}" )
                break
        return self
