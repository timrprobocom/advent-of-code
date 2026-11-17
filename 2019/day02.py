import sys

test = [
"1,9,10,3,2,3,11,0,99,30,40,50",
"1,0,0,0,99",
"2,3,0,3,99",
"2,4,4,5,99,0",
"1,1,1,4,99,5,6,0,99"
]

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

live = open('day02.txt').read()

if TEST:
    data = test
else:
    data = live

# This program computes 466644 + 216000 x [1] + [2];

def run(pgm):
    pc = 0;
    while 1:
        opcode = pgm[pc]
        if opcode == 1:
            pgm[pgm[pc+3]] = pgm[pgm[pc+1]] + pgm[pgm[pc+2]]
            pc += 4
        elif opcode == 2:
            pgm[pgm[pc+3]] = pgm[pgm[pc+1]] * pgm[pgm[pc+2]]
            pc += 4
        elif opcode == 99:
            return pgm

if TEST:
    for ln in data:
        pgm = [int(p) for p in ln.split(",")]
        print( "Part 1:", run( pgm ) )
    exit(0)

data = [int(p) for p in data.split(",")]

def testrun( pgm, p1, p2 ):
    base = pgm[:]
    base[1] = p1
    base[2] = p2
    return run(base)[0]

# Part 1.

def part1( real ):
    return testrun(real, 12, 2)

# Part 2, brute force.
# Answer 8976.
# (19690720 - 466644) // 216000 == 89
# (19690720 - 466644 - 216000 * 89) == 76.

def part2( real ):
    for i in range(100):
        for j in range(100):
            k = testrun(real,i,j)
            if DEBUG:
                print(i, j, k )
            if k == 19690720:
                return i * 100 + j

print("Part 1:", part1(data))
print("Part 2:", part2(data))
