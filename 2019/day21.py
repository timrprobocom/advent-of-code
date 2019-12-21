import sys
from intcode import Program
from tools import Point


TRACE = 'trace' in sys.argv

# So, we have to probe to find the holes.

real = list(eval(open('day21.txt').read()))

def run(instructions):
    pgm = Program(real)
    for c in '\n'.join(instructions):
        pgm.push(ord(c))
    pgm.run()
    dump = pgm.dump()
    print( ''.join(chr(i) for i in dump if i < 255) )
    if dump[-1] > 255:
        return dump[-1]
    return -1


# Jump spans 4
# I've seen 
#  #####...##     
#   DCBA
#  #####.#..#
#   DCBA A
#        B
#  #####.####

part1 = (
    "NOT C J",  # if +3 is hole
    "AND D J",  # but +4 is land
    "NOT A T",  # if +1 is hole
    "OR  T J",  # also jump
    "WALK\n"
)

print( "Part 1:", run(part1) )

# I like this because it's more general.
# ( !1 | !2 | !3 ) & 4 & (8 | (5 & 9))

part2 = (
    "NOT A J",
    "NOT B T",
    "OR  T J",
    "NOT C T",
    "OR  T J",
    "AND D J",
    "NOT E T",
    "NOT T T",
    "OR  H T",
    "AND T J",
    "RUN\n"
)

# Seen

# ####.#..#
# ####...#
# ####.#.##.####
# ####.##.######

print( "Part 2:", run(part2) )
