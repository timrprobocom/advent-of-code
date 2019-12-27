import sys
from intcode import Program

# Run the program once to get the path.

class Prog25(Program):
    def __init__(self,pgm):
        Program.__init__(self,pgm)
        self.string = []

    def read_input(self):
        if not self.string:
            answer = input()
            self.string = list(ord(s) for s in answer+'\n' )
        return int(self.string.pop(0))
         
    def send_output(self,x):
        sys.stdout.write(chr(x))

real = list(eval(open('day25.txt').read()))
pgm = Prog25(real)
pgm.run()
print( ''.join(chr(c) for c in pgm.dump()) )
