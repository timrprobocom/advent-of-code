import math
import itertools

data = 33100000

# So, here's the question.  What is the smallest number where the
# sum of the factors is data / 10?

# What's the easy way to do factorization?

def factsum(n):
    sqn = int(math.sqrt(n))
    sumx = sum( i + n//i for i in range(1,sqn+1) if not n % i )
    if sqn * sqn == n:
        sumx -= sqn
    return sumx

def factsum2(n):
    sqn = int(math.sqrt(n))
    sumx = 0
    for i in range(1,sqn+1):
        if n % i:
            continue
        if i * 50 >= n:
            sumx += i
        if i < 50:
            sumx += n//i
    if sqn * sqn == n:
        sumx -= sqn
    return sumx

for i in itertools.count(1):
    if factsum(i) * 10 >= data:
        print( "Part 1:", i )
        break

# 12 = 1 2 3 4 6 12
# But only if N/i < 50 ?

for i in itertools.count(1):
    if factsum2(i) * 11 >= data:
        print( "Part 2:", i )
        break
