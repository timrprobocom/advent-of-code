import sys
import itertools
from intcode import Program

test = (
[3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],  # 43210
[3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0], # 54321
[3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0 ] # 365210
)


real = [ 3,8,1001,8,10,8,105,1,0,0,21,38,55,80,97,118,199,280,361,442,99999,3,9,101,2,9,9,1002,9,5,9,1001,9,4,9,4,9,99,3,9,101,5,9,9,102,2,9,9,1001,9,5,9,4,9,99,3,9,1001,9,4,9,102,5,9,9,101,4,9,9,102,4,9,9,1001,9,4,9,4,9,99,3,9,1001,9,3,9,1002,9,2,9,101,3,9,9,4,9,99,3,9,101,5,9,9,1002,9,2,9,101,3,9,9,1002,9,5,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99]

TRACE = 'trace' in sys.argv
DEBUG = 'debug' in sys.argv
TESTS = 'test' in sys.argv

def part1( pgm0 ):
    maxval = 0
    for inputset in itertools.permutations((0,1,2,3,4)):
        if DEBUG:
            print( inputset )
        lastval = 0
        for ip in inputset:
            lastval = Program(pgm0, [ip, lastval]).run().dump()[0]
            if DEBUG:
                print( lastval )
        maxval = max(maxval,lastval)
    return maxval
    
def part2( pgm0 ):
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

        amps[0].push( 0 )

# Go.

        for amp in amps:
            amp.start()

# Wait for all to exit.

        for amp in amps:
            amp.join()

# The answer is waiting in amp 4's output queue.

        maxval = max( maxval, amps[4].pop() )

    return maxval
    
if TESTS:
    for p in test:
        print( "Part 1: ", part1(p) )
        print( "Part 2: ", part2(p) )
else:
    print( "Part 1:", part1(real))
    print( "Part 2:", part2(real))
