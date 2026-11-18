import sys
import itertools
from intcode import Program

TRACE = 'trace' in sys.argv
TEST = 'test' in sys.argv

test = (
[109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], # takes no input and produces a copy of itself as output.
[1102,34915192,34915192,7,4,7,99,0], # should output a 16-digit number.
[104,1125899906842624,99] # should output the large number in the middle.
)

live = [int(k) for k in open('day09.txt').read().replace('\n','').split(',')]

if TEST:
    for p in test:
        print( Program(p).run().dump() )

else:
    print( "Part 1:", Program(live, [1]).run().dump()[0] )
    print( "Part 2:", Program(live, [2]).run().dump()[0] )
