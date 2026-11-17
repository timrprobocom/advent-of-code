import sys

def fuel1(mass):
    return mass // 3 - 2

def fuel2(mass,sum=0):
    f = fuel1(mass)
    if f <= 0:
        return sum
    return fuel2(f,sum+f)

if 'test' in sys.argv:
    test = 100756
    print( "Part 1:", fuel1( test) )
    print( "Part 2:", fuel2( test) )
else:
    sum = 0
    for line in open('day01.txt').readlines():
        sum += fuel1(int(line))
    print( "Part 1:", sum )
    sum = 0
    for line in open('day01.txt').readlines():
        sum += fuel2(int(line))
    print( "Part 2:", sum )

