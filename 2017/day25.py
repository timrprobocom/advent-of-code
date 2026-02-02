import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

test = {
    'A':  [ (1, +1, 'B'),  (0, -1, 'B') ],
    'B':  [ (1, -1, 'A'),  (1, +1, 'A') ]
}

live = {
    'A': [ (1, +1, 'B'), (0, +1, 'C') ],
    'B': [ (0, -1, 'A'), (0, +1, 'D') ],
    'C': [ (1, +1, 'D'), (1, +1, 'A') ],
    'D': [ (1, -1, 'E'), (0, -1, 'D') ],
    'E': [ (1, +1, 'F'), (1, -1, 'B') ],
    'F': [ (1, +1, 'A'), (1, +1, 'E') ]
}



def lookup( tape, pos ):
    if not pos in tape:
        tape[pos] = 0
    return tape[pos]

class machine(object):
    def __init__( self, code, start ):
        self.machine = code
        self.pos = 0
        self.tape = { }
        self.state = start

    def step( self ):
        cur = lookup(self.tape, self.pos)
        do = self.machine[self.state][cur]
        self.tape[self.pos] = do[0]
        self.pos += do[1]
        self.state = do[2]

    def cksum( self ):
        if DEBUG:
            print(self.tape)
        return sum( self.tape.values() )

liveSteps = 12399302

turing = machine(live, 'A')
for i in range(liveSteps):
    if DEBUG and i % 10000 == 0:
        print(i, end='\r')
    turing.step()
print('Part 1:', turing.cksum())
