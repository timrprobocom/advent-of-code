
def fuel1(mass):
    return mass // 3 - 2

def fuel2(mass,sum=0):
    f = fuel1(mass)
    if f <= 0:
        return sum
    return fuel2(f,sum+f)

fuel = fuel2

for test in (12,14,1969,100756):
    print( fuel( test) )

sum = 0
for line in open('day01.txt').readlines():
    sum += fuel(int(line))
print( sum )

